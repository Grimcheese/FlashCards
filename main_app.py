"""FlashCards GUI definitions.

This is the main program file. Run FlashCards by executing this script.

Each section of the program to be displayed in the main window is created as a 
separate frame which has its own class. Each frame class derives from the 
BasicFrame which provides the show() and remove() methods to hide and show the
frame as required when moving between sections of the program.

Each frame is designed to only be used by MainApp which manages switching between
each frame while each frame class defines the widgets and their functions that
should belong to that frame.

Classes:
    BasicFrame
    IntroFrame
    ChooseFileFrame
    TopicSelectFrame
    DisplayPrompts
    
    MainApp

"""
import tkinter as tk
from tkinter import ttk
import json

import handle_json
from handle_json import JSONHandler
from handle_json import JSONTopicHandler

from pathlib import Path


class BasicFrame:
    """A generic tkinter frame that can be further extended.

    Provides a base frame class that can be hidden or shown. Allows MainApp to
    easily switch between frames which have been further customised with
    additional widgets to have different frames within the main program window.
    """

    def __init__(self, parent):
        self.base_frame = ttk.Frame(master=parent)

    def show(self):
        self.base_frame.grid()

    def remove(self):
        self.base_frame.grid_remove()


class IntroFrame(BasicFrame):
    """The intro screen to be displayed to the user on program start.

    Extends a BasicFrame object with widgets to display the intro screen. Can be
    referred to by using it's string index S_INDEX variable.
    """

    S_INDEX = "intro_frame"

    def __init__(self, parent):
        """Initalise a frame by extending from a BasicFrame.

        Args:
            parent: The parent container for IntroFrame"""

        super().__init__(parent)
        self.intro_label = None

        self.build_intro_screen()

    def build_intro_screen(self):
        """Define and place the widgets for the intro screen.

        Reads the label to be displayed from a JSON file called gui_reference.json
        """

        gui_reference_data = JSONHandler.get_js("gui_reference.json")

        self.intro_label = ttk.Label(
            master=self.base_frame,
            text=gui_reference_data["intro_frame"][0]["main_text"],
        )
        self.intro_label.grid(column=0, row=0)


class ChooseFileFrame(BasicFrame):
    """The screen to be displayed for choosing a topic file.

    Extends the functionality of a BasicFrame by adding widgets to allow for
    displaying and choosing files. Can be referred to by using its string index
    S_INDEX.
    """

    S_INDEX = "choose_file_frame"

    def __init__(self, main_app):
        """Initialise the choose file frame by extending from a BasicFrame.

        Args:
            main_app: The parent container which is the window this frame will
                sit in.
        """

        super().__init__(main_app.main_window)

        self.chosen_file = main_app.topic_file

        self.found_files = []
        self.files_display = []

        self.main_label = None
        self.previous_frame_button = None
        self.next_frame_button = None

        self.build_choose_file_frame(main_app)

    def build_choose_file_frame(self, main_app):
        """Define and place the widgets to be used for the choose file screen.

        Args:
            main_app: The tk main window object which links all frames together.
        """

        self.main_label = ttk.Label(
            master=self.base_frame, text="Choose file to read topics/prompts from"
        )
        self.main_label.grid(column=0, row=1)

        self.previous_frame_button = ttk.Button(
            master=self.base_frame,
            text="Go back.",
            command=lambda: main_app.update_current_screen(
                main_app.intro_frame.S_INDEX, main_app.current_screen
            ),
        )
        self.previous_frame_button.grid(column=0, row=0)
        self.next_frame_button = ttk.Button(
            master=self.base_frame,
            text="Choose: '" + main_app.topic_file.get_name() + "'",
            command=lambda: self.to_topic_select(main_app),
            width=25,
        )
        self.next_frame_button.grid(column=1, row=0)

        self.create_file_button = ttk.Button(
            master=self.base_frame,
            text="Create new file",
            width=25,
            command=lambda: main_app.update_current_screen(
                main_app.create_topic_frame.S_INDEX, main_app.current_screen
            ),
        )
        self.create_file_button.grid(column=3, row=0)

        self.show_files()

    def to_topic_select(self, main_app):
        """Change display from choose file screen to topic select screen."""

        main_app.topic_file = self.chosen_file
        main_app.topic_select_frame = TopicSelectFrame(main_app)
        main_app.update_current_screen(
            main_app.topic_select_frame.S_INDEX, main_app.current_screen
        )

    def show_files(self):
        """Display a list of files that can be used as button widgets."""

        rsrc_dir = Path(MainApp.CWD, MainApp.RESOURCES_DIR)

        file_index = 0
        for file in rsrc_dir.iterdir():
            # Check each file supports FlashCards format
            try:
                self.found_files.append(JSONTopicHandler(file))
                self.found_files.append(file)
                file_name = Path(file).name
                self.files_display.append(
                    ttk.Button(
                        master=self.base_frame,
                        text=file_name,
                        command=lambda file=file: self.pick_file(file),
                        width=25,
                    )
                )
                self.files_display[file_index].grid(column=0, row=file_index + 2)

                file_index += 1
            except json.decoder.JSONDecodeError:
                print("Not a valid FlashCards file")

    def pick_file(self, f_path):
        """Select the file after button press and update widgets on the frame.

        Args:
            f_path: The file path that points to the file that has been selected."""

        new_file = JSONTopicHandler(f_path)
        self.chosen_file = new_file
        print("Picking file: " + new_file.get_name())

        self.next_frame_button.config(text="Choose: '" + new_file.get_name() + "'")


