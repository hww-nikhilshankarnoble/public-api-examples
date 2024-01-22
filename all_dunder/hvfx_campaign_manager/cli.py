"""
Command line interface for the Hokey campaign manager tool.
"""
# Built-in
import argparse
import logging
import sys

# Internal
from hvfx_campaign_manager import manager

__all__ = ["run_command_line"]


def start() -> int:
    """
    Start the campaign.
    """

    client = input("Please enter the client name").lower()
    jobid = input("Please enter the job id").lower()
    confirmation = input("Please confirm, the above is correct, by entering 'yes'")
    if confirmation != "yes":
        print("Exiting.")
        return 1

    print(f"Client: {client}")
    print(f"Job ID: {jobid}")
    try:
        manager.start_campaign(client, jobid)
    except Exception as e:
        print(f"Failed to start campaign: {e}")
        return 1

    return 0


def complete() -> int:
    """
    Complete the campaign.
    """
    try:
        manager.complete_campaign()
    except Exception as e:
        print(f"Failed to complete campaign: {e}")
        return 1

    return 0


def run_command_line(cmdline_args: list[str]) -> int:
    """
    Runs the command line interface with the given arguments.

    Args:
        cmdline_args (list[str]): The command line arguments.

    Returns:
        int: The return code.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    start_parser = subparsers.add_parser("start")
    complete_parser = subparsers.add_parser("complete")

    args = parser.parse_args(cmdline_args)

    # Set up logging.
    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.command == "start":
        return start()
    elif args.command == "complete":
        return complete()
    else:
        parser.print_help()
        return 1


def main() -> int:
    """
    Hokey Campaign Manager.
    """
    return run_command_line(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
