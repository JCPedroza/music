# -*- coding: utf-8 -*-
import sys
import math

class IntervalResult:
    """
    Represents the results for one interval.
    """
    def __init__(self, name, value = 0.0, weightedValue = 0.0):
        self.name          = name
        self.value         = value
        self.weightedValue = weightedValue

def to_cents(note1, note2):
    """
    Returns the distance between two frequencies in cents.
    """
    return 1200 * math.log(note1/note2, 2)

def generate_harmonics(root, depth):
    """
    Returns an array with <depth> harmonics of the root frequency.
    The fundamental frequency (root) is considered the first harmonic.
    """
    return [root * n for n in range(1, int(depth + 1))]

def generate_intervals(root):
    """
    Generates the frequencies of the intervals of the root (including unison) using
    12 tone equal temperament. 
    """
    ratio   = 2**(1/12.0)   # ratio in equal temperament
    results = [root]
    value   = root
    for i in range(11):
        value = value * ratio
        results.append(value)
    return results

def categorize(root, depth):
    """
    Categorizes each harmonic to the closest interval.
    The weighted value is calculated using the harmonic's amplitude in a sawtooth wave:
    http://hyperphysics.phy-astr.gsu.edu/hbase/audio/geowv.html
    """
    last       = 0
    current    = 0
    harmonics  = generate_harmonics(root, depth)
    intervals  = generate_intervals(root)
    results    = [
            IntervalResult("root"),          IntervalResult("minor second"), 
            IntervalResult("major second"),  IntervalResult("minor third"), 
            IntervalResult("major third"),   IntervalResult("fourth"),
            IntervalResult("tritone"),       IntervalResult("fifth"), 
            IntervalResult("minor sixth"),   IntervalResult("major sixth"), 
            IntervalResult("minor seventh"), IntervalResult("major seventh")]

    for harmonic in range(len(harmonics)):
        
        # If the harmonic is out of range of the current octave, create a new list of
        # intervals for the next octave.
        while harmonics[harmonic] > intervals[-1]:
            intervals = [n * 2 for n in intervals]

        # Search for the closest interval
        for interval in range(len(intervals)):
            current = to_cents(harmonics[harmonic], intervals[interval])
            if current < 0:
                current_difference = abs(current)
                last_difference = abs(last)
                if current_difference < last_difference:                   
                    results[interval].value += 1
                    results[interval].weightedValue += 1 / (harmonic + 1.0)
                else:
                    results[interval - 1].value += 1
                    results[interval - 1].weightedValue += 1 / (harmonic + 1.0)
                break
            else:
                last = current

    return results;

def print_results(root, depth):
    results   = categorize(root, depth)
    precision = 3

    print "\n---- Results: ----\n"
    for i in range(len(results)):
        print "{0:<13} {1:>5} {2:<5.{precision}}".format(results[i].name, results[i].value, 
                results[i].weightedValue, precision=precision)
    print ""

    print "Ordered by total:"
    results.sort(key = lambda x: x.value, reverse = True)
    for i in results:
        print "{0:13} {1:>5}".format(i.name, i.value)
    print ""

    print "Ordered by weighted total:"
    results.sort(key = lambda x: x.weightedValue, reverse = True)
    for i in results:
        print "{0:{width}} {1:<5.{precision}}".format(i.name, i.weightedValue, width=15, precision=precision)
    print ""

if __name__ == "__main__":
    usage = "usage: python harmonics.py <root frequency> <number of harmonics>"

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
 
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    # Check for two command-line arguments.
    if len(sys.argv) != 3:
        print usage
    
    # Check that command-line arguments are numbers.
    elif not is_number(sys.argv[1]) or not is_number(sys.argv[2]):
        print usage

    # If checks are passed, perform operations
    else:
        print_results(float(sys.argv[1]), float(sys.argv[2]))







