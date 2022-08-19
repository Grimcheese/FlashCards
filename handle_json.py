import json
import random

class InvalidKeyError(Exception):
    def __init__(self, key, message = "Invalid key. Must be 'prompt' or 'answer'"):
        self.key = key
        self.message = message
        super().__init__(self.message)

class JSONHandler():
    def __init__(self, filename):
        self.fname = filename
        self.raw_string = JSONHandler.get_js(self.fname)

    @classmethod
    def get_js(cls, fname):
        f = open(fname)
        data = json.load(f)

        return data

class JSONTopicHandler(JSONHandler):

    def __init__(self, filename):
        super().__init__(filename)

        self.topics = self.extract_topics()
        self.prompts = []

    def topic_string(self):
        for topic in self.topics:
            print(topic)

    # Gets a value from the key/value pair as specified
    # Must specify "prompt" or "answer"
    def get_value(self, index, key):
        try:
            if key == "prompt" or key == "answer":
                return self.prompts[index][key]
            else:
                raise InvalidKeyError(key)
        except InvalidKeyError:
            return "Invalid Key"
        except IndexError:
            print("Index out of bounds error")
            return "IndexError"
    
    # Generate random numbers within range of length
    def randomise_prompts(self):
        temp_prompts = self.prompts
        random_prompts = []
        while len(temp_prompts) > 0:
            rnum = random.randint(0, len(temp_prompts) - 1)
            random_prompts.append(temp_prompts[rnum])
            del temp_prompts[rnum]

        return random_prompts

    def extract_topics(self):
        topics = []
        for topic in self.raw_string:
            topics.append(topic["topic_name"])
        
        return topics


