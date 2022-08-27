# Module that defines the GUI elements of FlashCards
import tkinter as tk
import json

from handle_json import JSONHandler
from handle_json import JSONTopicHandler

from pathlib import Path

class BasicFrame():
    def __init__(self, parent):
        self.base_frame = tk.Frame(master = parent)

    def show(self):
        self.base_frame.grid()
        
    def remove(self):
        self.base_frame.grid_remove()

class IntroFrame(BasicFrame):
    S_INDEX = "intro_frame"
    def __init__(self, parent):
        super().__init__(parent)
        self.intro_label = None

        self.build_intro_screen()

    def build_intro_screen(self):
        gui_reference_data = JSONHandler.get_js("gui_reference.json")

        self.intro_label = tk.Label(master = self.base_frame, text = gui_reference_data["intro_frame"][0]["main_text"])
        self.intro_label.grid(column = 0, row = 0)

class ChooseFileFrame(BasicFrame):
    S_INDEX = "choose_file_frame"
    def __init__(self, main_app):
        super().__init__(main_app.main_window)

        self.chosen_file = main_app.topic_file

        self.found_files = []
        self.files_display = []

        self.main_label = None
        self.previous_frame_button = None
        self.next_frame_button = None

        self.build_choose_file_frame(main_app)

    def build_choose_file_frame(self, main_app):
        self.main_label = tk.Label(master = self.base_frame, text = "Choose file to read topics/prompts from: ")
        self.main_label.grid(column = 0, row = 1)

        self.previous_frame_button = tk.Button(master = self.base_frame, text = "Go back.",
            command = lambda: main_app.update_current_screen(main_app.intro_frame.S_INDEX, main_app.current_screen))
        self.previous_frame_button.grid(column = 0, row = 0)
        self.next_frame_button = tk.Button(master = self.base_frame, text = "Choose: '" + main_app.topic_file.get_name() + "'",
            command = lambda: self.to_topic_select(main_app))
        self.next_frame_button.grid(column = 1, row = 0)
        
        self.show_files()

    def to_topic_select(self, main_app):
        main_app.topic_file = self.chosen_file
        main_app.topic_select_frame = TopicSelectFrame(main_app)
        main_app.update_current_screen(main_app.topic_select_frame.S_INDEX, main_app.current_screen)

    def show_files(self):
        rsrc_dir = Path(MainApp.CWD, MainApp.RESOURCES_DIR)
        
        file_index = 0
        for file in rsrc_dir.iterdir():
            # Check each file supports FlashCards format
            try:
                self.found_files.append(JSONTopicHandler(file))
                self.found_files.append(file)
                file_name = Path(file).name
                self.files_display.append(tk.Button(master = self.base_frame, text = file_name,
                        command = lambda file = file: self.pick_file(file)))
                self.files_display[file_index].grid(column = 3, row = file_index + 2)

                file_index += 1
            except json.decoder.JSONDecodeError:
                print("Not a valid FlashCards file")

    def pick_file(self, f_path):
        new_file = JSONTopicHandler(f_path)
        self.chosen_file = new_file
        print("Picking file: " + new_file.get_name())

        self.next_frame_button.config(text = "Choose: '" + new_file.get_name() + "'")


class TopicSelectFrame(BasicFrame):
    S_INDEX = "topic_select_frame"
    def __init__(self, main_app):
        super().__init__(main_app.main_window)

        self.top_label = None
        self.topic_buttons = []
        self.chosen_topic_labels = []
        self.next_screen_button = None
        self.previous_frame_button = None

        self.topic_file = main_app.topic_file
        
        self.chosen_topics = []

        self.build_topic_select_screen(main_app)

    def build_topic_select_screen(self, main_app):
        self.top_label = tk.Label(master = self.base_frame, text = "Topics from file: ")
        self.top_label.grid(column = 0, row = 1)

        self.next_screen_button = tk.Button(master = self.base_frame, text = "Run prompts from selected topic/s",
                    command = lambda: self.to_display_prompts_frame(main_app),
                    state = tk.DISABLED)

        self.previous_frame_button = tk.Button(master = self.base_frame, 
                    text = "Back to file selection.", 
                    command = lambda: main_app.update_current_screen(main_app.choose_file_frame.S_INDEX, main_app.current_screen))
        self.previous_frame_button.grid(column = 0, row = 0)
        
        topic_row = self.make_topic_buttons()
        self.next_screen_button.grid(column = 0, row = topic_row + 1)
    
    def to_display_prompts_frame(self, main_app):
        main_app.display_propmts_frame = DisplayPrompts(main_app)
        main_app.update_current_screen(main_app.display_prompts_frame.S_INDEX, main_app.current_screen)

    def make_topic_buttons(self):
        topic_row = 1
        for topic in self.topic_file.topics:
            self.topic_buttons.append(tk.Button(master = self.base_frame, 
                                            text = topic, 
                                            justify = tk.LEFT, 
                                            wraplength = 145,
                                            width = 20,
                                            command = lambda topic = topic: self.pick_topics(topic)))
            
            self.chosen_topic_labels.append(tk.Label(master = self.base_frame, text = ""))
            self.update_picked_topics_label(topic)

            self.topic_buttons[topic_row - 1].grid(column = 1, row = topic_row, sticky = tk.W)
            self.chosen_topic_labels[topic_row - 1].grid(column = 2, row = topic_row)
            topic_row += 1

        return topic_row

    def pick_topics(self, selected_topic):
        print("You have selected: " + selected_topic)
        self.topic_file.set_topic(selected_topic)

        self.update_picked_topics_label(selected_topic)

    def update_picked_topics_label(self, selected_topic):
        topic_label_index = self.topic_file.topics.index(selected_topic)
        is_selected = self.topic_file.topic_is_selected(selected_topic)
        if is_selected:
            self.chosen_topic_labels[topic_label_index].config(text = "Picked")
        else:
            self.chosen_topic_labels[topic_label_index].config(text = "")
        
        if len(self.topic_file.chosen_topics) == 0:
            print("Next screen button disabled")
            self.next_screen_button.config(state = tk.DISABLED)
        else:
            print("Next screen button activated")
            self.next_screen_button.config(state = tk.ACTIVE)
        
        self.topic_file.topic_string(1)

