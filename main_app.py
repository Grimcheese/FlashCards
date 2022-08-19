# Module that defines the GUI elements of FlashCards
import tkinter as tk
import json

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
    def __init__(self, parent, main_app):
        super().__init__(parent)

        self.top_label = None
        self.topic_buttons = []
        self.chosen_topic_labels = []
        self.next_screen_button = None
        self.back_to_start_button = None

        self.chosen_topics = []

        self.build_topic_select_screen(main_app)

    def build_topic_select_screen(self, main_app):
        topic_row = self.make_topic_buttons()
        
        self.top_label = tk.Label(master = self.base_frame, text = "Topics from file: ")
        self.top_label.grid(column = 0, row = 1)

        self.next_screen_button = tk.Button(master = self.base_frame, text = "Run prompts from selected topic",
                                                command = lambda: main_app.start_prompts())
        self.next_screen_button.grid(column = 0, row = topic_row + 1)

        self.back_to_start_button = tk.Button(master = self.base_frame, 
                                                text = "Back to intro!", 
                                                command = lambda: main_app.update_current_screen(0, main_app.current_screen))
        self.back_to_start_button.grid(column = 0, row = 0)

    def make_topic_buttons(self):
        topic_file = JSONTopicHandler("topic.json")
        print("Topics in file: ")
        topic_file.topic_string()
        
        topic_row = 1
        for topic in topic_file.topics:
            self.topic_buttons.append(tk.Button(master = self.base_frame, 
                                            text = topic, 
                                            justify = tk.LEFT, 
                                            wraplength = 145,
                                            width = 20,
                                            command = lambda topic = topic: self.pick_topics(topic, topic_file)))
            
            self.chosen_topic_labels.append(tk.Label(master = self.base_frame, text = ""))

            self.topic_buttons[topic_row - 1].grid(column = 1, row = topic_row, sticky = tk.W)
            self.chosen_topic_labels[topic_row - 1].grid(column = 2, row = topic_row)
            topic_row += 1

        return topic_row

    def pick_topics(self, topic, topic_file):
        i = 0
        print("You have selected: " + topic)
        for element in topic_file.topics:
            if element == topic:
                break
            else:
                i = i + 1
        
        if topic in self.chosen_topics:
            index = self.chosen_topics.index(topic)
            del self.chosen_topics[index]
            self.chosen_topic_labels[i].config(text = "")
        else:
            self.chosen_topics.append(topic)
            self.chosen_topic_labels[i].config(text = "Picked")

        print(self.chosen_topics)

class DisplayPrompts(BasicFrame):
    def __init__(self, parent, main_app):
        super().__init__(parent)

        self.top_label = None
        self.return_to_start_button = None

        self.build_run_prompts_screen(main_app)

    def build_run_prompts_screen(self, main_app):
        self.return_to_start_button = tk.Button(master = self.base_frame, text = "Return to start screen", 
                                                    command = lambda: main_app.update_current_screen(0, main_app.current_screen))
        self.return_to_start_button.grid(column = 0, row = 0)

        self.top_label = tk.Label(master = self.base_frame, text = "Running through prompts!")
        self.top_label.grid(column = 1, row = 0)


class MainApp:
    def __init__(self, parent, name = None):
        self.main_window = parent
        self.current_screen = 0

        self.intro_frame = IntroFrame(self.main_window)
        self.topic_select_frame = TopicSelectFrame(self.main_window, self)
        self.display_prompts_frame = DisplayPrompts(self.main_window, self)        

        self.update_current_screen(0)

        self.set_callbacks()

    # Will change the current screen that is display.
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
            self.clear_vals()
        elif new_screen == 1:
            self.topic_select_frame.show()
            self.current_screen = new_screen
        elif new_screen == 2:
            self.display_prompts_frame.show()
            self.current_screen = new_screen

        if current_screen == -1:
            print("No previous screen, no screen unpacked.")

    def clear_vals(self):
        self.topic_select_frame = TopicSelectFrame(self.main_window, self)
        self.display_prompts_frame = DisplayPrompts(self.main_window, self)
    
    def set_callbacks(self):
        def handle_intro_callbacks(event, self = self):
            if self.current_screen == 0:
                self.update_current_screen(1, self.current_screen)
                print("Any key pressed")

        self.main_window.bind("<Any-Key>", handle_intro_callbacks) # Will trigger while any frame is up - perform check in callback method
        self.main_window.bind("<Any-Button>", handle_intro_callbacks)

    def start_prompts(self):
        self.update_current_screen(2, self.current_screen)

    


if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("FlashCards! - The best way to study-")
    main_window.geometry("800x600")
    main_window.resizable(False, False)

    app = MainApp(main_window)

    main_window.mainloop()

