# Submitter anismail(Ismail, Assam)
import goody

def read_fa(file : open) -> {str:{str:str}}:
    diction = dict()
    for line in file:
        value = line.rstrip('\n')
        value1 = value.split(';')
        original_state = value1[0]
        state = value1[2::2]
        input = value1[1:len(value)-1:2]
        z = zip(input,state)
        input_dict = {}
        for k,v in list(z):
            input_dict[k] = v
        diction[original_state] = input_dict
    return (diction)
        
        
        


def fa_as_str(fa : {str:{str:str}}) -> str:
    print("The Contents of the file designating this Finite Automaton")
    string =''
    for k,v in sorted(fa.items()):
        temp = []
        for y,z in sorted(v.items()):
            new = (y,z)
            temp.append(new)
        string += ("  "+k+" transitions: "+str(temp)+"\n")
    return (string)
        

    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    temp = [state]
    for x in inputs:
        if x.isdigit() == True:
            new = (x,fa[state][x])
            state = fa[state][x]
            temp.append(new)
        else:
            print(f"Process terminated {x} is not a valid key! ({x},None)")
            temp.append((x,None))
            break
    return temp

def interpret(fa_result : [None]) -> str:
    print("Initiate tracing this FA from a start-state")
    start_string = (f"Start state = {fa_result[0]}\n")
    values = fa_result[1:]
    middle_string = ''
    for input,state in values:
        stop_state = state
        if input.isdigit() == False:
            errorString = (f"  Input = {input}; illegal input: simulation terminated\n")
            stop_state = None
        else:
            errorString = ''
            middle_string += (f"  Input = {input}; new state = {state}\n")
    stop_string = (f"Stop state = {stop_state}\n")
    total_string = start_string + middle_string+errorString+stop_string
    return total_string



if __name__ == '__main__':
    # Write script here
    file_name = goody.safe_open("Enter the file name designating this Finite Automaton", "r", "Incorrect File! Please enter a valid file.")
    print()
    fa = read_fa(file_name)
    string = fa_as_str(fa)
    print(string)
    file_name1 = goody.safe_open("Enter the file name designating a sequence of start-states and their subsequent inputs", "r", "Incorrect File! Please enter a valid file.")
    print()
    for line in file_name1:
        line = line.rstrip('\n')
        value = line.split(';')
        state = value[0]
        inputs = value[1:]
        list_of_states = process(fa, state, inputs)
        tString = interpret(list_of_states)
        print(tString)
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
