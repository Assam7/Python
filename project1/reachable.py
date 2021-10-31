# Submitter anismail(Ismail, Assam)
import goody
import prompt
from collections import defaultdict
from goody import safe_open
from builtins import set


def read_graph(file : open) -> {str:{str}}:
    reachable_dict = defaultdict(set)
    for x in file:
        line = x.rstrip("\n")
        value = line.split(";")
        if len(value) > 1:
            reachable_dict[value[0]].add(value[1])
        else:
            reachable_dict[value[0]].add(set)
    file.close()
    return reachable_dict
def graph_as_str(graph : {str:{str}}) -> str:
    print("Graph a node -> [designating all its destination nodes]")
    string = ''
    for k,v in sorted(graph.items()):
        n = sorted(v)
        string += ("  "+k+" -> "+str(n)+"\n")
    return string
        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reach = set()
    exploring_list = [start]
    while len(exploring_list) > 0:
        node = exploring_list.pop(0)
        value = graph.get(node)
        reach.add(node)
        if value == None:
            print()
        else:
            for r in value:
                if r not in reach:
                    exploring_list.append(r)
        if trace == True:
            print("reached set = ", reach)
            print("exploring list = ",exploring_list)
            print("removing node",node,"from the exploring list; then adding it to the reached set\nafter adding all nodes reachable directly from",node,"but not already in reached, exploring =",exploring_list)
    
    print("From the node",start,"its reachable nodes:",reach)
    return reach
if __name__ == '__main__':
    # Write script here
    file = safe_open("Enter file name","r","Illegal file name!")
    diction = read_graph(file) 
    gas = graph_as_str(diction)
    print(gas)
    start = input("Enter one start node (or enter quit):")
    while start.lower() != "quit":
        while start.lower() not in diction.keys():
            print("Entry Error:",start,"; Illegal: not a source node\nPlease enter a legal String")
            start = input("Enter one start node (or enter quit):")
        trace1 = input("Enter whether or not to trace the algorithm[True]:")
        if len(trace1) == 0:
            trace1 = True
        rset = reachable(diction, start, trace1)  
        start = input("Enter one start node (or enter quit):")
    # For running batch self-tests
    import driver
    driver.default_file_name = "bsc1.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