class DisplayPrompts(BasicFrame):
    S_INDEX = "display_prompts_frame"
    def __init__(self, main_app):
        super().__init__(main_app.main_window)

        self.topic_file = main_app.topic_file
        self.prompt_index = 0
        self.showing_answer = False
        self.end_of_prompts = False

        self.top_label = None
        self.return_to_start_button = None
        self.return_to_topic_select_button = None
        self.back_button = None
        self.start_prompts = None

        self.prompt_label = None
        self.answer_label = None
        self.user_answer = None

        self.build_run_prompts_screen(main_app)
    
    def checkfile(self):
        self.topic_file.topic_string()
        print("Number of prompts: " + str(self.topic_file.number_of_prompts()))
        for i in range(self.topic_file.number_of_prompts()):
            print(self.topic_file.get_value(i, "prompt"))


    def build_run_prompts_screen(self, main_app):
        self.return_to_start_button = tk.Button(master = self.base_frame, text = "Return to start screen", 
                    command = lambda: main_app.update_current_screen(main_app.intro_frame.S_INDEX, main_app.current_screen))
        self.return_to_start_button.grid(column = 0, row = 0)
        self.return_to_topic_select_button = tk.Button(master = self.base_frame, text = "Return to topic select",
                    command = lambda: main_app.update_current_screen(main_app.topic_select_frame.S_INDEX, main_app.current_screen))
        self.return_to_topic_select_button.grid(column = 1, row = 0)

        self.top_label = tk.Label(master = self.base_frame, text = "Running through prompts!")
        self.top_label.grid(column = 2, row = 0)

        self.back_button = tk.Button(master = self.base_frame, text = "Go back a prompt",
                                        command = self.previous_prompt)
        self.back_button.grid(column = 3, row = 0)

        self.prompt_label = tk.Label(master = self.base_frame, text = "", width = 22, wraplength = 100)
        self.prompt_label.grid(column = 2, columnspan = 2, row = 2)
        self.answer_label = tk.Label(master = self.base_frame, text = "")
        self.answer_label.grid(column = 3, row = 3)

        self.start_prompts_button = tk.Button(master = self.base_frame, text = "Begin running through prompts",
                                        command = self.show_first_prompt)
        self.start_prompts_button.grid(column = 4, row = 0)

        self.counter_label = tk.Label(master = self.base_frame, text = "")
        self.counter_label.grid(column = 4, row = 0)

    def show_first_prompt(self):
        self.prompt_labels_update(self.topic_file.get_value(0, "prompt"))
        self.start_prompts_button.grid_remove()
        self.start_prompts_button.config(state = tk.DISABLED)

    def previous_prompt(self):
        if self.prompt_index > 0:
            self.prompt_index = self.prompt_index - 1
            self.prompt_labels_update(self.topic_file.get_value(self.prompt_index, "prompt"),
                                        self.topic_file.get_value(self.prompt_index, "answer"))
            self.end_of_prompts = False
            
            print("Going back to last prompt")
            print("Current index number: " + str(self.prompt_index))

    def goto_next_prompt(self):
        print("Current index: " + str(self.prompt_index))
        try:
            if self.showing_answer:
                print("Updating prompt label")
                self.next_prompt()
            else:
                print("Updating answer label ")
                self.prompt_labels_update(answer = self.topic_file.get_value(self.prompt_index, "answer"))
        except IndexError:
            self.prompt_labels_update(prompt = "Out of prompts! Press Enter to return to start...", answer = "")
            self.end_of_prompts = True


    def next_prompt(self):
        self.prompt_index = self.prompt_index + 1
        self.prompt_labels_update(prompt = self.topic_file.get_value(self.prompt_index, "prompt"),
                                    answer = "")
            

    def prompt_labels_update(self, prompt = None, answer = None):
        if prompt is not None:
            self.prompt_label.config(text = prompt)
        if answer is not None:
            self.answer_label.config(text = answer)
            if answer == "":
                self.showing_answer = False
                print("Not showing answer")
            else:
                self.showing_answer = True
                print("Showing answer")
        self.update_counter()
    
    def update_counter(self):
        num_prompts = self.topic_file.number_of_prompts()
        if self.prompt_index < num_prompts:
            count_val = str(self.prompt_index + 1) + " / " + str(num_prompts)
            self.counter_label.config(text = count_val)
        else:
            self.counter_label.config(text = "")

    def show(self, chosen_file):
        self.topic_file = chosen_file
        self.topic_file.prompts_from_chosen_topics()
        self.topic_file.randomise_prompts()

        self.topic_file.print_prompts()
        self.show_first_prompt()

        super().show()

    def remove(self):
        self.prompt_index = 0
        self.showing_prompt = False
        self.prompt_labels_update("", "")
        
        super().remove()

