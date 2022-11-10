from flask import (
    Blueprint,
    Flask,
    render_template,
    make_response,
    app,
    abort,
    current_app,
    request,
    redirect,
    url_for,
    session,
)
import logging
import base64
from typing import Optional
from http import HTTPStatus
from flask_wtf.csrf import CSRFProtect
from .file_server import (
    ServerConfig,
    FileServer,
    FileManager,
    ServerInvalidFilePath,
    ServerDirectoryListing,
    ServerFileResult,
)
from . import formatters
from .color import Color
from .payload_generator import PayloadGenerator, TEMPLATE_DIRECTORY
from flask_wtf.file import FileField, FileRequired
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from dataclasses import dataclass
from typing import Dict
import secrets
from http import HTTPStatus
from .interfaces import allowed_interfaces, get_ip_address
from flask_httpauth import HTTPBasicAuth


class UploadForm(FlaskForm):
    token_id = StringField("token", validators=[DataRequired()])
    file = FileField(validators=[FileRequired()])


class UploadTokenForm(FlaskForm):
    file_name = StringField("File Name", validators=[DataRequired()])


UploadTokenId = str


@dataclass
class UploadToken:
    id: UploadTokenId
    file_name: str


@dataclass
class IndexViewModel:
    payload_generator: PayloadGenerator
    directory_listing: ServerDirectoryListing
    upload_token_form: UploadForm
    upload_token: UploadToken
    has_uploads_enabled: bool


@dataclass
class Credentials:
    username: str
    password: str


class ToolboxServerException(Exception):
    pass


upload_tokens: Dict[UploadTokenId, UploadToken] = {}

server = Blueprint(
    "serve", __name__, template_folder=TEMPLATE_DIRECTORY, static_folder=None
)
server.app_template_filter("pretty_date")(formatters.pretty_date)

csrf = CSRFProtect()
auth = HTTPBasicAuth()


# No login required - shells can be accessed from anywhere
@server.route("/shells/<name>")
@server.route("/shells/<name>/<lport>")
@server.route("/shells/<name>/<lhost>/<lport>")
def shell(name: str, lhost: Optional[str] = None, lport: Optional[str] = None):
    payload_generator = PayloadGenerator()
    payload = payload_generator.generate(name=name, lhost=lhost, lport=lport)
    if payload is None:
        return abort(HTTPStatus.NOT_FOUND)
    response = make_response(payload)
    response.headers["Content-Type"] = "text/plain"
    return response


# No login required - debugging can be accessed from anywhere
@server.route("/debug/", defaults={"namespace": None})
@server.route("/debug/<path:namespace>")
def debug(namespace):
    value = request.args.get("value")
    if value:
        try:
            value = base64.b64decode(value)
        except:
            value = f"Unknown base: {value}"
    current_app.logger.info(
        "debug=%s value=%s", Color.green(namespace), Color.green(value)
    )
    return make_response("", HTTPStatus.OK)


# No login required - uploads must provide a one time token
@server.route("/uploads", methods=["POST"])
@csrf.exempt
def uploads():
    upload_form = UploadForm(meta={"csrf": False})
    if upload_form.validate_on_submit():
        upload_token_id = upload_form.token_id.data
        upload_token = upload_tokens.get(upload_token_id, None)

        if upload_token is None:
            return make_response(
                '{ "error": "token not valid" }\n', HTTPStatus.BAD_REQUEST
            )

        file_manager = FileManager(
            root_user_directory=current_app.config["ROOT_USER_DIRECTORY"],
            root_toolbox_directory=current_app.config["ROOT_TOOLBOX_DIRECTORY"],
        )

        file = upload_form.file.data
        file_name = upload_token.file_name
        new_file_path = Path(current_app.config["ROOT_USER_DIRECTORY"]) / file_name

        if not file_manager.is_allowed_user_file_path(new_file_path):
            return make_response(
                '{ "error": "invalid path" }\n', HTTPStatus.BAD_REQUEST
            )

        with file_manager.open_user_file(new_file_path, "wb") as new_file:
            current_app.logger.info(
                "Successfully wrote new file %s", Color.green(new_file_path)
            )
            new_file.write(file.read())

        upload_tokens.pop(upload_token_id, None)
        return make_response('{ "success": true }\n', HTTPStatus.CREATED)

    return make_response(upload_form.errors, HTTPStatus.BAD_REQUEST)


