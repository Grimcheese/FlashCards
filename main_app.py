# Module that defines the GUI elements of FlashCards
import tkinter as tk

from handle_json import JSONHandler
from handle_json import JSONTopicHandler

class BasicFrame():
    def __init__(self, parent):
        self.base_frame = tk.Frame(master = parent)

    def show(self):
        self.base_frame.grid()
        
    def remove(self):
        self.base_frame.grid_remove()

class IntroFrame(BasicFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.intro_label = None

        self.build_intro_screen()

    def build_intro_screen(self):
        gui_reference_data = JSONHandler.get_js("gui_reference.json")

        self.intro_label = tk.Label(master = self.base_frame, text = gui_reference_data["intro_frame"][0]["main_text"])
        self.intro_label.grid(column = 0, row = 0)

class TopicSelectFrame(BasicFrame):
    def __init__(self, parent, main_app, in_file):
        super().__init__(parent)

        self.top_label = None
        self.topic_buttons = []
        self.chosen_topic_labels = []
        self.next_screen_button = None
        self.back_to_start_button = None

        self.topic_file = in_file
        
        self.chosen_topics = []

        self.build_topic_select_screen(main_app)

    def build_topic_select_screen(self, main_app):
        self.top_label = tk.Label(master = self.base_frame, text = "Topics from file: ")
        self.top_label.grid(column = 0, row = 1)

        self.next_screen_button = tk.Button(master = self.base_frame, text = "Run prompts from selected topic",
                                                command = lambda: main_app.start_prompts(),
                                                state = tk.DISABLED)

        self.back_to_start_button = tk.Button(master = self.base_frame, 
                                                text = "Back to intro!", 
                                                command = lambda: main_app.update_current_screen(0, main_app.current_screen))
        self.back_to_start_button.grid(column = 0, row = 0)
        
        topic_row = self.make_topic_buttons()
        self.next_screen_button.grid(column = 0, row = topic_row + 1)

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
    def __init__(self, parent, main_app, file_obj):
        super().__init__(parent)

        self.topic_file = file_obj
        self.prompt_index = 0
        self.showing_prompt = False
        self.end_of_prompts = False

        self.top_label = None
        self.return_to_start_button = None
        self.return_to_topic_select_button = None
        self.back_button = None

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
                                                    command = lambda: main_app.update_current_screen(0, main_app.current_screen))
        self.return_to_start_button.grid(column = 0, row = 0)
        self.return_to_topic_select_button = tk.Button(master = self.base_frame, text = "Return to topic select",
                                                        command = lambda: main_app.update_current_screen(1, main_app.current_screen))
        self.return_to_topic_select_button.grid(column = 1, row = 0)

        self.top_label = tk.Label(master = self.base_frame, text = "Running through prompts!")
        self.top_label.grid(column = 2, row = 0)

        self.back_button = tk.Button(master = self.base_frame, text = "Go back a prompt",
                                        command = self.back)
        self.back_button.grid(column = 3, row = 0)

        self.prompt_label = tk.Label(master = self.base_frame, text = "", width = 22, wraplength = 100)
        self.prompt_label.grid(column = 2, columnspan = 2, row = 2)
        self.answer_label = tk.Label(master = self.base_frame, text = "")
        self.answer_label.grid(column = 3, row = 3)

        self.user_answer = tk.Entry(master = self.base_frame)
        self.user_answer.grid(column = 2, row = 3)

    def back(self):
        print("Going back to last prompt")
        print("Current index number: " + str(self.prompt_index))
        if self.prompt_index > 0:
            self.prompt_index = self.prompt_index - 1
            self.prompt_labels_update(self.topic_file.get_value(self.prompt_index, "prompt"),
                                        self.topic_file.get_value(self.prompt_index, "answer"))
            

    def next(self):
        if self.prompt_index < self.topic_file.number_of_prompts():
            if self.showing_prompt:
                self.answer_label.config(text = self.topic_file.get_value(self.prompt_index, "answer"))
                self.showing_prompt = False
                self.prompt_index += 1
            else:
                self.answer_label.config(text = "")
                self.prompt_label.config(text = self.topic_file.get_value(self.prompt_index, "prompt"))
                self.showing_prompt = True
        else:
            self.prompt_label.config(text = "Out of prompts! Press Enter to return to start...")
            self.answer_label.config(text = "")
            self.end_of_prompts = True

        print(self.prompt_index)
    
    def prompt_labels_update(self, prompt, answer):
        self.prompt_label.config(text = prompt)
        self.answer_label.config(text = answer)

    def show(self):
        self.topic_file.prompts_from_chosen_topics()
        self.topic_file.randomise_prompts()

        super().show()

    def remove(self):
        self.prompt_index = 0
        self.showing_prompt = False
        self.prompt_labels_update("", "")
        
        super().remove()



class MainApp:
    def __init__(self, parent, name = None):
        self.main_window = parent
        self.current_screen = 0

        self.topic_file = JSONTopicHandler("topic.json")

        self.intro_frame = IntroFrame(self.main_window)
        self.topic_select_frame = TopicSelectFrame(self.main_window, self, self.topic_file)
        self.display_prompts_frame = DisplayPrompts(self.main_window, self, self.topic_file)        

        self.update_current_screen(0)

        self.set_callbacks()

    # Will change the current screen that is displayed on the main_window.
    # WARNING - If no current_screen is entered (no argument passed) no screen will be unpacked
    def update_current_screen(self, new_screen, current_screen = -1):
        # Unpack/destroy current frame in prep for building next frame

        if current_screen == 0:
            self.intro_frame.remove()
        elif current_screen == 1:
            self.topic_select_frame.remove()
        elif current_screen == 2:
            self.display_prompts_frame.remove()

        # Builds the next frame
        if new_screen == 0:
            self.intro_frame.show()
            self.current_screen = new_screen
            self.clear_instance()
        elif new_screen == 1:
            self.topic_select_frame.show()
            self.current_screen = new_screen
        elif new_screen == 2:
            self.display_prompts_frame.show()
            self.current_screen = new_screen

        if current_screen == -1:
            print("No previous screen, no screen unpacked.")

    def clear_instance(self):
        del self.topic_select_frame
        del self.display_prompts_frame
        del self.topic_file

        self.topic_file = JSONTopicHandler("topic.json")
        self.topic_select_frame = TopicSelectFrame(self.main_window, self, self.topic_file)
        self.display_prompts_frame = DisplayPrompts(self.main_window, self, self.topic_file)
    
    def set_callbacks(self):
        def handle_callbacks(event, self = self):
            if self.current_screen == 0:
                self.update_current_screen(1, self.current_screen)
                print("Any key pressed")
            elif self.current_screen == 2 and (event.keysym == "Return" or event.keysym == "Right"):
                next_display_prompt_callback(event, self)
            elif self.current_screen == 2 and event.keysym == "Left":
                self.display_prompts_frame.back()
        
        def next_display_prompt_callback(event, self = self):
            if self.current_screen == 2:
                if self.display_prompts_frame.end_of_prompts is False:
                    self.display_prompts_frame.next()
                else:
                    self.update_current_screen(0, self.current_screen)

        self.main_window.bind("<Any-Key>", handle_callbacks) # Will trigger while any frame is up - perform check in callback method
        self.main_window.bind("<Any-Button>", handle_callbacks)


    def start_prompts(self):
        self.update_current_screen(2, self.current_screen)

    


if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("FlashCards! - The best way to study-")
    main_window.geometry("800x600")
    main_window.resizable(False, False)

    app = MainApp(main_window)

    main_window.mainloop()

