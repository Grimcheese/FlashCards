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

    def output_string(self):
        print(self.raw_string)
        print("String loaded from JSON file: " + self.fname)

    @classmethod
    def get_js(cls, fname):
        f = open(fname)
        data = json.load(f)

        return data

class JSONTopicHandler(JSONHandler):

    def __init__(self, filename):
        super().__init__(filename)

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
                    selected = True
        else:
            index = self.chosen_topics.index(in_topic)
            del self.chosen_topics[index]
            print(in_topic + " removed from chosen topics.")
            modified = True
            selected = False
        
        if not modified:
            print("'" + in_topic + "' is an invalid topic string")
            selected = False
        
        return selected
    
    def prompts_from_chosen_topics(self):
        self.all_prompts = []
        for topic in self.chosen_topics:
            self.prompts_from_topic(topic)

        return self.all_prompts
    
    def prompts_from_topic(self, search_topic):
        for topics in self.raw_string:
            if topics["topic_name"] == search_topic:
                #found topic
                for prompt in topics["prompts"]:
                    self.all_prompts.append(prompt)


    def topic_string(self, modifier = 0):
        if modifier == 0:
            print("Topics found in file: ")
            for topic in self.topics:
                print("    " + topic)
            
        print("Topics chosen: ")
        for topic in self.chosen_topics:
            print("    " + topic)
    
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

def run_module_tests():
    json_data = JSONHandler("topic.json")
    json_data.output_string()

    json_data = JSONTopicHandler("topic.json")
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
    for i in range(len(prompts)):
        print("Prompt: " + json_data.get_value(i, "prompt"))
        print("Answer: " + json_data.get_value(i, "answer"))

if __name__ == "__main__":
    run_module_tests()
    

