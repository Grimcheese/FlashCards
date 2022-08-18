# Module that defines the GUI elements of FlashCards
import tkinter as tk

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
    
    # B
    def initalise_screens(self):
        self.build_intro_screen()
        self.build_topic_select_screen()

    def build_intro_screen(self):
        self.intro_label = tk.Label(master = self.intro_frame, text = "intro label")
        self.intro_label.grid(column = 0, row = 0)

        self.scene_change_button = tk.Button(master = self.intro_frame, text = "Next scene", command = lambda: self.update_current_screen(1, self.current_screen))
        self.scene_change_button.grid(column = 1, row = 0)

    def build_topic_select_screen(self):
        self.top_label = tk.Label(master = self.topic_select_frame, text = "Choose a topic: ")
        self.top_label.grid(column = 0, row = 0)

        self.back_to_start_button = tk.Button(master = self.topic_select_frame, text = "Back to intro!", command = lambda: self.update_current_screen(0, self.current_screen))
        self.back_to_start_button.grid(column = 0, row = 1)

if __name__ == "__main__":
    main_window = tk.Tk()
    app = MainApp(main_window)

    main_window.mainloop()

