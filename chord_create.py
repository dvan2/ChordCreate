import os
import pickle
import time
import re

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SIZE = len(NOTES)

VALID_SYMBOLS = ["#", "b", "m", "M", "7" "dim", "sus"]

MAJOR_CHORD = [0, 4, 7]
MINOR_CHORD = [0, 3, 7]

MAJOR_SCALES = [0, 2, 4, 5, 7, 9, 11, 0]
MINOR_SCALES = [0, 2, 3, 5, 7, 8, 10, 0]

# Where to save pickled files
PICKLED_FOLDER = "pickled_files"
TEXT_FOLDER = "text_files"

# # Used for displaying song
DISPLAY_PAUSE = 2
MEDIUM_PAUSE = 1.2
QUICK_PAUSE = 0.8

# remove after test
# DISPLAY_PAUSE = 0
# MEDIUM_PAUSE = 0
# QUICK_PAUSE = 0


x_emoji = "❌ "
check_emoji = "✅"
warning_emoji = "⚠️  "


def main():
    print(
        "\n\n\n\n\n\n\nHello.  This program allows you to learn about chords and scales."
    )
    print(
        "You can also create your own chord progression, transpose, save and load them back."
    )
    time.sleep(1.5)

    while True:
        print_line()
        print("\tMain Menu")
        selection = get_selection(
            "1 to create a new chord progression for a song\n2 to load an existing song\n3 to enter Music Playground🎶",
            3,
        )
        if selection == 1 or selection == 2:
            print_line()
            print("\t\tMain Menu > Song Progression")
            if selection == 1:
                song = create_song()
            if selection == 2:
                song = interact_load_song()

            while True:
                if song == -1:
                    break
                print_line()
                print(f"Current song opened: {song.name}")
                write_selection = get_selection(
                    "1 to create a new section for this song\n2 to edit a section for this song\n3 to transpose this song to a different key\n4 to display the song\n5 to save the song",
                    5,
                )
                if write_selection == 1:
                    song.create_new_section()
                if write_selection == 2:
                    song.edit_section()
                if write_selection == 3:
                    song.transpose()
                if write_selection == 4:
                    print(song)
                    time.sleep(DISPLAY_PAUSE)
                if write_selection == 5:
                    song.save_song()
                if write_selection == -1:
                    if song.saved == False:
                        prompt = f"{warning_emoji}Warning... There are unsaved changes to {song.name}.  Quit with out saving?\n"
                        user_yes = get_yes_no(prompt)
                        if user_yes:
                            break
                        else:
                            continue
                    break
        elif selection == 3:
            while True:
                print_line()
                print("\t\tMain Menu > Music Playground🎶\n")
                playground_menu = get_selection(
                    "1 to create a major chord\n2 to create a minor chord\n3 to generate a major scale\n4 to generate a minor scale\n",
                    4,
                )
                if playground_menu == 1:
                    print("\t\tMain Menu > Music Playground🎶 > Major Chords\n\n")
                    print(
                        "Major Chords comprise of 3 notes, the root, the third and the fifth. (1, 3, 5)\n"
                    )
                    interact_chord(MAJOR_CHORD)
                if playground_menu == 2:
                    print("\t\tMain Menu > Music Playground🎶 > Minor Chords\n\n")
                    print(
                        "Minor Chords comprise of 3 notes, the root, the minor third and the fifth. (1, 3b , 5)\n"
                    )
                    interact_chord(MINOR_CHORD)
                if playground_menu == 3:
                    print("\t\tMain Menu > Music Playground🎶 > Major Scales\n\n")
                    print(
                        "Major scales follow W-W-H-W-W-W-H\nWhere W(whole) means 2 semitones apart\nH(half) means 1 semitone apart\n"
                    )
                    interact_scales(MAJOR_SCALES)
                if playground_menu == 4:
                    print("\t\tMain Menu > Music Playground🎶 > Minor Scales\n\n")
                    print(
                        "Minor scales follow W-H-W-W-H-W-W\nWhere W(whole) means 2 semitones apart\nH(half) means 1 semitone apart\n"
                    )
                    interact_scales(MINOR_SCALES)

                if playground_menu == -1:
                    break
        if selection == -1:
            break

