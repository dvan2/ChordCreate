from chord_create import Song, NOTES, SIZE, MAJOR_SCALES, MINOR_SCALES

import pytest

import unittest
from unittest.mock import patch

title = 'Those Eyes'
intro_chords = 'E E B B C#m C#m'

class TestSongMethods(unittest.TestCase):
    @patch('builtins.input', side_effect=['Intro', intro_chords, '-1'])
    def setUp(self, mock_inputs):
        self.song = Song(title)
        self.song.create_section()


    @patch('builtins.input', side_effect=['Intro', intro_chords, '-1'])
    def test_create_section_mock_inputs(self, mock_inputs):
        self.song.create_section()

        self.assertIn('Intro', self.song.sections.keys())
        self.assertIn(intro_chords, self.song.sections['Intro'])
    
    @patch('builtins.input', side_effect=['2'])
    def test_transpose(self, mock_inputs):
        self.song.transpose()

        self.assertIn('Intro', self.song.sections.keys())
        self.assertIn('F# F# C# C# D#m D#m', self.song.sections['Intro']) 




if __name__ == "__main__":
    unittest.main()