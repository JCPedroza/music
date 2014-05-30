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
        self.differences   = []

    def average_difference(self):
        if len(self.differences) > 0:
            return sum(self.differences) / float(len(self.differences))
        else:
            return False

def sums_100(n1, n2, a=0.1):
    """
    To check invariants. Checks if the sum of two numbers is close enough
    to 100.
    """
    upper_limit = 100 + a
    lower_limit = 100 - a
    the_sum     = n1 + n2
    return the_sum >= lower_limit and the_sum <= upper_limit

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

def generate_intervals(root, last_harmonic=0):
    """
    Generates the frequencies of the intervals of the root (including unison) using
    12 tone equal temperament. 
    """
    ratio     = 2**(1/12.0)   # ratio between semitones
    intervals =  [root * ratio ** i for i in range(0,12)]

    while intervals[-1] < last_harmonic:
        intervals.extend([interval * 2 for interval in intervals[-12:]])

    return intervals

def generate_intervals_JI(root, last_harmonic=0):
    """
    Genertes the frequencies of the intervals of the root (including unisong) using
    Just Intonation Pythagorean Tuning
    """
    intervals = [root, root * (256/243.0), root * (9/8.0), root * (32/27.0), 
                 root * (81/64.0), root * (4/3.0), root * (1024/729.0), 
                 root * (3/2.0), root * (128/81.0), root * (27/16.0), 
                 root * (16/9.0), root * (243/128.0)]

    while intervals[-1] < last_harmonic:
        intervals.extend([interval * 2 for interval in intervals[-12:]])

    return intervals

# !!! Can be optimized. Currently for each harmonic the loop iterates through the whole
# interval array.
def categorize(root, depth):
    """
    Categorizes each harmonic to the closest interval.
    The weighted value is calculated using the harmonic's amplitude in a sawtooth wave:
    http://hyperphysics.phy-astr.gsu.edu/hbase/audio/geowv.html
    """
    last       = 0
    current    = 0
    weight     = 1.0
    harmonics  = generate_harmonics(root, depth)
    intervals  = generate_intervals_JI(root, harmonics[-1])
    results    = [
            IntervalResult("root"),          IntervalResult("minor second"), 
            IntervalResult("major second"),  IntervalResult("minor third"), 
            IntervalResult("major third"),   IntervalResult("fourth"),
            IntervalResult("tritone"),       IntervalResult("fifth"), 
            IntervalResult("minor sixth"),   IntervalResult("major sixth"), 
            IntervalResult("minor seventh"), IntervalResult("major seventh")]

    for harmonic in range(len(harmonics)):
        
        # Search for the closest interval
        for interval in range(len(intervals)):
            current = to_cents(harmonics[harmonic], intervals[interval])
            if current < 0:
                interval_index = interval % 12
                current_difference = abs(current)
                last_difference = abs(last)
                # assert sums_100(current_difference, last_difference)
                if current_difference < last_difference:
                    assert current_difference <= 50
                    results[interval_index].value += 1
                    results[interval_index].weightedValue += 1 / (harmonic + weight)
                    results[interval_index].differences.append(current_difference)
                else:
                    assert last_difference <= 50
                    results[interval_index - 1].value += 1
                    results[interval_index - 1].weightedValue += 1 / (harmonic + weight)
                    results[interval_index - 1].differences.append(last_difference)
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

    print "\nDifferences:"
    for i in range(len(results)):
        print "{0:13}".format(results[i].name), ["{0:0.3f}".format(i) for i in results[i].differences]

    print "\nAverage difference:"
    for i in results:
        print "{0:13} {1:0.3f}".format(i.name, i.average_difference())

    print "\nOrdered by total:"
    results.sort(key = lambda x: x.value, reverse = True)
    for i in results:
        print "{0:13} {1:>5}".format(i.name, i.value)


    print "\nOrdered by weighted total:"
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