def create_song():
    while True:
        name = input("\n\nEnter a name for the song: ")
        print()
        try:
            out = int(name)
            if out == -1:
                # go back to main menu
                return -1
        except ValueError:
            pass
        try:
            song = Song(name)
            return song
        except ValueError as e:
            print("\n\nError,", e)
            print("Consider loading the song instead.")
            pass


def interact_load_song():
    while True:
        display_existing_files()
        name = input("\nEnter an existing file: ")
        print()
        try:
            out = int(name)
            print_line()
            if out == -1:
                # go back to main menu
                return -1
        except ValueError:
            pass
        try:
            song = Song.load_song(name)
            song.saved = True
            song.loaded = True
            prompt = f"{check_emoji} Found Song: {song.name}"
            print_animated(prompt)
            return song
        except FileNotFoundError:
            print(f"\n\n{x_emoji}Error, Cannot find song name of: {name}")
            pass


def display_existing_files():
    if os.path.exists(PICKLED_FOLDER) and os.path.isdir(PICKLED_FOLDER):
        files = os.listdir(PICKLED_FOLDER)

        pickled_files = [
            os.path.splitext(file)[0] for file in files if file.endswith(".pk1")
        ]

        print("Currently saved songs: ")
        for file in pickled_files:
            print(file)
    else:
        print("There are no saved songs yet")


def interact_chord(m_chord):
    while True:
        try:
            result = chord(m_chord)
            if result == -1:
                print("\n\n")
                break
            else:
                print(result)
        except ValueError as e:
            print("Error:", e)
            pass


def interact_scales(m_scale):
    while True:
        try:
            result = chord(m_scale)
            if result == -1:
                print("\n\n")
                break
            else:
                print(result)
        except ValueError as e:
            print("Error:", e)
            pass


def print_line():
    print()
    print("__________________________________________________________________")
    print()


def get_selection(prompt, menu_size):
    while True:
        try:
            print(f"\nEnter:\n{prompt}\n-1 to go back or quit the program\n\n")
            # time.sleep(QUICK_PAUSE)
            res = int(input("Input: "))
        except ValueError:
            print(f"\nError.  Please enter a number\n")
            pass
        else:
            if res > menu_size:
                print(f"{x_emoji}Invalid selection: {res}. Enter a smaller number")
            elif res < -1:
                print(f"Invalid selection: {res}. Enter a bigger number")
            else:
                return res


def get_yes_no(prompt):
    """
    Prompts user and asks for yes or no

    Returns:
        True if user responds Yes.
        False if user responds No.
    """
    print(prompt)
    while True:
        try:
            res = int(input(f" 1: Yes\n-1: No\nInput: "))
            print_line()
        except ValueError:
            print(f"{x_emoji}Error. Enter 1 or -1")
            pass
        else:
            if res == 1:
                return True
            elif res == -1:
                return False


def print_animated(prompt, speed=0.045):
    for c in prompt:
        print(c, end="", flush=True)
        time.sleep(speed)
    time.sleep(QUICK_PAUSE)


def chord(chord):
    res = input("Enter a key: ").upper()
    try:
        out = int(res)
        if out == -1:
            return -1
    except ValueError:
        pass
    try:
        index = NOTES.index(res)
    except ValueError:
        raise ValueError(f"Invalid Note: {res}")
    result = ""
    for note in chord:
        result += NOTES[(note + index) % SIZE] + "-"
    return result[:-1]


def scale(scale):
    key = input("Enter a key: ").upper()
    try:
        out = int(key)
        if out == -1:
            return -1
    except ValueError:
        pass

    result = ""
    try:
        index = NOTES.index(key)
    except ValueError:
        raise ValueError(f"{key} is not a valid key")
    else:
        for note in scale:
            result += NOTES[(note + index) % SIZE] + "-"
        return result[:-1]


