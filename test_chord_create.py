from chord_create import Song, NOTES, SIZE, MAJOR_SCALES, MINOR_SCALES, MAJOR_CHORD, MINOR_CHORD, is_valid_chords, generate_file_path, chord, scale

import pytest

import unittest
from unittest.mock import patch

def test_file_path_generation():
    name = 'na kha tha'
    assert generate_file_path('pickled_files', name, '.pk1') == 'pickled_files\\nakhatha.pk1'

#How to mock inputs:
#https://andressa.dev/2019-07-20-using-pach-to-test-inputs/
@patch('builtins.input', side_effect= ["C", "D", "D#"])
def test_major_chords(mock_inputs):
        result1 = chord(MAJOR_CHORD)
        result2 = chord(MAJOR_CHORD)
        result3 = chord(MAJOR_CHORD)
        assert result1 == "C-E-G"
        assert result2 == "D-F#-A"
        assert result3 == "D#-G-A#"

@patch('builtins.input', side_effect= ["C", "A", "A#"])
def test_minor_chords(mock_inputs):
    assert chord(MINOR_CHORD) == "C-D#-G"
    assert chord(MINOR_CHORD) == "A-C-E"
    assert chord(MINOR_CHORD) == "A#-C#-F"


@patch('builtins.input', side_effect= ["Z", "GH"])
def test_invalid_notes(mock_inputs):
    with pytest.raises(ValueError):
        chord(MAJOR_CHORD)
        chord(MAJOR_CHORD)

@patch('builtins.input', side_effect= "C")
def test_major_scales(mock_inputs):
    assert scale(MAJOR_SCALES) == "C-D-E-F-G-A-B-C"


@patch('builtins.input', side_effect= "C")
def test_minor_scales(mock_inputs):
    assert scale(MINOR_SCALES) == "C-D-D#-F-G-G#-A#-C"


@patch('builtins.input', side_effect= ["Z", "GH"])
def test_invalid_keys(mock_inputs):
    with pytest.raises(ValueError):
        scale(MINOR_SCALES)
        scale(MAJOR_SCALES)

def test_invalid_chords():
    assert is_valid_chords("E F G") == True
    assert is_valid_chords("E-F G") == True
    assert is_valid_chords("E-Fm G#m C7") == True

    assert is_valid_chords("E S G") == False
    assert is_valid_chords("E-F GC") == False
    assert is_valid_chords("E-Fm G#m C7D") == False
    assert is_valid_chords("Invalid") == False

inputs = [
    "Verse", "C C Em F", "C C Em F" , "C C G G", "-1", 
    "Chorus", "F G C Em", "F G C Em", "F G C Em", "F F Fm G G", "-1" ,
    "2", "2", "",

    ]

@patch('builtins.input', side_effect= inputs)
def test_chord_progression(mock_inputs):
    song = Song("Untill I Found You")

    song.create_new_section()
    assert "Untill I Found You" in str(song)
    assert "Verse" in str(song)
    assert "C C Em F" in str(song)

    # create a chorus
    song.create_new_section()
    assert "Chorus" in str(song)
    assert "F F Fm G G" in str(song)

    song.transpose()
    assert "Verse" in str(song)
    assert "D D F#m G" in str(song)

    song.transpose()
    assert "Verse" in str(song)
    assert "E E G#m A" in str(song)

    #revert to original
    song.transpose()
    assert "C C Em F" in str(song)


if __name__ == "__main__":
    test_chord_progression()