class TopicSelectFrame(BasicFrame):
    """The screen to be displayed when selecting which topics the program will run.

    Provides the following functions:
        Return to file selection
        A list of topics from the file displayed as buttons
        Labels displaying if a topic has been chosen
        A button to run the prompts from the selected topics
    """

    S_INDEX = "topic_select_frame"

    def __init__(self, main_app):
        """Initialises the frame with main_app as the parent."""

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
        """Define and place the widgets used for topic selection.

        Args:
            main_app: The tk main window object that links all frames together.
        """

        self.top_label = ttk.Label(master=self.base_frame, text="Topics from file: ")
        self.top_label.grid(column=0, row=1)

        self.next_screen_button = ttk.Button(
            master=self.base_frame,
            text="Run prompts from selected topic/s",
            command=lambda: self.to_display_prompts_frame(main_app),
            state=tk.DISABLED,
        )

        self.previous_frame_button = ttk.Button(
            master=self.base_frame,
            text="Back to file selection.",
            command=lambda: main_app.update_current_screen(
                main_app.choose_file_frame.S_INDEX, main_app.current_screen
            ),
        )
        self.previous_frame_button.grid(column=0, row=0)

        topic_row = self.make_topic_buttons()
        self.next_screen_button.grid(column=0, row=topic_row + 1)

    def to_display_prompts_frame(self, main_app):
        """Update the main_app window frame to the display prompts screen.

        Args:
            main_app: The tk main window object which the program is displayed
                from.
        """

        main_app.display_propmts_frame = DisplayPrompts(main_app)
        main_app.update_current_screen(
            main_app.display_prompts_frame.S_INDEX, main_app.current_screen
        )

    def make_topic_buttons(self):
        """Creates a list of button widgets, one for each topic in the file.

        Returns:
            topic_row: The number of buttons that have been created so there is
                a reference that the TopicSelectFrame can organise other
                widgets for this frame on the grid correctly."""

        topic_row = 1
        for topic in self.topic_file.topics:
            self.topic_buttons.append(
                ttk.Button(
                    master=self.base_frame,
                    text=topic,
                    width=20,
                    command=lambda topic=topic: self.pick_topics(topic),
                )
            )

            self.chosen_topic_labels.append(ttk.Label(master=self.base_frame, text=""))
            self.update_picked_topics_label(topic)

            self.topic_buttons[topic_row - 1].grid(column=1, row=topic_row, sticky=tk.W)
            self.chosen_topic_labels[topic_row - 1].grid(column=2, row=topic_row)
            topic_row += 1

        return topic_row

    def pick_topics(self, selected_topic):
        """Update the list of selected topics with the selected_topic argument."""

        print("You have selected: " + selected_topic)
        self.topic_file.set_topic(selected_topic)

        self.update_picked_topics_label(selected_topic)

    def update_picked_topics_label(self, selected_topic):
        """Update the corresponding selected_topic label when a topic is selected."""

        topic_label_index = self.topic_file.topics.index(selected_topic)
        is_selected = self.topic_file.topic_is_selected(selected_topic)
        if is_selected:
            self.chosen_topic_labels[topic_label_index].config(text="Picked")
        else:
            self.chosen_topic_labels[topic_label_index].config(text="")

        if len(self.topic_file.chosen_topics) == 0:
            print("Next screen button disabled")
            self.next_screen_button.config(state=tk.DISABLED)
        else:
            print("Next screen button activated")
            self.next_screen_button.config(state=tk.ACTIVE)

        self.topic_file.topic_string(1)


