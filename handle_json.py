import json
import random

class InvalidKeyError(Exception):
    def __init__(self, key, message = "Invalid key. Must be 'prompt' or 'answer'"):
        self.key = key
        self.message = message
        super().__init__(self.message)

class JSONHandler():
    def __init__(self, filename):
        self.fname = f
        self.raw_string = JSONHandler.get_js(self.fname)
        self.prompts = self.extract_prompts()

    # Gets a value from the key/value pair as specified
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
        temp_prompts = prompts
        random_prompts = []
        while len(temp_prompts) > 0:
            rnum = randint(0, len(temp_prompts) - 1)
            random_prompts.append(temp_prompts[rnum])
            del temp_prompts[rnum]

        return random_prompts

        



    # Returns all the prompts from the JSON file as a tuple.
    # prompt_pairs[prompt][answer]
    def extract_prompts(self):
        prompts = []
        for prompt_pair in self.raw_string["prompts"]:
            prompts.append(prompt_pair)

        return prompts

    
    @classmethod
    def get_js(cls, fname):
        f = open(fname)
        data = json.load(f)

        return data
