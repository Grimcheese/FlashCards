"""Unit test module for handle_json.py module

Running this file as a script will execute each unit test 
and display output to stdout.

Current tests:
    get_files()
"""

from pathlib import Path

import handle_json
import json

failed = []
tested = []


def get_files_test():
    """Test get_files method."""

    name = "get_files()"
    tested.append(name)

    try:
        print("Testing get_files(dir)")

        directory = Path(Path.cwd())
        flist = handle_json.get_files(directory, extension=True)

        actual_files = ["invalidate_file.json", "validate_file.json"]
        print(f"Returned: {flist}")
        print(f"Comparing to {actual_files}")

        assert flist == actual_files
    except AssertionError:
        print("FAILURE: get_files_test failed")
        failed.append(name)
    except Exception as e:
        print("Uncaught exception.")
        print(e)
        failed.append(name)
        raise


def JSONHandler_test():
    """Test JSONHandler class."""

    name = "JSONHandler"
    print("Testing JSONHandler class")
    tested.append(name)

    valid_flashcard_file = "validate_file.json"
    file_obj1 = handle_json.JSONHandler(valid_flashcard_file)

    try:
        invalid_flashcard_file = "README.md"
        file_obj2 = handle_json.JSONHandler(invalid_flashcard_file)

        # Should not get here - exception should be raised
        failed.append(name)
    except json.JSONDecodeError:
        print("Correctly raised exception for non json file.")


def results():
    """Output results of the unit tests."""

    print("\n\nOutputting test results\n------------------------")
    num_succeeded = 0
    num_tested = 0
    for test in tested:
        num_tested = num_tested + 1
        if test in failed:
            print(f"FAILED: {test}, {num_succeeded}/{num_tested} successful")
        else:
            num_succeeded = num_succeeded + 1
            print(f"SUCCEEDED: {test}, {num_succeeded}/{num_tested} successful")


if __name__ == "__main__":
    print("Starting handle_json.py test file...")
    get_files_test()
    JSONHandler_test()

    results()
