import os
import pickle
import time

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SIZE = len(NOTES)

MAJOR_CHORD = [0, 4, 7]
MINOR_CHORD = [0, 3, 7]

MAJOR_SCALES = [0, 2, 4, 5, 7, 9, 11, 0]
MINOR_SCALES = [0, 2, 3, 5, 7, 8, 10, 0]


def main():
    print(
        "\n\n\n\n\n\n\nHello.  This program allows you to learn about chords and scales."
    )
    print(
        "You can also create your own chord progression, transpose, save and load them back."
    )

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
                    "1 to create a new section for this song\n2 to edit a section for this song\n3 to transpose this song to a different key\n4 to display the song\n5 to save the song", 5
                )
                if write_selection == 1:
                    song.create_section()
                if write_selection == 2:
                    song.edit_section()
                if write_selection == 3:
                    song.transpose()
                if write_selection == 4:
                    print(song)
                    time.sleep(2)
                if write_selection == 5:
                    song.save_song()
                if write_selection == -1:
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
            if out== -1:
                #go back to main menu
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
        name = input("\nEnter an existing file: ")
        print()
        try:
            out = int(name)
            if out== -1:
                #go back to main menu
                return -1
        except ValueError:
            pass
        try:
            song = Song.load_song(name)
            return song
        except FileNotFoundError:
            print(f"\n\nError, Cannot find song name of: {name}")
            pass



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
            res = int(
                input(f"\nEnter:\n{prompt}\n-1 to go back or quit the program\n\nInput: ")
            )
        except ValueError:
            print(f"\nError.  Please enter a number\n")
            pass
        else:
            if res > menu_size:
                print(f"Invalid selection: {res}. Enter a smaller number")
            elif res < -1:
                print(f"Invalid selection: {res}. Enter a bigger number")
            else:
                return res

def get_yes_no(prompt):
    print(prompt)
    while True:
        try:
            res = int(input(f' 1: Yes\n-1: No\nInput: '))
        except ValueError:
            print("Enter 1 or -1")
            pass
        else:
            if res == 1:
                return True
            elif res == -1:
                return False

def print_animated(prompt, speed=0.05):
    for c in prompt:
        print(c, end = "", flush = True)
        time.sleep(speed)



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
    for chord in chords:
        if chord != " ":
            if chord not in NOTES:
                if chord != "-" and chord != "_" and chord!= 'm' and chord!='#' and chord!= 'b':
                    raise ValueError(f"{chord} is invalid")
    return True


def generate_file_path(folder, file_name, ext):
    file_name = file_name.lower().replace(' ', '') + ext
    file_path = os.path.join(folder, file_name)
    return file_path


class Song:
    def __init__(self, name):
        self.file_path = generate_file_path('pickled_files', name, '.pk1')
        if os.path.isfile(self.file_path):
            raise ValueError("Song already exists")
        self.name = name
        self.sections = {}


    def create_section(self):
        print_line()
        section = input(
            "Enter the section name: Intro, Verse, Chorus, Instrumental, etc: "
        )
        chords = input(f"Write out the chord progression for the {section}\n")
        if is_valid_chords(chords):
            self.sections[section] = chords

    def get_title(self):
        return self.name

    def __str__(self):
        result = f"{self.name}\n\n"
        for section, chords in self.sections.items():
            result += f"{section}:\n{chords}\n"
        return result

    # Using pickle to store object
    # https://www.geeksforgeeks.org/how-to-use-pickle-to-save-and-load-variables-in-python/
    def save_song(self):
        folder = 'text_files'
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = generate_file_path(folder, self.name, '.txt')
        with open(file_path, "w") as file:
            file.write(str(self))
        self.save_song_pickle()
        prompt = f'{self.name} saved at {file_path}'
        print_animated(prompt, 0.03)

    def save_song_pickle(self):
        folder = 'pickled_files'
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.file_path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load_song(cls, name):
        file_path = generate_file_path('pickled_files', name, '.pk1')
        with open(file_path, 'rb') as file:
            result_song = pickle.load(file)
        return result_song

    def edit_section(self):
        if len(self.sections) == 0:
            print("There are no song sections yet. Consider creating new section")
            return
        print_line()
        result = "Available sections to edit: \n"
        for sec in self.sections:
            result += sec + "\n"
        print(result)

        new_sec = input("Enter a section to edit: ")
        print_line()
        if new_sec in self.sections:
            result = ''
            print(f'Editing {new_sec} Section:\n{self.sections[new_sec]}\n')
            print("Hint: You can enter nothing to delete the section")
            new_chords = input(f"Enter new chord progression for the {new_sec}:")
            if new_chords == "":
                prompt = f'Do you want to delete {new_sec}'
                del_res = get_yes_no(prompt)
                if del_res:
                    del self.sections[new_sec]
                    prompt = f'{new_sec} deleted'
                    print_animated(prompt)
                    time.sleep(1)
                    return
                else:
                    #re run the function
                    self.edit_section()
                    return
            is_valid_chords(new_chords)
            self.sections[new_sec] = new_chords
            print(f"{new_sec} updated to:\n {new_chords}")

        else:
            raise ValueError(f"Cannot find {new_sec} in {self.name}")

    """
    Transpose a song up or down(-) some number of semitones
    """

    def transpose(self):
        try:
            amount = int(
                input(
                    "Enter how number of semitones to transpose to: \nNote C to C#: 1 semitone."
                )
            )
        except ValueError:
            raise ValueError("Input was not a number.")
        else:
            for section, chords in self.sections.items():
                result = ""
                for chord in chords:
                    if chord in NOTES:
                        index = NOTES.index(chord)
                        if amount < 0:
                            amount += SIZE
                        result += NOTES[(amount + index) % SIZE]
                    else:
                        result += chord
                print(f"Chords transposed {amount} semitones")
                self.sections[section] = result


def progression():
    name = input("Name for the song: ")
    song = Song(name)

    song.create_section(section, chords)
    song.save_song()


if __name__ == "__main__":
    main()
