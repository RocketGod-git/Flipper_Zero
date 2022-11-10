import click
from toolbox import __version__
from toolbox.server import server

from os import path
from pathlib import Path


def validate_port_permissions(ctx, param, value):
    try:
        # Windows doesn't have geteuid available and raises ImportError
        from os import geteuid
        if value < 1024 and geteuid() != 0:
            raise click.BadParameter(f"sudo permission required to bind to port '{value}'")
    except ImportError:
        pass

    return value


def validate_directory(ctx, param, value):
    resolved_path = Path(value).resolve()
    valid_directory = path.exists(resolved_path) and path.isdir(resolved_path)
    if not valid_directory:
        raise click.BadParameter(f"value '{resolved_path}' is not a valid folder")
    return str(resolved_path)


@click.version_option(__version__)
@click.group()
def cli():
    pass

@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind on")
@click.option(
    "--debug/--no-debug",
    is_flag=True,
    default=False,
    help="Enable debug mode. Note this exposes `/console` which could potentially be accessed remotely and access could be bruteforced.",
)
@click.option(
    "--reload/--no-reload",
    is_flag=True,
    default=False,
    help="Enable reloading of files. This includes python files *and* python files",
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose logging"
)
@click.option(
    "--password",
    required=False,
    default=None,
    help="A password is required to upload files. There is no username.",
)
@click.option(
    "-p",
    "--port",
    type=click.INT,
    required=True,
    callback=validate_port_permissions,
    help="the port to serve from",
)
@click.argument("root_user_directory", required=True, callback=validate_directory)
def serve(host, port, password, debug, reload, verbose, root_user_directory):
    root_toolbox_directory = Path(__file__).parent.parent

    server.serve(
        host=host,
        port=port,
        verbose=verbose,
        password=password,
        root_toolbox_directory=root_toolbox_directory,
        root_user_directory=root_user_directory,
        config_path=Path(__file__).parent / "config.json",
        use_debugger=debug,
        use_reloader=reload,
    )


def run():
    cli()


if __name__ == "__main__":
    run()
