# Module that defines the GUI elements of FlashCards
import tkinter as tk
import json

from handle_json import JSONHandler

class MainApp:
    def __init__(self, parent, name = None):
        self.main_window = parent
        self.current_screen = 0

        self.intro_frame = tk.Frame(master = self.main_window)
        self.topic_select_frame = tk.Frame(master = self.main_window)

        self.initalise_screens()
        self.update_current_screen(0)

    # Will change the current screen that is display.
    # WARNING - If no current_screen is entered (no argument passed) no screen will be unpacked
    def update_current_screen(self, new_screen, current_screen = -1):
        # Unpack/destroy current frame in prep for building next frame

        if current_screen == 0:
            self.intro_frame.grid_remove()
        elif current_screen == 1:
            self.topic_select_frame.grid_remove()

        # Builds the next frame
        if new_screen == 0:
            self.intro_frame.grid()
            self.current_screen = new_screen
        elif new_screen == 1:
            self.topic_select_frame.grid()
            self.current_screen = new_screen

        if current_screen == -1:
            print("No previous screen, no screen unpacked.")
        
        self.set_callbacks()
    
    def set_callbacks(self):
        def handle_intro_callbacks(event, self = self):
            if self.current_screen == 0:
                self.update_current_screen(1, self.current_screen)
                print("Any key pressed")

        self.main_window.bind("<Any-Key>", handle_intro_callbacks) # Will trigger while any frame is up - perform check in callback method

    # Builds all the screens/widgets but does not place them onto the main_window
    def initalise_screens(self):
        self.build_intro_screen()
        self.build_topic_select_screen()

    def build_intro_screen(self):
        f = open("gui_reference.json")
        data = json.load(f)

        self.intro_label = tk.Label(master = self.intro_frame, text = data["intro_frame"][0]["main_text"])
        self.intro_label.grid(column = 0, row = 0)



    def build_topic_select_screen(self):
        self.top_label = tk.Label(master = self.topic_select_frame, text = "Choose a topic: ")
        self.top_label.grid(column = 0, row = 1)

        self.back_to_start_button = tk.Button(master = self.topic_select_frame, text = "Back to intro!", command = lambda: self.update_current_screen(0, self.current_screen))
        self.back_to_start_button.grid(column = 0, row = 0)

if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("FlashCards! - The best way to study-")
    main_window.geometry("800x600")
    main_window.resizable(False, False)

    app = MainApp(main_window)

    main_window.mainloop()

