# Module that defines the GUI elements of FlashCards
import tkinter as tk

class MainApp:
    def __init__(self, name = None):
        self.main_window = tk.Tk()

        self.current_screen = 0

        self.intro_frame = tk.Frame(master = self.main_window)
        self.topic_select_frame = tk.Frame(master = self.main_window)
        
        self.build_intro_screen()
        self.update_current_screen(0)


        self.main_window.mainloop()

    # Will change the current screen that is display.
    # WARNING - If no current_screen is entered no screen will be unpacked
    def update_current_screen(self, new_screen, current_screen = -1):
        # Unpack/destroy current frame in prep for building next frame
        if current_screen == 0:
            self.intro_frame.grid_remove()
        elif current_screen = 1:
            self.topic_select_frame.grid_remove()

        # Builds the next frame
        if new_screen == 0:
            self.intro_frame.grid()
            self.current_screen = new_screen
        elif new_screen == 1:
            self.topic_select_frame.grid()
            self.current_screen = new_screen

    def build_intro_screen(self):
        self.intro_label = tk.Label(master = self.intro_frame, text = "intro label")
        self.intro_label.grid(column = 0, row = 0)

    def build_topic_select_screen(self):
        self.top_label = tk.Label(master = self.top_select_frame, text = "Choose a topic: ")

intro_window = MainApp()

