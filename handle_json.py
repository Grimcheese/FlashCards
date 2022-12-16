"""Module for FlashCards App that provides JSON support.

Classes:
    JSONHandler
    JSONTopicHandler
    InvalidKeyError
"""

import json
import jsonschema
import random

from pathlib import Path


class InvalidKeyError(Exception):
    """An invalid key has been used to access a JSON object.

    Inherits from Exception, essentially used to create a custom key error
    exception where the invalid key is passed as an argument."""

    def __init__(self, key, message="Invalid key. Must be 'prompt' or 'answer'"):
        """Initialise exception object with invalid key and a custom message.

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
    """Base class for storing a JSON file to be used by FlashCards."""

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
        return self.fname

    @classmethod
    def get_js(cls, fname):
        f = open(fname)
        data = json.load(f)

        return data


class JSONTopicHandler(JSONHandler):
    """Extends JSON file capabilities from JSONHandler for reading FlashCard topics.

    Attributes:
        set_topic(in_topic)
        topic_is_selected(check_topic)
        prompts_from_chosen_topics()
        prompts_from_topic(search_topic)
        print_prompts()
        number_of_prompts()

        topics
        chosen_topics
        all_prompts
    """

    def __init__(self, filepath):
        """Reads topics and prompts from a specified JSON file.

        Args:
            filepath: The filepath of the FlashCards JSON file to be read.
        """

        super().__init__(filepath)

        self.topics = self.extract_topics()
        self.chosen_topics = []
        self.all_prompts = []

    def set_topic(self, in_topic):
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

        if not modified:
            print("'" + in_topic + "' is an invalid topic string")

    def topic_is_selected(self, check_topic):
        if check_topic in self.chosen_topics:
            return True
        else:
            return False

    def prompts_from_chosen_topics(self):
        self.all_prompts = []
        for topic in self.chosen_topics:
            self.prompts_from_topic(topic)

        return self.all_prompts

    def prompts_from_topic(self, search_topic):
        for topics in self.raw_string:
            if topics["topic_name"] == search_topic:
                # found topic
                for prompt in topics["prompts"]:
                    self.all_prompts.append(prompt)

    def topic_string(self, modifier=0):
        if modifier == 0:
            print("Topics found in file: ")
            for topic in self.topics:
                print("    " + topic)

        print("Topics chosen: ")
        for topic in self.chosen_topics:
            print("    " + topic)

    def print_prompts(self):
        for i in range(self.number_of_prompts()):
            print("Prompt: " + self.get_value(i, "prompt"))
            print("Answer: " + self.get_value(i, "answer"))

    def number_of_prompts(self):
        return len(self.all_prompts)

    # Gets a value from the key/value pair as specified
    # Must specify "prompt" or "answer"
    def get_value(self, index, key):
        try:
            if key == "prompt" or key == "answer":
                return self.all_prompts[index][key]
            else:
                raise InvalidKeyError(key)
        except InvalidKeyError:
            return "InvalidKeyError"

    # Generate random numbers within range of length
    def randomise_prompts(self):
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
        topics = []
        for topic in self.raw_string:
            topics.append(topic["topic_name"])

        return topics


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