class DisplayPrompts(BasicFrame):
    """The screen that displays prompts and their answers to the user.

    Provides the following functions:
        Return to start screen or topic select buttons
        The ability to navigate through all the prompts from chosen topics
        Displays a prompt and an answer
        Navigation using arrow keys or buttons"""

    S_INDEX = "display_prompts_frame"

    def __init__(self, main_app):
        """Initialise the display prompt screen with the parent element.

        Args:
            main_app: The parent main window which contains the entire program.
        """

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
        """Prints values of prompts from the file to console.

        Used for debugging purposes, not required for program interface.
        """

        self.topic_file.topic_string()
        print("Number of prompts: " + str(self.topic_file.number_of_prompts()))
        for i in range(self.topic_file.number_of_prompts()):
            print(self.topic_file.get_value(i, "prompt"))

    def build_run_prompts_screen(self, main_app):
        """Create and place the widgets used to display the prompts.

        Args:
            main_app: The main window which the program is contained within.
        """

        self.return_to_start_button = ttk.Button(
            master=self.base_frame,
            text="Return to start screen",
            command=lambda: main_app.update_current_screen(
                main_app.intro_frame.S_INDEX, main_app.current_screen
            ),
        )
        self.return_to_start_button.grid(column=0, row=0)
        self.return_to_topic_select_button = ttk.Button(
            master=self.base_frame,
            text="Return to topic select",
            command=lambda: main_app.update_current_screen(
                main_app.topic_select_frame.S_INDEX, main_app.current_screen
            ),
        )
        self.return_to_topic_select_button.grid(column=1, row=0)

        self.top_label = ttk.Label(
            master=self.base_frame, text="Running through prompts!"
        )
        self.top_label.grid(column=2, row=0)

        self.back_button = ttk.Button(
            master=self.base_frame,
            text="Go back a prompt",
            command=self.previous_prompt,
        )
        self.back_button.grid(column=3, row=0)

        self.prompt_label = ttk.Label(
            master=self.base_frame, text="", width=22, wraplength=100
        )
        self.prompt_label.grid(column=2, columnspan=2, row=2)
        self.answer_label = ttk.Label(master=self.base_frame, text="")
        self.answer_label.grid(column=3, row=3)

        self.start_prompts_button = ttk.Button(
            master=self.base_frame,
            text="Begin running through prompts",
            command=self.show_first_prompt,
        )
        self.start_prompts_button.grid(column=4, row=0)

        self.counter_label = ttk.Label(master=self.base_frame, text="")
        self.counter_label.grid(column=4, row=0)

    def show_first_prompt(self):
        """Display the initial prompt from the randomised list."""

        self.prompt_labels_update(self.topic_file.get_value(0, "prompt"))
        self.start_prompts_button.grid_remove()
        self.start_prompts_button.config(state=tk.DISABLED)

    def previous_prompt(self):
        """Display the prompt at the index from current prompt - 1."""

        if self.prompt_index > 0:
            self.prompt_index = self.prompt_index - 1
            self.prompt_labels_update(
                self.topic_file.get_value(self.prompt_index, "prompt"),
                self.topic_file.get_value(self.prompt_index, "answer"),
            )
            self.end_of_prompts = False

            print("Going back to last prompt")
            print("Current index number: " + str(self.prompt_index))

    def goto_next_prompt(self):
        """Update the next prompt or answer depending on current display."""

        print("Current index: " + str(self.prompt_index))
        try:
            if self.showing_answer:
                print("Updating prompt label")
                self.next_prompt()
            else:
                print("Updating answer label ")
                self.prompt_labels_update(
                    answer=self.topic_file.get_value(self.prompt_index, "answer")
                )
        except IndexError:
            self.prompt_labels_update(
                prompt="Out of prompts! Press Enter to return to start...", answer=""
            )
            self.end_of_prompts = True

    def next_prompt(self):
        """Send the value of the next prompt with no answer to the prompt label."""

        self.prompt_index = self.prompt_index + 1
        self.prompt_labels_update(
            prompt=self.topic_file.get_value(self.prompt_index, "prompt"), answer=""
        )

    def prompt_labels_update(self, prompt=None, answer=None):
        """Update the prompt and answer labels.

        Can choose to update either prompt, answer or both depending on given
        arguments. Each has a default of None. Updates the current prompt
        counter with the current index value.

        Args:
            prompt: The text to display on the prompt label. A none value results
                in no change.
            answer: The text to display on the answer label. A none value results
                in no change.
        """

        if prompt is not None:
            self.prompt_label.config(text=prompt)
        if answer is not None:
            self.answer_label.config(text=answer)
            if answer == "":
                self.showing_answer = False
                print("Not showing answer")
            else:
                self.showing_answer = True
                print("Showing answer")
        self.update_counter()

    def update_counter(self):
        """Display the index of the current prompt being displayed.

        Will display current_index/total_number_of_propmts
        """

        num_prompts = self.topic_file.number_of_prompts()
        if self.prompt_index < num_prompts:
            count_val = str(self.prompt_index + 1) + " / " + str(num_prompts)
            self.counter_label.config(text=count_val)
        else:
            self.counter_label.config(text="")

    def show(self, chosen_file):
        """Extends BasicFrame show functionality to properly set topic file."""

        self.topic_file = chosen_file
        self.topic_file.prompts_from_chosen_topics()
        self.topic_file.randomise_prompts()

        self.topic_file.print_prompts()
        self.show_first_prompt()

        super().show()

    def remove(self):
        """Extends BasicFrame remove to properly reset class attributes."""

        self.prompt_index = 0
        self.showing_prompt = False
        self.prompt_labels_update("", "")

        super().remove()


