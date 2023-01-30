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
    """Test get_files function."""

    name = "get_files()"
    tested.append(name)

    try:
        print("Testing get_files(dir)...")

        directory = Path(Path.cwd())
        flist = handle_json.get_files(directory, extension=True)

        actual_files = [
            "invalidate_file.json",
            "not_valid_json.json",
            "validate_file.json",
        ]
        print(f"\tReturned: {flist}")
        print(f"\tComparing to {actual_files}")

        assert flist == actual_files
    except AssertionError:
        print("FAILURE: get_files_test failed")
        failed.append(name)
    except Exception as e:
        print("Uncaught exception.")
        print(e)
        failed.append(name)
        raise


def is_valid_file_test():
    """Test is_valid_file function."""

    print("Testing is_valid_file()...")

    # Test valid file
    name = "is_valid_file() - valid file"
    tested.append(name)

    try:
        print("\tUsing a valid file.")
        valid_file = "validate_file.json"
        assert handle_json.is_valid_file(valid_file) == True
    except AssertionError:
        print(f"\tFAILURE: {name} failed")
        failed.append(name)

    # Test invalid file
    name = "is_valid_file() - invalid file"
    tested.append(name)
    try:
        print("\tUsing an invalid file.")
        invalid_file = "invalidate_file.json"
        assert handle_json.is_valid_file(invalid_file) == False
    except AssertionError:
        print(f"\tFAILURE: {name} failed")
        failed.append(name)


def JSONHandler_test():
    """Test JSONHandler class. Note that JSONHandler is tested only
    for json file types - not FlashCard json files.
    """

    name = "JSONHandler"
    print("Testing JSONHandler class...")
    tested.append(name)

    valid_files = "validate_file.json"
    invalid_files = ["README.md", "not_valid_json.json"]

    # Valid json file test
    valid_flashcard_file = "validate_file.json"
    file_obj1 = handle_json.JSONHandler(valid_flashcard_file)

    # Invalid, non-json file test
    invalid_objects = []
    for file in invalid_files:
        print(f"\tTrying invalid file: {file}")
        try:
            invalid_objects.append(handle_json.JSONHandler(file))

            # Should not get here - exception should be raised
            print("\tInvalid file has instantiated with no except raised.")
        except handle_json.InvalidJSONFile as e:
            print("\tCorrectly raised exception for non json or invalid json file.")

    if len(invalid_objects) > 0:
        failed.append(name)
    else:
        print("\tSuccess!")


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
    is_valid_file_test()

    results()
