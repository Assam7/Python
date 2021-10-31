# Submitter anismail(Ismail, Assam)
import goody
from goody import irange
import prompt
from random import choice
from _collections import defaultdict


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    diction = defaultdict(list)
    
    total = []
    i = word_at_a_time(file)
    for c in i:
        total.append(c)
    for x in range(0,len(total)):
        value = []
        for y in range(0,os):
            if x+y < len(total):
                count = x+y
                value.append(total[x+y])
        key = tuple(value)
        if key not in diction.keys():
            if len(total) >count+1:
                diction[key] = [total[count+1]]
        else:
            if len(total) >count+1:
                if total[count+1] not in diction[key]:
                    diction[key].append(total[count+1])
    return diction
    
        


def corpus_as_str(corpus : {(str):[str]}) -> str:
    print(corpus)
    string = ''
    mini,maxi = 10,0
    for k,v in sorted(corpus.items()):
        string += (f"  {k} can be followed by any of {v}\n")
        minimum = len(v)
        maximum = len(v)
        if minimum <= mini:
            mini = minimum
        if maximum >= maxi:
            maxi = maximum
    string+=(f"min/max value lengths = {mini}/{maxi}\n")
    return string

def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    random_text = start
    first = start
    value1 = len(start)
    while len(random_text) < (count + value1):
        value = tuple(first)
        if value not in corpus.keys():
            random_text.append(None)
            return random_text
        else:
            randomT = choice(corpus[value])
            random_text.append(randomT)
            first = [random_text[-2],random_text[-1]]
    return random_text




        
if __name__ == '__main__':
    # Write script here
    os = int(input("Designate an order statistic: "))    
    file_name = goody.safe_open("Enter the file name designating the text to read", "r", "Incorrect File! Please enter a valid file.") 
    corpus = read_corpus(os, file_name)
    string = corpus_as_str(corpus)
    print("Corpus\n",string)
    print()
    print("Designate 2 words for start of list")
    w1 = input("Designate word 1:")
    w2 = input("Designate word 2:")
    start = [w1,w2]
    count = int(input("Designate # of words for appending to list:"))
    produce_text(corpus, start, count)
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