def is_valid_chords(chords):
    chord_pattern = re.compile(r"^(([A-G](#|b)?m?(5|7|9)?)?(\s|-|$))+$")

    if chord_pattern.match(chords.strip()):
        return True
    else:
        return False

    # for chord in chords:
    #     if chord.strip() != "":
    #         if not chord_pattern.match(chord.strip()):
    #             return False
    # return True
    # if chord not in NOTES:
    #     if (
    #         chord != "-"
    #         and chord != "_"
    #         and chord != "m"
    #         and chord != "#"
    #         and chord != "b"
    #         and chord != "\n"
    #         and chord != " "
    #     ):
    #         raise ValueError(f"{chord} is invalid")


def generate_file_path(folder, file_name, ext):
    """
    Returns a file path by joining all parameters
    """
    file_name = file_name.lower().replace(" ", "") + ext
    file_path = os.path.join(folder, file_name)
    return file_path


def create_chord_progression_section():
    chords = ""
    while True:
        chord_input = input()
        if chord_input == "-1":
            return chords
        else:
            if chord_input == "":
                lines = chords.split("\n")
                last_line = lines[-2]
                chords += last_line + "\n"
            else:
                if is_valid_chords(chord_input):
                    chords += chord_input + "\n"
                else:
                    print(
                        f"{chord_input} has an invalid Chord key.  Please rewrite from begginging."
                    )
                    print_line()
                    chords = ""