class CreateTopicFrame(BasicFrame):
    """Displays text boxes to allow the user to create their own topics.


    Allow the user to choose a file to modify or create a new one,
    then the topic to add to or create. Then once file and topic is
    selected, enter the new prompt and answer.
    """

    S_INDEX = "create_topic_frame"

    def __init__(self, main_app):
        """Initialise the create topic screen with parent element.

        Args:
            main_app: The parent window this frame has as a parent.
        """

        super().__init__(main_app.main_window)

        self.build_create_topic_frame(main_app)

    def build_create_topic_frame(self, main_app):
        """Define and place widgets that make up the create topic frame.

        Args:
            main_app: The parent window the frame sits witin.
        """

        # Program navigation header buttons
        self.file_select_screen_button = ttk.Button(
            self.base_frame,
            text="File Select Screen",
            command=lambda: main_app.update_current_screen(
                main_app.choose_file_frame.S_INDEX, main_app.current_screen
            ),
        )
        self.file_select_screen_button.grid(column=1, row=0)

        self.file_select_frame = ttk.Frame(self.base_frame)
        self.file_select_frame.grid(column=1, row=1)

        # Choose the file
        self.files_label = ttk.Label(self.file_select_frame, text="Files")
        self.files_label.grid(column=1, row=3)

        files = handle_json.get_files(Path(Path.cwd(), "resources"))
        files_var = tk.StringVar(value=files)

        self.topics_label = ttk.Label(self.file_select_frame, text="Topics")
        self.topics_label.grid(column=3, row=3)

        # List box and bindings - display files and topics from file in listbox
        self.file_listbox = tk.Listbox(
            self.file_select_frame,
            listvariable=files_var,
            height=5,
            exportselection=False,
        )
        self.file_listbox.grid(column=1, row=4)

        self.list_bar1 = ttk.Scrollbar(
            self.file_select_frame, orient=tk.VERTICAL, command=self.file_listbox.yview
        )
        self.list_bar1.grid(column=2, row=4, sticky=(tk.N, tk.S))
        self.file_listbox["yscrollcommand"] = self.list_bar1.set

        self.file_listbox.bind(
            "<<ListboxSelect>>",
            lambda f: self.display_topics_from_file(self.file_listbox.curselection()),
        )

        self.topics_var = tk.StringVar()
        self.topic_listbox = tk.Listbox(
            self.file_select_frame,
            listvariable=self.topics_var,
            height=5,
            exportselection=False,
        )
        self.topic_listbox.grid(column=3, row=4)

        self.list_bar2 = ttk.Scrollbar(
            self.file_select_frame, orient=tk.VERTICAL, command=self.topic_listbox.yview
        )
        self.list_bar2.grid(column=4, row=4, sticky=(tk.N, tk.S))
        self.topic_listbox['yscrollcommand'] = self.list_bar2.set
        
        # Text field that displays formatted contents of the file/topic
        self.file_text = tk.Text(self.base_frame, state="disabled", width=95, height=20)
        self.file_text.grid(pady=8, padx=(10, 0), column=1, row=3, columnspan=10)

        self.text_scrollbar = ttk.Scrollbar(
            self.base_frame, orient=tk.VERTICAL, command=self.file_text.yview
        )
        self.text_scrollbar.grid(pady=8, column=11, row=3, sticky=(tk.N, tk.S))
        self.file_text.configure(yscrollcommand=self.text_scrollbar.set)

        # New prompt and answer submission to the selected file and topic
        self.prompt_box_label = ttk.Label(self.base_frame, text="New prompt")
        self.prompt_box_label.grid(column=1, row=5)

        self.prompt_box = tk.Text(self.base_frame, width=50, height=1, wrap="none")
        self.prompt_box.grid(column=2, row=5)

        self.answer_box_label = ttk.Label(self.base_frame, text="New answer")
        self.answer_box_label.grid(column=1, row=6)

        self.answer_box = tk.Text(self.base_frame, width=50, height=2, wrap="word")
        self.answer_box.grid(column=2, row=6)

    def display_topics_from_file(self, file_index):
        """Populate the topics listbox with topics from the selected file.

        Bound to <<ListboxSeletion>> events.

        Args:
            file_index: Return value of curselection() of the file listbox. Will
                give a tuple where the first element is the index of the
                currently selected file from self.file_listbox.
        """

        # Select chosen file from files in resources directory
        file_index = file_index[0]  # Only interested in first element of tuple
        files = handle_json.get_files(Path(Path.cwd(), "resources"))
        chosen_file = files[file_index]

        print(chosen_file)

        # Find topics from file
        fpath = Path.joinpath(Path.cwd(), "resources", chosen_file)
        print(fpath)
        file_obj = JSONTopicHandler(fpath)

        # Create formatted string containing topics and place in text field
        formatted_topic_string = self.formatted_file_output(file_obj)
        self.file_text.configure(state="normal")
        self.file_text.delete("1.0", "end")
        self.file_text.insert("end", formatted_topic_string)
        self.file_text.configure(state="disabled")

        # Set Listbox stringvar to list of topics
        self.topics_var.set(file_obj.topics)

    def formatted_file_output(self, file):
        """Takes a topic file and returns a string with the contents formatted."""

        formatted_string = f"{file.fname} topic file\n"

        for topic in file.topics:
            topic_string = f"{topic}\n"
            prompts = file.prompts_from_topic(topic)
            for prompt in prompts:
                topic_string = f"{topic_string}\tPrompt: {prompt['prompt']}\n"
                topic_string = f"{topic_string}\tAnswer: {prompt['answer']}\n\n"
            formatted_string = f"{formatted_string}{topic_string}"
        return formatted_string


