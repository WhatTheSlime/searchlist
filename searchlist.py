#!/usr/bin/env python3
import argparse
import configparser
import os
import sys
import subprocess
from tabulate import tabulate


#: Path of the file where the list of directories containing wordlists 
#: is located
CONFIGFILE = os.path.join(os.path.dirname(__file__), "searchlist.cfg")


def count_lines(filepath: str) -> str:
    """Count lines in a file

    Args: 
        filepath (str): File to count lines
    
    Returns:
        str: Number of lines in file
    """    
    return subprocess.check_output(
        ["wc", "-l", filepath]).decode("utf-8").split(" ")[0]


def is_query_in_file(filepath: str, query: str) -> True:
    """Search query in a file

    Args:
        filepath (str): File to inspect
        query (str): Query to search

    Returns:
        True: Query is in the file
    """
    if subprocess.check_output(["grep", "-i", query, filepath]):
        return True
    return False


def is_valid_path(filepath: str, query: str, exts: list) -> bool:
    """Check if a file path match a specific query

    Args:
        filepath (str): File path to check
        query (str): Query to match paths
        exts (list): File extensions white list

    Returns:
        bool: True if the path match the query, False otherwise
    """
    # Check extention is valid
    for ext in exts:
        if filepath.endswith(ext):
            # Check query terms
            for q in query:
                if q.lower() in filepath.lower():
                    return True
    return False


def find_files(start_path: str, query: list, exts: list) -> list:
    """Recursively finds file paths that match a query

    Args:
        start_path (str): Path to start the research 
        query (lst): Query to match paths
        exts (list): File extensions white list

    Results:
        list: Valid paths list
    """
    valid_files = []

    # Walking through sub files
    for root, dirs, files in os.walk(start_path):
        for file in files:
            path = os.path.join(root, file)
            if is_valid_path(path, query, exts):
                valid_files.append(path)
    
    return valid_files


def filepath_type(filepath: str) -> str:
    """Check if filepath exists

    Args:
        filepath (str): File path to check
    
    Returns:
        str: File path if exists
    """
    if os.path.isfile(filepath):
        return filepath
    else:
        raise argparse.ArgumentTypeError(f"'{filepath}' file not found")


def parse_args(args: list) -> list:
    """Parse user arguments

    Args:
        args (list): Program arguments

    Returns:
        argparse.NameSpace: NameSpace containing user arguments
    """
    parser = argparse.ArgumentParser(
        args, description="Search and well display wordlists")
    parser.add_argument(
        "query", metavar="TERM", type=str, nargs="+", 
        help="Query to search in filepath")
    parser.add_argument(
        "-n", "--number", type=int, 
        help="Display only full file path according to "
        "the same search without this flag")
    parser.add_argument(
        "--no-lines", action="store_true", help="Disable lines count")
    parser.add_argument(
        "-c", "--config", 
        metavar="FILEPATH", type=filepath_type, default=CONFIGFILE,
        help=f"Set configuration file (default is {CONFIGFILE})")
    return parser.parse_args()


def main():
    #: User arguments
    args = parse_args(sys.argv[1:])

    #: Load script configuration
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(args.config)
   
    #: Directories paths that contain wordlists
    dirs = list(config["Directories"].keys())

    #: File extensions to whitelist
    exts = list(config["Extensions"].keys())
    
    #: Files found
    files = []

    #: Total files number
    total = 0

    #: Table headers
    headers = ["N°", "File path"]
    if not args.no_lines:
        headers.append("Lines")

    # Iterate over directories 
    for d in dirs:
        #: Files whose paths match with the query
        files += sorted(find_files(d, args.query, exts))

        # Counting
        if args.number is None:
            curr_files = files[total:]
            print(f"==== {len(curr_files)} files founds in {d}/ ====\n")

            if curr_files:
                # Display results in tables                
                table = []

                for nb, filepath in enumerate(curr_files):
                    line = [total + nb, filepath.replace(f"{d}/", "")]

                    if not args.no_lines:
                        line.append(count_lines(filepath))

                    table.append(line)

                print(tabulate(table, headers=headers))
                print()

        # Updating total files number 
        total = len(files)

    if args.number is not None:
        print(files[args.number])
        return

    print(f"==== Total files found: {total} ====")


if __name__ == "__main__":
    main()