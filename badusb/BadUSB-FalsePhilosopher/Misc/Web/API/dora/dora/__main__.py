import json
import subprocess
import signal
import sys
from shutil import which
import argparse
import os
from dora.printer import Printer 


def ripgrep(regex, path, rg_path, rg_arguments, rg_args_from_json_data):
    if not color:
        rg_arguments = f"{rg_arguments} --color=never"

    if rg_args_from_json_data:
        rg_arguments = f"{rg_arguments} {rg_args_from_json_data}"

    global command
    command = f"{rg_path} {rg_arguments} -- \"{regex}\" \"{path}\""

    output, error = subprocess.Popen(command,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     shell=True
                                     ).communicate()

    output = output.decode("utf-8").rstrip("\r\n")
    error = error.decode("utf-8")
    return output, error, command


def exit_gracefully(signum, frame):
    # Erase the current line and return the cursor to the beginning
    print("\033[2K", end="\r", flush=True)
    printer.bad("Scan got interrupted by CTRL-C")
    sys.exit(1)


def main():
    # Get the full path of the directory where this file file
    # is located. This is needed so that we can fetch data.json
    dora_path = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser(usage="%(prog)s [options]")

    parser.add_argument("path",
                        metavar='PATH',
                        action="store",
                        help="Path to directory or file to scan"
                        )

    parser.add_argument("--rg-path",
                        action="store",
                        default=which("rg"),
                        help="Specify path to ripgrep"
                        )

    parser.add_argument("--rg-arguments",
                        action="store",
                        default="--pretty",
                        help="Arguments you want to provide to ripgrep"
                        )

    parser.add_argument("--json",
                        action="store",
                        default=f"{dora_path}/db/data.json",
                        help="Load regex data from a valid JSON file (default: db/data.json)"
                        )

    parser.add_argument("--verbose", "-v", "--debug", "-d",
                        action="store_true",
                        default=False,
                        help="Display extra debugging information"
                        )

    parser.add_argument("--no-color",
                        action="store_true",
                        default=False,
                        help="Don't show color in terminal output"
                        )

    args = parser.parse_args()

    # Catch SIGINT (also known as CTRL-C) and exit gracefully
    signal.signal(signal.SIGINT, exit_gracefully)

    global color
    color = not args.no_color
    path = args.path
    json_data = args.json
    rg_path = args.rg_path
    rg_arguments = args.rg_arguments
    verbose = args.verbose

    # Create a printer object for displaying text.
    # We are making this global because exit_gracefully() also
    # requires this object in order to display the exit message.
    global printer
    printer = Printer(color=color, verbose=verbose)

    if which("rg") is None:
        printer.negative("Is ripgrep installed?")
        # Yes, I could use one print_content() function and triple quotes to have this
        # message span multiple lines, but that reduces the legibility of the code.
        printer.content("The ripgrep (rg) binary couldn't be found. Try specifying the path")
        printer.content("to 'rg' by using '--rg-path /path/to/rg'")
        printer.content("You can install it from here: https://github.com/BurntSushi/ripgrep")
        sys.exit(1)

    if verbose:
        printer.info(f"Path to ripgrep: {rg_path}")
        printer.info(f"RegEx source: {json_data}")

    with open(json_data, "r") as f:
        try:
            data = json.loads(f.read())
        except json.decoder.JSONDecodeError as e:
            printer.warning("Provided JSON data is invalid")
            printer.content(str(e))
            sys.exit(1)

        for item in data:
            regex = item.strip()
            service_name = item

            regex = data.get(service_name).get("regex")
            # Awfully long variable name, I know. I'm open for suggestions.
            rg_args_from_json_data = data.get(service_name).get("flags")
            info = data.get(service_name).get("info")

            printer.info(f"Checking for {service_name or regex}")
            output, error, command = ripgrep(regex=regex, path=path, rg_path=rg_path, rg_arguments=rg_arguments, rg_args_from_json_data=rg_args_from_json_data)

            if verbose:
                printer.info(f"{command}\n")

            # Erase the current line and return the cursor to the beginning.
            # This has no effect on the terminal output when --verbose is set
            # and that is because of the extra newline (\n) while showing
            # the ripgrep command.
            print("\033[2K", end="\r", flush=True)

            if error:
                printer.warning("Error from ripgrep")
                printer.content(error)
                printer.content(f"\nThe command that caused the error:\n $ {command}")
                sys.exit()

            if output:
                printer.positive(f"{service_name or regex}")

                if info is not None:
                    printer.content(info)

                printer.content(output)

                # Adding a spacer to the output for better legibility
                print("\n")

    printer.good("Scan has been completed!")


if __name__ == "__main__":
    main()
