# FlashCards - The easier way to study

FlashCards is a program designed to output to the user a series of prompts or questions and then the answer to that prompt or question when the user presses a button.

It has a GUI which allows for selection of topics which the user has input in a corresponding FlashCard file. 

Once the topic(s) have been selected the user will be prompted with a random question from that topic, they can then push a button and the screen will output the answer. The user can then carry on until all the prompts in that topic have been read, they can choose to redo the topic or choose another one.

## JSON Formatting

FlashCards reads data from a JSON file and uses that data to display topics and then prompts and answers from those topics to the user. The "topic.json" file can be modified to provide whatever custom topcis and prompts the user wants to study, however they must be in the right format otherwise FlashCards will not be able to properly interpret the file.

The basic structure of the json file is as such:
```json
[
    {
        "topic_name": "Computers",
        "prompts": [
            {
                "prompt": "How do you turn on a computer?",
                "answer": "Press the power button!"
            },
            {
                "prompt": "What is the best internet browser?",
                "answer": "Firefox!"
            }
        ]
    }
]
```
As far as I know, there is no limit to the number of prompts that can be put into a single topic. Same goes for topics in the file, as many topics can be placed in the file as the user requires. You just need to add your new topic (or replace the old one) with a comma following the curly brackets.

Basically the file consists of a list of dictionaries containing topics and each topic contains another list of dictionaries which contain the prompts and answers for the topic.
```json
[{"topic_name": "First topic", "prompts": [{"prompt": "First prompt", "answer": "First answer"}]}]
```

# To do list - future features and ideas
* File selection

   FlashCards currently only supports reading from a single file that is located in the same directory as main_app.py. The file must be called "topic.json". It should be possible for the user to create their own JSON files and select them from any location they choose.
* User input checking

   Answer checking could be included and would take simple input (eg, one or two word answers, single numbers, match single words from a sentence).