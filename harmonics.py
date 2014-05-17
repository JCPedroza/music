# -*- coding: utf-8 -*-
# !!! Need more accurete floating point numbers?
# !!! The distance between two intervals is not linear!!! need to fix that in categorize()
import sys
import math

class IntervalResult:
    def __init__(self, name, value):
        self.name  = name
        self.value = value

def to_cents(note1, note2):
    """
    Returns the distance between two frequencies in cents.
    """
    return abs(1200 * math.log(note1/note2, 2))

def generate_harmonics(root, depth):
    """
    Returns an array with <depth> harmonics of the root frequency.
    The fundamental frequency (root) is considered the first harmonic.
    """
    harmonics = []
    for i in range(int(depth)):
        harmonics.append(root * (i + 1))
    return harmonics

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
    """
    harmonics  = generate_harmonics(root, depth)
    intervals  = generate_intervals(root)
    results    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    last       = 0
    current    = 0
    print "harmonics: ", harmonics
    print "intervals: ", intervals

    for harmonic in harmonics:
        
        # If the harmonic is out of range of the current octave, create a new list of 
        # intervals for the next octave.
        while harmonic > intervals[-1]:
            intervals = [n * 2 for n in intervals]

        # Search for the closest interval
        for interval in range(len(intervals)):
            current = harmonic - intervals[interval]                     
            if current < 0:                
                current_difference = abs(current)
                last_difference = abs(last)
                if current_difference < last_difference:                                        
                    results[interval] += 1
                else:                                        
                    results[interval - 1] += 1                                
                break
            else:
                last = current

    return results;

def print_results(root, depth):
    interval_names = ["root          ", "minor second  ", "major second  ", "minor third   ", "major third   ", "fourth        ",  
        "tritone       ", "fifth         ", "minor sixth   ", "major sixth   ", "minor seventh ", "major seventh "]
    results = categorize(root, depth)
    result_objects = []

    print "\nUnordered results:"
    for i in range(len(results)):
        print interval_names[i], results[i]
        result_objects.append(IntervalResult(interval_names[i], results[i]))
    print ""

    print "Ordered results:"
    result_objects.sort(key = lambda x: x.value, reverse = True)
    for i in result_objects:
        print i.name, i.value
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







