from mido import MidiFile

import sys

def get_note_sequence(file):
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
            note_sequence[index] = (msg.note, note_sequence[index][1], time)
            del current_notes[msg.note]

    return note_sequence

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: {} <midi file>'.format(sys.argv[0]))
		
    note_sequence = get_note_sequence(sys.argv[1])
    print(note_sequence)
