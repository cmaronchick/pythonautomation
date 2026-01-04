from music21 import stream, note, chord, meter, key, tempo, instrument, metadata, duration,environment
environment.set('musescoreDirectPNGPath', 'C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe')

# Create a score and add metadata
score = stream.Score()
score.insert(0, metadata.Metadata())
score.metadata.title = "Ride Like the Wind (Intro)"
score.metadata.composer = "Christopher Cross"

score.metadata.arranger = "Arr. by ChatGPT for Jazz Quintet"
# Key, time signature, and tempo
key_sig = key.Key('d', 'minor')
time_sig = meter.TimeSignature('4/4')
tempo_mark = tempo.MetronomeMark(number=100)

# Instruments
instruments_list = [
    instrument.Trumpet(),
    instrument.AltoSaxophone(),
    instrument.Piano(),
    instrument.Contrabass(),
    instrument.BassDrum(),
    instrument.SnareDrum(),
    instrument.HiHatCymbal()
]

# 4-bar intro vamp chords
chords_progression = [
    chord.Chord(["D4", "F4", "A4", "C5"]),     # Dm7
    chord.Chord(["C4", "E4", "G4", "B4"]),     # Cmaj7
    chord.Chord(["Bb3", "D4", "F4", "A4"]),    # Bbmaj7
    chord.Chord(["A3", "C#4", "E4", "G4"])     # A7
]

# Build parts
for instr in instruments_list:
    part = stream.Part()
    part.insert(0, instr)
    part.insert(0, key_sig)
    part.insert(0, time_sig)
    part.insert(0, tempo_mark)

    # Add 4 bars of chords
    for i in range(4):
        m = stream.Measure()
        ch = chords_progression[i % 4].closedPosition(forceOctave=4)
        ch.duration = duration.Duration(4)
        m.append(ch)
        part.append(m)

    score.append(part)

# Save to MusicXML (open in MuseScore/Finale/Sibelius to print PDF)
score.write('musicxml.pdf', fp='Ride_Like_the_Wind_Jazz_Quintet_Intro.pdf')

print("PDF created: Ride_Like_the_Wind_Jazz_Quintet_Intro.pdf")