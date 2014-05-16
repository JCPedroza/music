# One octave of equal-temperament frequencies
C  = 32.703194
Db = 34.647827
D  = 36.708094
Eb = 38.890871
E  = 41.203443
F  = 43.653527
Gb = 46.249301
G  = 48.999427
Ab = 51.913085
A  = 55.000000
Bb = 58.270468
B  = 61.735410

# Dictionary <note name>: <frequency>
freqDic = {"C": C, "Db": Db, "D": D, "Eb": Eb, "E": E, "F": F,
        "Gb": Gb, "G": G, "Ab": Ab, "A": A, "Bb": Bb, "B": B}

# Array of note names
noteNames = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

def step_count(note1, note2):
    global noteNames
    count = noteNames.index(note2) - noteNames.index(note1)
    if count > 0:
        return count
    else:
        return count + len(noteNames)