# No Login required - The root index is accessible so that it can easily serve arbitrary files
@server.route("/", defaults={"server_path": ""}, methods=["GET"])
@server.route("/<path:server_path>", methods=["GET"])
def index(server_path):
    payload_generator = PayloadGenerator()
    file_manager = FileManager(
        root_user_directory=current_app.config["ROOT_USER_DIRECTORY"],
        root_toolbox_directory=current_app.config["ROOT_TOOLBOX_DIRECTORY"],
    )
    server_config = ServerConfig(
        root_toolbox_directory=current_app.config["ROOT_TOOLBOX_DIRECTORY"],
        #  TODO: Remove config path and assume only built in files can be mapped
        config_path=current_app.config["CONFIG_PATH"],
        file_manager=file_manager,
    )
    file_server = FileServer(server_config=server_config)
    server_response = file_server.serve(server_path)

    if isinstance(server_response, ServerInvalidFilePath):
        return abort(HTTPStatus.NOT_FOUND)

    if isinstance(server_response, ServerFileResult):
        response = make_response(server_response.content)
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response

    if isinstance(server_response, ServerDirectoryListing):
        formdata = session.get("formdata")
        upload_form = UploadTokenForm(data=formdata)

        upload_token = upload_tokens.get(session.get("upload_token_id"))
        session.pop("upload_token_id", None)
        return render_template(
            "views/index.html",
            view_model=IndexViewModel(
                payload_generator=payload_generator,
                directory_listing=server_response,
                upload_token_form=upload_form,
                upload_token=upload_token,
                has_uploads_enabled=current_app.config["HAS_UPLOADS_ENABLED"],
            ),
        )

    return abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"{str(server_response.__class__)}")


# No login required - simply redirects to the index page
@server.route("/tokens", methods=["GET"])
def redirected():
    return redirect(url_for("serve.index"))


# Login required - this page can generate upload tokens
@server.route("/tokens", methods=["POST"])
@auth.login_required
def create_token():
    form = UploadTokenForm()
    upload_token = None
    if form.validate_on_submit():
        upload_token = UploadToken(
            id=secrets.token_hex(16),
            file_name=form.file_name.data,
        )
        upload_tokens[upload_token.id] = upload_token
        session["upload_token_id"] = upload_token.id

    session["formdata"] = request.form
    return redirect(url_for("serve.index"))


def validate_app(app):
    file_manager = FileManager(
        root_user_directory=app.config["ROOT_USER_DIRECTORY"],
        root_toolbox_directory=app.config["ROOT_TOOLBOX_DIRECTORY"],
    )

    try:
        ServerConfig(
            root_toolbox_directory=app.config["ROOT_TOOLBOX_DIRECTORY"],
            #  TODO: Remove config path and assume only built in files can be mapped
            config_path=app.config["CONFIG_PATH"],
            file_manager=file_manager,
        )
    except ValueError as e:
        raise ToolboxServerException(
            f"{str(e)}\nConfiguration problem occurred. Ensure that {Color.green('git submodule update --init --recursive')} has been run."
        )

    return True


def make_app(
    verbose,
    host,
    port,
    password,
    root_toolbox_directory,
    root_user_directory,
    config_path,
    use_debugger=False,
    use_reloader=False,
) -> Flask:
    app = Flask(
        __name__,
        static_url_path="/assets",
        static_folder=str(root_toolbox_directory / "toolbox" / "server" / "assets"),
    )
    app.config["ROOT_TOOLBOX_DIRECTORY"] = root_toolbox_directory
    app.config["ROOT_USER_DIRECTORY"] = root_user_directory
    app.config["CONFIG_PATH"] = config_path
    app.config["TEMPLATES_AUTO_RELOAD"] = use_reloader
    app.config["HAS_UPLOADS_ENABLED"] = password is not None
    secret_key = secrets.token_bytes(32)
    app.secret_key = secret_key
    csrf.init_app(app)

    if password:
        credentials = Credentials(
            username="", password=generate_password_hash(password)
        )
    else:
        credentials = None

    @auth.verify_password
    def verify_password(username, password) -> bool:
        if credentials is None:
            return False
        return check_password_hash(credentials.password, password)

    # TODO: Add middleware logging for IP, time, user agent details, highlighting on 404s etc.
    # log = logging.getLogger("werkzeug")
    # log.disabled = True

    app.logger.setLevel(logging.INFO)
    app.register_blueprint(server)
    validate_app(app)

    return app
