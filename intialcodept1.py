#testing for getting an accelerating thing to output to pd
#should play the higher notes faster
#like a guitar if you sped up near the end of the strum

### !!!! check if sending a message without a value for note will return note = 0 or note = what it was before

import mido
from timeit import default_timer

outport = mido.open_output('Pure Data Midi-In 1')
v = raw_input("velocity in m/s: ")

tstart = default_timer()

#function to get time
def getTime(tstart = tstart):
    t = default_timer() - tstart
    return t

#function to get lowest note of key chord
def getLowNote():
    c = 12
    db = 13
    d = 14
    eb = 15
    e = 16
    f = 17
    gb = 18
    g = 19
    ab = 20
    a = 21
    bb = 22
    b = 23
    key = input("what key are we in (nb, no sharps only flats (represented by b))? ")
    octave = input("what octave are we in? ")
    lowNote = key + (octave * 12)
    return lowNote    


#function to get chord being played based on button presses
def getChord(lowNote):
    I = [lowNote, lowNote + 4, lowNote + 7, lowNote + 12]
    IV = [x + 5 for x in I]
    V = [x + 7 for x in I]
    vi = [lowNote + 9, lowNote + 12, lowNote + 16, lowNote + 21]
    chordList = [I, IV, V, vi]
    buttonPress = int(raw_input("which button would you be pressing? ")) - 1
    return chordList[buttonPress]

#function to play notes
def play(v, n, chord, outport = outport, tstart = tstart):
    
    #if velocity > 0 then calculate the time until the string gets plucked
    strT = (float(0.1)/float((4*v))) - float(getTime())

    #if the string should be plucked the pluck the string
    if strT <= 0:
        msg = mido.Message('note_on', note = chord[n], channel = n, velocity = 1)
        outport.send(msg)
        played = True
    else:
        played = False
    return played

#function to turn all the notes off
def reset(outport = outport):
    for i in range(4):
        msg = mido.Message('note_off', channel = i)
        outport.send(msg)
        
#main bit of code
n = 0
lowNote = getLowNote()
chord = getChord(lowNote)

while True:
    if v > 0 and n < 4:
        played = play(v, n, chord)
        if played == True:
            tstart = default_timer()
            n += 1
    elif v < 0:
        tstart = default_timer()
        n = 0