class Song:
    def __init__(self, name):
        self.file_path = generate_file_path(PICKLED_FOLDER, name, ".pk1")
        self.text_file_path = generate_file_path(TEXT_FOLDER, name, ".txt")
        if os.path.isfile(self.file_path):
            raise ValueError("Song already exists")
        self.name = name
        self.transpose_amount = 0
        self.sections = {}
        # Variable to keep track if there are recent changes
        self.saved = False

        # If it's loaded, we don't need to check for same file name
        self.loaded = False

    def create_new_section(self):
        print_line()
        if len(self.sections) == 0:
            print("There are no sections yet.")
        else:
            result = "Existing sections\n"
            for sec in self.sections:
                result += sec + "\n"
            print(result)
        while True:
            section = input(
                "Enter a name for the new section: Intro, Verse, Chorus, Instrumental, etc: "
            )
            print_line()
            if section in self.sections:
                print(f"{x_emoji} {section} already exists.")
            elif section == "-1":
                return
            else:
                break
        print_line()
        print(
            f"Write out a new chord progression for the {section}\nNote: Enter -1 to finish\nEnter nothing to duplicate line"
        )
        print("Chord Progression:")
        chords = create_chord_progression_section()
        self.sections[section] = chords
        self.saved = False
        prompt = f"New section: {section}, added..."
        self.saved = False
        print_animated(prompt)
        print(self, end="")
        time.sleep(DISPLAY_PAUSE)

    def get_title(self):
        return self.name

    def __str__(self):
        print_line()
        result = f"\t\t{self.name}\n\n"
        for section, chords in self.sections.items():
            result += f"{section}:\n{chords}\n\n"
        return result[:-2]

    # Using pickle to store object
    # https://www.geeksforgeeks.org/how-to-use-pickle-to-save-and-load-variables-in-python/

    def save_song(self):
        folder = PICKLED_FOLDER
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(TEXT_FOLDER):
            os.makedirs(TEXT_FOLDER)

        # If first time saving, prompt for a location
        if not os.path.exists(self.file_path):
            default_name = self.file_path.split("\\")[1]
            print_animated(f"Default file name: {default_name}.\n")

            yes = get_yes_no("Would you like to change the file name?")
            if yes:
                self.create_user_path()

        while True:
            # Check existing file
            if os.path.exists(self.file_path) and not self.loaded:
                print(f"{warning_emoji}{self.file_path} already exists\n")
                print("Enter a different file name.")
                print_line()
                self.create_user_path()
            else:
                with open(self.file_path, "wb") as file:
                    pickle.dump(self, file)
                with open(self.text_file_path, "w") as file:
                    file.write(str(self))
                if not os.path.exists(self.file_path):
                    print(f"{self.file_path} is an invalid file name.")
                    self.create_user_path()
                else:
                    break

        self.saved = True
        prompt = f"{self.name} saved in {self.file_path}"
        print_animated(prompt, 0.03)

    def create_user_path(self):
        user_file_name = input(f"Enter filename for {self.name}: ")
        user_path = generate_file_path(PICKLED_FOLDER, user_file_name, ".pk1")
        user_text_path = generate_file_path(TEXT_FOLDER, user_file_name, ".txt")
        self.file_path = user_path
        self.text_file_path = user_text_path

    @classmethod
    def load_song(cls, name):
        file_path = generate_file_path(PICKLED_FOLDER, name, ".pk1")
        with open(file_path, "rb") as file:
            result_song = pickle.load(file)
        return result_song

    def edit_section(self):
        while True:
            if len(self.sections) == 0:
                print("There are no song sections yet. Consider creating new section")
                return
            print_line()
            print(f"\t\tEditing {self.name}")
            result = "Available sections to edit: \n"
            for sec in self.sections:
                result += sec + "\n"
            print(result)

            new_sec = input("Enter a section to edit: ").strip()
            if new_sec == "-1":
                break
            print_line()
            if new_sec in self.sections:
                result = ""
                prompt = f"Editing {new_sec} Section:"
                print_animated(prompt)
                print(f"\n{self.sections[new_sec]}\n")
                print("Hint: You can enter nothing to delete the section")
                new_chords = input(f"Enter new chord progression for the {new_sec}: ")
                if new_chords == "-1":
                    return
                elif new_chords == "":
                    prompt = f"Do you want to delete {new_sec}\n"
                    del_res = get_yes_no(prompt)
                    if del_res:
                        del self.sections[new_sec]
                        self.saved = False
                        prompt = f"{new_sec} deleted"
                        print_animated(prompt)
                        print()
                        print_animated("Updated Song: ")
                        print(self, end="")
                        return
                    else:
                        continue
                try:
                    is_valid_chords(new_chords)
                except ValueError as e:
                    print(f"{x_emoji}Error: {e}")
                    print(f"{new_sec} not updated.")
                    continue

                print_line()
                prompt = f"Do you want to update {new_sec}?\nFROM:\n"
                print_animated(prompt)
                print(f"{self.sections[new_sec]}\n ")
                print_animated("TO\n")
                print(self.sections[new_sec])
                while True:
                    print(f" 1: Yes\n-1: No")
                    confirm = input("Input: ")
                    if confirm == "1":
                        self.sections[new_sec] = new_chords
                        self.saved = False
                        prompt = f"{x_emoji}Done!"
                        print_animated(prompt)
                        print(f"{new_sec} updated to:\n {new_chords}")
                        time.sleep(DISPLAY_PAUSE)
                        return
                    elif confirm == "-1":
                        print_animated(f"Aborted editing {new_sec}")
                        break
                    else:
                        print(f"{x_emoji}Input: '{confirm}' is invalid")
            else:
                print(f"{x_emoji}Cannot find '{new_sec}' in {self.name}")

    """
    Transpose a song up or down(-) some number of semitones
    """

    def transpose(self):
        """
        Prompt user and tranpose the song
        """
        while True:
            try:
                print_line()
                print("Note: Enter nothing to return to original key written")
                amount = input("Enter how number of semitones to transpose to: ")
                print_line()
                if amount == "":
                    # Revert what we transposed
                    amount = -1 * (self.transpose_amount)
                    self.transpose_amount = 0
                else:
                    amount = int(amount)
                    self.transpose_amount += amount
            except ValueError:
                print("Input was not a number")
                pass
                # raise ValueError("Input was not a number.")
            else:
                for section, chords in self.sections.items():
                    result = ""
                    i = 0
                    while i < len(chords):
                        chord = chords[i]
                        if chord in NOTES:
                            if i + 1 < len(chords):
                                if chords[i + 1] == "#":
                                    # ignore the #
                                    i += 1
                                    chord += "#"
                            index = NOTES.index(chord)
                            if self.transpose_amount < 0:
                                amount += SIZE
                            result += NOTES[(amount + index) % SIZE]
                        elif chord != "#" or chord != "b":
                            result += chord
                        i += 1
                    print(f"Chords transposed {amount} semitones")
                    self.sections[section] = result
                    self.saved = False
                    print_animated("Newly transposed Version:")
                    print(self, end="")
                    time.sleep(DISPLAY_PAUSE)
                    return


if __name__ == "__main__":
    main()
