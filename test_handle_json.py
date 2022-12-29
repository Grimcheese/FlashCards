"""Unit test module for handle_json.py module

Running this file as a script will execute each unit test 
and display output to stdout.

Current tests:
    get_files()
"""

from pathlib import Path

import handle_json


def get_files_test():
    try:
        print("Testing get_files(dir)")

        directory = Path.cwd()
        flist = handle_json.get_files(directory)

        actual_files = ["test_handle_json.py"]
        print(f"Returned: {flist}")
        print(f"Comparing to {actual_files}")

        assert flist == actual_files
    except AssertionError:
        print("FAILURE: get_files_test failed")


if __name__ == "__main__":
    print("Starting handle_json.py test file...")
    get_files_test()