class MainApp:
    """The main app window and its functionality.

    Contains each frame as an attribute and allows for switching between the
    frames as the user moves through the program.
    """

    CWD = Path.cwd()
    RESOURCES_DIR = "resources"
    default_file_path = Path.joinpath(CWD, RESOURCES_DIR, "topic.json")

    def __init__(self, parent, name=None):
        """Initialises the main window with a root tk window."""

        self.main_window = parent
        self.current_screen = "intro_frame"

        self.topic_file = JSONTopicHandler(MainApp.default_file_path)

        self.intro_frame = IntroFrame(self.main_window)
        self.create_topic_frame = CreateTopicFrame(self)
        self.choose_file_frame = ChooseFileFrame(self)
        self.topic_select_frame = TopicSelectFrame(self)
        self.display_prompts_frame = DisplayPrompts(self)

        self.update_current_screen(self.intro_frame.S_INDEX)

        self.set_callbacks()

    def update_current_screen(self, new_screen, current_screen=None):
        """Switch currently displayed frame to new_screen.

        WARNING - If no current_screen is entered (no argument passed) no screen
        will be unpacked/displayed

        Args:
            new_screen: The new screen to display in MainApp. This argument
                should be a string value which represents one of the defined
                class attributes S_INDEX.
            current_screen: The current_screen which should be removed.
        """
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
        elif current_screen == "create_topic_frame":
            self.create_topic_frame.remove()

        # Builds the next frame using show()
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
        elif new_screen == "create_topic_frame":
            self.create_topic_frame.show()
            self.current_screen = new_screen

        if current_screen == None:
            print("No previous screen, no screen unpacked.")

    def clear_instance(self):
        """Delete each frame object and create a new one."""

        del self.choose_file_frame
        del self.topic_select_frame
        del self.display_prompts_frame
        del self.topic_file

        self.topic_file = JSONTopicHandler(MainApp.default_file_path)
        self.choose_file_frame = ChooseFileFrame(self)
        self.topic_select_frame = TopicSelectFrame(self)
        self.display_prompts_frame = DisplayPrompts(self)

    def set_callbacks(self):
        """Define all the callback functions and wrappers to use for bindings."""

        def handle_callbacks(event, self=self):
            if self.current_screen == "intro_frame":
                self.update_current_screen(
                    self.choose_file_frame.S_INDEX, self.current_screen
                )
                print("Any key pressed")
            elif self.current_screen == "display_prompts_frame" and (
                event.keysym == "Return" or event.keysym == "Right"
            ):
                next_display_prompt_callback(event, self)
            elif (
                self.current_screen == "display_prompts_frame"
                and event.keysym == "Left"
            ):
                self.display_prompts_frame.previous_prompt()

        def next_display_prompt_callback(event, self=self):
            if self.display_prompts_frame.end_of_prompts is False:
                self.display_prompts_frame.goto_next_prompt()
            elif (
                self.display_prompts_frame.end_of_prompts is True
                and event.keysym == "Return"
            ):
                self.update_current_screen(
                    self.intro_frame.S_INDEX, self.current_screen
                )

        self.main_window.bind(
            "<Any-Key>", handle_callbacks
        )  # Will trigger while any frame is up - perform check in callback method
        self.main_window.bind("<Any-Button>", handle_callbacks)


if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("FlashCards! - The best way to study-")
    main_window.geometry("800x600")
    main_window.resizable(False, False)

    app = MainApp(main_window)

    main_window.mainloop()
