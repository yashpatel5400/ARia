"""
__authors__     = Yash, Peter, Jeff, Robert
__description__ = Reads MIDI files and returns list of notes to be played
__name__ = midi.py
"""

from mido import MidiFile
import sys
import math

import config as c

# converts from MIDI note to letter note 
# from (https://www.midikits.net/midi_analyser/midi_note_numbers_for_octaves.htm)
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def _get_note_sequence(file):
    mid = MidiFile(file)

    current_notes = {}
    note_sequence = []
    time = 0
    for msg in mid:
        if msg.type == 'note_on':
            time += msg.time
            note_sequence.append((msg.note, time, -1))
            current_notes[msg.note] = len(note_sequence)-1
        elif msg.type == 'note_off':
            time += msg.time
            index = current_notes[msg.note]
            note_sequence[index] = (NOTES[msg.note % len(NOTES)], 
                note_sequence[index][1], time)
            del current_notes[msg.note]

    return note_sequence

def _discretize(note_sequence):
    final_time = math.ceil(note_sequence[-1][-1])
    discretized = []
    for step in range(int(final_time // c.TIME_DELTA)):
        step_notes = set()
        cur_time = step * c.TIME_DELTA

        for note in note_sequence:
            if note[1] <= cur_time and note[2] > cur_time:
                step_notes.add(note[0])
        discretized.append(step_notes)
    return discretized

def get_note_times(fn):
    note_sequence = _get_note_sequence(fn)
    return _discretize(note_sequence)

if __name__ == '__main__':
    note_times = get_note_times("music/pirates.mid")
    print(note_times)