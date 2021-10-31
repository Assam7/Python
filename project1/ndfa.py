# Submitter anismail(Ismail, Assam)
import goody
from collections import defaultdict


def read_ndfa(file : open) -> {str:{str:{str}}}:
    diction = defaultdict(set)
    for line in file:
        value = line.rstrip('\n')
        value1 = value.split(';')
        original_state = value1[0]
        state = value1[2::2]
        input = value1[1:len(value)-1:2]
        z = zip(input,state)
        input_Dict = defaultdict(set)
        for input,state in set(z):
            input_Dict[input].add(state)
        diction[original_state] = input_Dict
    return diction

def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    print("The Contents of the file designating this Non-Deterministic Finite Automaton")
    string1 = ''
    for k,v in sorted(ndfa.items()):
        new = []
        for y,z in sorted(v.items()):
            Tuple_val = (y,sorted(z))
            new.append(Tuple_val)
        string1 += ("  "+k+" transitions: "+str(new)+"\n")
    return string1
    
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    track = []
    track = [state]
    state = [state]
    for x in inputs:
        possible = set()
        for current_state in state:
            if x in ndfa[current_state]:
                next_destination = (x,sorted(ndfa[current_state][x]))
                z = next_destination[1]
                possible.update(ndfa[current_state][x])
        track.append((x,possible))
        state = list(possible)
        if len(state) == 0:
            break
    return track

def interpret(result : [None]) -> str:
    print("Initiate tracing this NDFA from a start-state")
    values = result[1:]
    middle_string = ''
    string = ("Start state = "+result[0]+"\n")
    for input,destination in values:
        stop_state = sorted(destination)
        middle_string += (f"  Input = {input}; new possible states = {sorted(destination)}\n")
    stop_string = (f"Stop state(s) = {stop_state}\n")
    total_string = string + middle_string +stop_string
    return total_string





if __name__ == '__main__':
    # Write script here
    file_name = goody.safe_open("Enter the file name designating this Non-Deterministic Finite Automaton", "r", "Incorrect File! Please enter a valid file.")
    ndfa = read_ndfa(file_name)   
    string = ndfa_as_str(ndfa)
    print(string) 
    file_name1 = goody.safe_open("Enter the file name designating a sequence of start-states and their subsequent inputs", "r", "Incorrect File! Please enter a valid file.")
    for line in file_name1:
        line = line.rstrip('\n')
        value = line.split(';')
        state = value[0]
        inputs = value[1:]
        list_of_states = process(ndfa, state, inputs)
        tString = interpret(list_of_states)
        print(tString)
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
