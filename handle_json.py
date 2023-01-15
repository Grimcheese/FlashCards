"""Module for FlashCards App that provides JSON file reading support.

Provides file reading and storage of the topics and prompts that are to be 
displayed by FlashCards. All data from the file is stored as a string but can
then be accessed using public methods from JSONTopicHandler.

Classes:
    JSONHandler
    JSONTopicHandler(JSONHandler)
    InvalidKeyError(Exception)

JSONHandler behaves as a base class. JSONTopicHandler inherits from JSONHandler 
to gain JSON file metadata and file reading capabilities. 
"""

import json
import jsonschema
import random

from pathlib import Path

# Module helper functions


def get_files(directory, extension=True, find_json=True, blacklist=[], whitelist=[]):
    """Get a list of the names of each file in a given directory.

    Ignores directories and hidden files. Default behaviour is to only return
    .json files.

    Args:
        directory: A pathlib Path containing the location of desired files.
        extension: If the file extension should be left on the end of the
            file name or not when returned.
        whitelist: A list of file extensions to search for
        blacklist: A list of file extensions to ignore

    Returns:
        A list containing all the files in the specified directory
            modified according to any flags passed as arguments
    """

    found_files = []
    for file in directory.iterdir():
        fname = Path(file).name
        print(fname)
        if find_json:
            try:
                if file.suffix != ".json":
                    continue

                JSONTopicHandler(file)
            except (json.decoder.JSONDecodeError):
                continue

        if file.is_dir():
            # file is a directory so does not need to be added
            print(f"{fname} is a directory, not adding")
            continue

        if fname[0] == ".":
            # file begins with . denoting hidden status
            continue

        if extension == False:
            # Do not want file extension in string
            fname, discard = fname.split(".")

        found_files.append(fname)

    return found_files


class InvalidKeyError(Exception):
    """An invalid key has been used to access a JSON object.

    Inherits from Exception, essentially used to create a custom key error
    exception where the invalid key is passed as an argument.
    """

    def __init__(self, key, message="Invalid key. Must be 'prompt' or 'answer'"):
        """Initialise exception object with invalid key and a custom message.

        Extends Exception with the key and message attributes.

        Args:
            key: The invalid key that triggered the exception.
            message: The error message that should be displayed to describe the
                exact circumstances of the exception.
                Has a default value to specify that the key value only has two
                correct values; prompt or answer.
        """

        self.key = key
        self.message = message
        super().__init__(self.message)


