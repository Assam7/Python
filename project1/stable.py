# Submitter anismail(Ismail, Assam)
import goody
from collections import defaultdict

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    stable_dict = defaultdict(list)
    for x in open_file:
        line = x.rstrip("\n")
        value = line.split(";")
        original_matched = None
        stable_dict[value[0]].append(original_matched)
        stable_dict[value[0]].append(value[1:])
    return stable_dict
    open_file.close()

def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    string = ''
    for key in sorted(d, key=key, reverse=reverse):
        string += (f"  {key} -> {d[key]}\n")
    return string


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    if order.index(p1, 0, len(order)) < order.index(p2, 0, len(order)):
        return p1
    else:
        return p2
    


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    extract = set()
    for k,v in men.items():
        extract.add((k,v[0]))
    return extract


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    menDiction = men
    womenDiction = women
    if trace == True:
        mstr = dict_as_str(menDiction, key=None, reverse=False)
        wstr = dict_as_str(women, key=None, reverse=False)
        print(f"Women preferences (unchanging)\n{wstr}")
        print(f"Men preferences (current)\n{mstr}")
    unmatched = set()
    for k in menDiction.keys():
        unmatched.add(k)
    if trace == True:
        print(f"unmatched men = {unmatched}")
    while len(unmatched) > 0:
        man = unmatched.pop()
        preferences = menDiction[man][prefs]
        preferred_match = preferences.pop(0)
        if womenDiction[preferred_match][match] == None:
            menDiction[man][match] = preferred_match
            womenDiction[preferred_match][match] = man
            if trace == True:
                mstr = dict_as_str(menDiction, key=None, reverse=False)
                print(f"{man} proposes to {preferred_match}, an unmatched woman accepting the proposal")
                print(f"Men preferences (current)\n{mstr}")
                print(f"unmatched men = {unmatched}")
                
        else:
            p1 = man
            p2 = womenDiction[preferred_match][match]
            preferences1 = womenDiction[preferred_match][prefs]
            currentMatch = who_prefer(preferences1, p1, p2)
            if currentMatch == p2:
                unmatched.add(p1)
                menDiction[p1][match] = None
                menDiction[p2][match] = preferred_match
                womenDiction[preferred_match][match] = p2
                if trace == True:
                    mstr = dict_as_str(menDiction, key=None, reverse=False)
                    print(f"{p1} proposes to {p2}, a matched woman rejecting the proposal (preferring her current match)")
                    print(f"Men preferences (current)\n{mstr}")
                    print(f"unmatched men = {unmatched}")
            else:
                unmatched.add(p2)
                menDiction[p1][match] = preferred_match
                menDiction[p2][match] = None
                womenDiction[preferred_match][match] = p1
                if trace == True:
                    mstr = dict_as_str(menDiction, key=None, reverse=False)
                    print(f"{p1} proposes to {p2}, a matched woman accepting the proposal (preferring her new match)")
                    print(f"Men preferences (current)\n{mstr}")
                    print(f"unmatched men = {unmatched}")
    extract = extract_matches(menDiction)
    return extract
        
        
  


  
    
if __name__ == '__main__':
    # Write script here
    open_file = goody.safe_open("Enter the file name designating the preferences for men", 'r', error_message="Not a legal entry", default='')
    men_diction = read_match_preferences(open_file)     
    open_file1 = goody.safe_open("Enter the file name designating the preferences for women", 'r', error_message="Not a legal entry", default='')
    women_diction = read_match_preferences(open_file1)
    mstr = dict_as_str(men_diction, key=None, reverse=False)
    wstr = dict_as_str(women_diction, key=None, reverse=False)
    print(f"Men Preferences\n{mstr}")
    print(f"Women Preferences\n{wstr}")
    trace_prompt = input("Enter whether or not to trace the algorithm[True]: ")
    if len(trace_prompt) == 0:
        trace_prompt = True
    answer = make_match(men_diction, women_diction, trace=trace_prompt)
    print(f"At end of trace, the final matches = {answer}")
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
