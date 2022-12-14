# Version Info - Important
Please note that this program is still in the early stages of development and only has basic features implemented so far. The UI is functional, that is all. There are also going to be lots of bugs and input/output issues. Consider everything at this stage to be a placeholder.

# FlashCards - The easier way to study

FlashCards is a program designed to output to the user a series of prompts or questions and then the answer to that prompt or question when the user presses a button.

It has a GUI which allows for selection of topics which the user has input in a corresponding JSON file. 

Once the topic(s) have been selected the user will be prompted with a random question from that topic, they can then push a button and the screen will output the answer. The user can then carry on until all the prompts in that topic have been read, they can choose to redo the topic or choose another one.

## JSON Formatting
FlashCards currently only supports reading data from "topic.json" file in the main directory.

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
[{"topic_name": "First topic", "prompts": [{"prompt": "First prompt for first topic", "answer": "First answer for first topic"}]}, {"topic_name": "Second topic", "prompts": [{"prompts": "First prompt for second topic", "answer": "First answer for second topic"}]}]
```

# To do list - future features and ideas
* UI Upgrade/Overhaul

   At this stage FlashCards has a very basic UI with no colours or any thought put into making it a program easy and pleasant to use. When all of the main features have been implemented and work as expected work should begin on making the program look nice: use different colours, button and label placement through the app, advanced keybindings... but most important is some sort of consistent theme and layout. Without such the app is basically useless.

* File selection

   FlashCards currently only supports reading from a single file that is located in the same directory as main_app.py. The file must be called "topic.json". It should be possible for the user to create their own JSON files and select them from any location they choose.

* User input checking

   Answer checking could be included and would take simple input (eg, one or two word answers, single numbers, match single words from a sentence). Currently there is an entry box that allows for user input but there is no checking provided.

* Creation of topic json files from within FlashCards

   It should be possible for the user to create new topics and prompts from within the app rather than having to manually edit the JSON file. 