class JSONHandler:
    """JSON file to be used by FlashCards."""

    def __init__(self, in_filepath):
        """Initialises JSONHandler with the filepath of the JSON file to be used.

        On initialisation the JSON file specified by in_filepath is read and
        stored as a raw string.

        Args:
            in_filepath: The file path for the JSON file to handle.
        """

        self.fpath = in_filepath
        self.fname = Path(in_filepath).name
        self.raw_string = JSONHandler.get_js(in_filepath)

    def output_string(self):
        print(self.raw_string)
        print("String loaded from JSON file: " + self.fname)

    def get_name(self):
        """A bad way of accessing a publicly accessible attribute. Do not use."""

        return self.fname

    @classmethod
    def get_js(cls, fpath):
        try:
            with open(fpath, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # File does not contain valid json or does not exist
            print(f"Invalid file: {fpath}")
            raise
        except FileNotFoundError:
            print(f"File not found. Make one.")
            raise

        return data

    @classmethod
    def make_empty_file(cls, fname):
        empty_file = []
        empty_obj = json.dumps(empty_file, indent=4)

        with open(fname, "w") as f:
            f.write(empty_obj)


class JSONTopicHandler(JSONHandler):
    """A JSON file containing FlashCard topics and prompts.

    Inherits file metadata and the raw string of the JSON file from JSONHandler
    which just acts as a base class.

    Attributes:
        topics
        chosen_topics
        all_prompts
    """

    def __init__(self, filepath):
        """Reads topics and prompts from a specified JSON file.

        Extends the superclass

        Args:
            filepath: The filepath of the FlashCards JSON file to be read.
        """

        super().__init__(filepath)

        self.topics = self.extract_topics()
        self.chosen_topics = []
        self.all_prompts = []

    def set_topic(self, in_topic):
        """Add or remove a topic from the list of chosen topics to be displayed to the user.

        The given string is checked against the chosen_topics attribute and then
        added or removed. If the chosen topic is not a topic from the file then
        nothing will be changed and an error message will be displayed to stdout.

        Args:
            in_topic: The topic to add to chosen_topics.
        """

        modified = False
        if in_topic not in self.chosen_topics:
            for element in self.topics:
                if in_topic == element:
                    self.chosen_topics.append(in_topic)
                    print(in_topic + " added to chosen topics.")
                    modified = True
        else:
            index = self.chosen_topics.index(in_topic)
            del self.chosen_topics[index]
            print(in_topic + " removed from chosen topics.")
            modified = True

        # Provides an error message when attemping to choose invalid topic
        if not modified:
            print("'" + in_topic + "' is an invalid topic string")

    def topic_is_selected(self, check_topic):
        """Check if a topic is selected by the user.

        Args:
            check_topic: A string with the topic name which is being checked.

        Returns:
            A boolean value with the result.
        """

        if check_topic in self.chosen_topics:
            return True
        else:
            return False

    def prompts_from_chosen_topics(self):
        """Returns all the prompts from the chosen_topics.

        Returns:
            A list containing every prompt from the chosen topics. Each element
                is a list of prompts from a specific topic.
        """

        self.all_prompts = []
        for topic in self.chosen_topics:
            self.prompts_from_topic(topic)

        return self.all_prompts

    def prompts_from_topic(self, search_topic, set_all_prompts=True):
        """Finds prompts from a topic in the topic file.

        The default functionality is to modify the class attribute all_prompts
        by adding a new element containing each prompt from the searched topic
        that is stored in the JSON string this object represents. It also returns
        a new list containing all the found prompts

        Args:
            search_topic: A string with the name of the topic you want the prompts
                from.
            set_all_prompts: A flag that changes whether the all_prompts value
                should be modified or not. By default this is set to True to
                preserve older functionality and other uses throughout the program.
                New calls to this method should set this to False unless it is
                necessary.

        Returns: A list of all the prompts that have been found in the search_topic.
        """

        found_prompts = []
        for topics in self.raw_string:
            if topics["topic_name"] == search_topic:
                # found topic
                for prompt in topics["prompts"]:
                    found_prompts.append(prompt)

                    if set_all_prompts:
                        self.all_prompts.append(prompt)

        return found_prompts

    def topic_string(self, modifier=0):
        """Displays topics for debugging/logging purposes."""

        if modifier == 0:
            print("Topics found in file: ")
            for topic in self.topics:
                print("    " + topic)

        print("Topics chosen: ")
        for topic in self.chosen_topics:
            print("    " + topic)

    def print_prompts(self):
        """Displays prompts for debugging/logging purposes."""

        for i in range(self.number_of_prompts()):
            print("Prompt: " + self.get_value(i, "prompt"))
            print("Answer: " + self.get_value(i, "answer"))

    def number_of_prompts(self):
        """Returns the number of prompts stored for use in this object."""

        return len(self.all_prompts)

    def get_value(self, index, key):
        """Get the string from a key/value pair which contains a prompt or answer.

        Args:
            index: The index number to use to access the all_prompts list. This
                number represents which prompt in the list to select the prompt from.
            key: String value which specifies if looking for the prompt or the
                answer to a prompt.
        """
        try:
            if key == "prompt" or key == "answer":
                return self.all_prompts[index][key]
            else:
                raise InvalidKeyError(key)
        except InvalidKeyError:
            return "InvalidKeyError"

    # Generate random numbers within range of length
    def randomise_prompts(self):
        """Randomise the list of prompts that are stored in this object."""

        print("Randomising all_prompts")
        temp_prompts = self.all_prompts
        random_prompts = []
        while len(temp_prompts) > 0:
            rnum = random.randint(0, len(temp_prompts) - 1)
            random_prompts.append(temp_prompts[rnum])
            del temp_prompts[rnum]

        self.all_prompts = random_prompts
        return random_prompts

    def extract_topics(self):
        """Get a list of topics from the JSON topic file.

        Returns:
            A list of strings with the names of the topics contained within the
                file this object represents.
        """

        topics = []
        for topic in self.raw_string:
            topics.append(topic["topic_name"])

        return topics

    def write_new_topic(self, new_topic):
        """Write a new, empty topic to the topic file."""

        # Create the JSON string
        topic_dict = {"topic_name": new_topic, "prompt": []}
        topic_obj = json.dumps(topic_dict, indent=4)

        with open(self.fpath, "w") as f:
            f.write(topic_obj)

    def write_new_prompt(self, new_prompt, topic):
        """Write a new prompt to a given topic in the topic file."""


# TODO: Move these to a separate module
def run_module_tests():
    file_name = "topic.json"
    cwd = Path.cwd()
    file_path = Path.joinpath(cwd, "resources", file_name)
    json_data = JSONHandler(file_path)
    json_data.output_string()

    json_data = JSONTopicHandler(file_path)
    json_data.output_string()

    json_data.set_topic("Ports")
    json_data.set_topic("Ports")
    json_data.set_topic("blah")
    json_data.topic_string()

    json_data.set_topic("Ports")
    json_data.set_topic("Connectors")
    prompts = json_data.prompts_from_chosen_topics()

    print(prompts)
    print("Cycling through all prompts and answers from chosen topic/s!")
    for prompt in prompts:
        print("Prompt: " + prompt["prompt"])
        print("Answer: " + prompt["answer"])
        print("")

    print("get_value test")
    json_data.print_prompts()

    print("Randomiser test")
    json_data.randomise_prompts()
    json_data.print_prompts()

    try:
        json_data.get_value(20, "prompt")
    except IndexError:
        print("There was an exception raised in the method")

    print("Testing file writing.")
    json_data.write_new_topic("test write")


def schema_tests():
    print("****************")
    print("Testing file validation with jsonschema")
    schema = [{"type": "string", "type": [{"type": "string", "type": "string"}]}]
    f = open("validate_file.json")
    test_file = json.load(f)
    jsonschema.validate(test_file, schema)


# If ran as a python script begin running tests that output to console
if __name__ == "__main__":
    run_module_tests()
    # schema_tests()
