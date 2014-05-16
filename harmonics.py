# !!! Need more accurete floating points?

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
    results = [root]
    value   = root
    for i in range(11):
        value = value * ratio
        results.append(value)
    return results

def categorize(root, depth):
    harmonics  = generate_harmonics(root, depth)
    intervals  = generate_intervals(root)
    results    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    last       = 0
    current    = 0

    for harmonic in harmonics:
        
        # If the harmonic is out of range of the current octave, create a new list of 
        # intervals for the next octave.
        if harmonic > intervals[-1]:
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

def print_unordered_results(root, depth):
    interval_names = ["root          ", "minor second  ", "major second  ", "minor third   ", "major third   ", "fourth        ",  
        "tritone       ", "fifth         ", "minor sixth   ", "major sixth   ", "minor seventh ", "major seventh "]
    results = categorize(root, depth)
    for i in range(len(results)):
        print interval_names[i], results[i]

print "55 11th harmonic: " , 55 * 11
print_unordered_results(55, 11)







