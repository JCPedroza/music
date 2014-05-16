# !!! Need more accurete floating points?

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

# Dictionary of <note name>: <frequency>
freqDic = {"C": C, "Db": Db, "D": D, "Eb": Eb, "E": E, "F": F,
        "Gb": Gb, "G": G, "Ab": Ab, "A": A, "Bb": Bb, "B": B}

# Dictionary of <step>: <interval>
intervals = ["root", "minor second", "major second", "minor third", "major third", "fourth",  
        "tritone", "fifth", "minor sixth", "major sixth", "minor seventh", "major seventh"]

# Array of note names
noteNames = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def step_count(note1, note2):
    """
    Counts the number of steps between two notes.
    """
    global noteNames
    count = noteNames.index(note2) - noteNames.index(note1)
    if count > 0:
        return count
    else:
        return count + len(noteNames)

def step_to_interval(step):
    """
    Converts a step to an interval.
    """
    global intervals
    return intervals[step]

def generate_harmonics(root, depth):
    """
    Returns an array with <depth> harmonics of the root frequency.
    The fundamental frequency (root) is considered the first harmonic.
    """
    harmonics = []
    for i in range(depth):
        harmonics.append(root * (i + 1))
    return harmonics

def generate_intervals(root):
    """
    Generates the frequencies of the intervals of the root using
    equal-temperament. 
    """
    ratio   = 2**(1/12.0)   # ratio in equal temperament
    results = []
    value   = root
    for i in range(11):
        value = value * ratio
        results.append(value)
    return results

# def categorize(root, depth):
#     harmonics = generate_harmonics(root, depth)
#     results   = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     for i in harmonics:

print generate_intervals(32.703194)
