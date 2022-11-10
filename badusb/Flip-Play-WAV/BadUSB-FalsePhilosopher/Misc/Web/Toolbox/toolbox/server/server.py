from werkzeug.serving import run_simple
from .interfaces import allowed_interfaces, get_ip_address
from .make_app import make_app, ToolboxServerException
from .color import Color


def serve(
    verbose,
    host,
    port,
    password,
    root_toolbox_directory,
    root_user_directory,
    config_path,
    use_debugger=False,
    use_reloader=False,
):
    try:
        app = make_app(
            host=host,
            port=port,
            verbose=verbose,
            password=password,
            root_toolbox_directory=root_toolbox_directory,
            root_user_directory=root_user_directory,
            config_path=config_path,
            use_debugger=use_debugger,
            use_reloader=use_reloader,
        )
    except ToolboxServerException as e:
        print(str(e))
        exit(1)
    available_interfaces = [
        (interface, get_ip_address(interface)) for interface in allowed_interfaces()
    ]

    server_details = ""
    server_details += f" * Useful interfaces:\n"
    for (interface, ip) in available_interfaces:
        if ip is not None:
            server_details += (
                f" * {Color.green(interface).rjust(20)} {Color.green(ip.rjust(20))}\n"
            )

    print(server_details)
    run_simple(host, port, app, use_debugger=use_debugger, use_reloader=True)