class MainApp:
    CWD = Path.cwd()
    RESOURCES_DIR = "resources"
    default_file_path = Path.joinpath(CWD, RESOURCES_DIR, "topic.json")

    def __init__(self, parent, name = None):
        self.main_window = parent
        self.current_screen = "intro_frame"

        self.topic_file = JSONTopicHandler(MainApp.default_file_path)

        self.intro_frame = IntroFrame(self.main_window)
        self.choose_file_frame = ChooseFileFrame(self)
        self.topic_select_frame = TopicSelectFrame(self)
        self.display_prompts_frame = DisplayPrompts(self)        

        self.update_current_screen(self.intro_frame.S_INDEX)

        self.set_callbacks()

    # Will change the current screen that is displayed on the main_window.
    # WARNING - If no current_screen is entered (no argument passed) no screen will be unpacked
    def update_current_screen(self, new_screen, current_screen = None):
        # Unpack/destroy current frame in prep for building next frame
        print("Current screen is: " + self.current_screen)

        if current_screen == "intro_frame":
            self.intro_frame.remove()
        elif current_screen == "topic_select_frame":
            self.topic_select_frame.remove()
        elif current_screen == "display_prompts_frame":
            self.display_prompts_frame.remove()
        elif current_screen == "choose_file_frame":
            self.choose_file_frame.remove()

        # Builds the next frame
        if new_screen == "intro_frame":
            self.intro_frame.show()
            self.current_screen = new_screen
            self.clear_instance()
        elif new_screen == "topic_select_frame":
            self.topic_select_frame.show()
            self.current_screen = new_screen
        elif new_screen == "display_prompts_frame":
            self.display_prompts_frame.show(self.topic_file)
            self.current_screen = new_screen
        elif new_screen == "choose_file_frame":
            self.choose_file_frame.show()
            self.current_screen = new_screen

        if current_screen == None:
            print("No previous screen, no screen unpacked.")

    def clear_instance(self):
        del self.choose_file_frame
        del self.topic_select_frame
        del self.display_prompts_frame
        del self.topic_file

        self.topic_file = JSONTopicHandler(MainApp.default_file_path)
        self.choose_file_frame = ChooseFileFrame(self)
        self.topic_select_frame = TopicSelectFrame(self)
        self.display_prompts_frame = DisplayPrompts(self)
    
    def set_callbacks(self):
        def handle_callbacks(event, self = self):
            if self.current_screen == "intro_frame":
                self.update_current_screen(self.choose_file_frame.S_INDEX, self.current_screen)
                print("Any key pressed")
            elif self.current_screen == "display_prompts_frame" and (event.keysym == "Return" or event.keysym == "Right"):
                next_display_prompt_callback(event, self)
            elif self.current_screen == "display_prompts_frame" and event.keysym == "Left":
                self.display_prompts_frame.previous_prompt()
        
        def next_display_prompt_callback(event, self = self):
            if self.display_prompts_frame.end_of_prompts is False:
                self.display_prompts_frame.goto_next_prompt()
            elif self.display_prompts_frame.end_of_prompts is True and event.keysym == "Return":
                self.update_current_screen(self.intro_frame.S_INDEX, self.current_screen)

        self.main_window.bind("<Any-Key>", handle_callbacks) # Will trigger while any frame is up - perform check in callback method
        self.main_window.bind("<Any-Button>", handle_callbacks)

if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("FlashCards! - The best way to study-")
    main_window.geometry("800x600")
    main_window.resizable(False, False)

    app = MainApp(main_window)

    main_window.mainloop()

