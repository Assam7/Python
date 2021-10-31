import atexit
import logging
import sys

from corpus import Corpus
from crawler import Crawler
from frontier import Frontier

if __name__ == "__main__":
    # Configures basic logging
    logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # Instantiates frontier and loads the last state if exists
    frontier = Frontier()
    frontier.load_frontier()

    # Instantiates corpus object with the given cmd arg
    corpus = Corpus(sys.argv[1])

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    atexit.register(frontier.save_frontier)

    # Instantiates a crawler object and starts crawling
    crawler = Crawler(frontier, corpus)
    crawler.start_crawling()
    file = open("Analytics.txt", 'w',encoding='utf-8')
    file.write("1. Keep track of the subdomains that it visited and count how many different URLs it has\n processed from each of those subdomains\n")
    for x,y in crawler.subdomainDict.items():
        file.write(f"{x}\t{y}\n")
    file.write("2. Find the page with the most valid out links (of all pages given to your crawler). Out links are the\nnumber of links that are present on a particular webpage\n")
    value2 = sorted(crawler.perPageDict.items(), key=lambda x: x[1], reverse=True)[:1]
    print("Value2",value2)
    file.write(f"The page is {value2[0][0]} with {value2[0][1]} links\n")
    file.write("3. List of downloaded URL's and Identified traps\n")
    file.write(f"{crawler.string3}")
    file.write("4. What is the longest page in terms of number of words?(HTML markup doesn't count as words)\n")
    value1 = sorted(crawler.numofwords.items(),key=lambda x:x[1],reverse=True)[:1]
    file.write(f"{value1[0][0]}\t{value1[0][1]}words\n")
    file.write("What are the 50 most common words in the entire set of pages?\n")
    mostcommon = sorted(crawler.tokensDict.items(), key=lambda x:x[1], reverse=True)[:50]
    commoncount = 0
    for k,v in mostcommon:
        commoncount+=1
        file.write(f"{commoncount}. {k}\t{v}\n")