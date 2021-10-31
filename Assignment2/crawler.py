import logging
import re
import urllib
from urllib.parse import urlparse, urljoin,urldefrag
import lxml
import requests
import tldextract
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)
'''
global subdomainDict,perPageDict,history,string3,tokensDict,numofwords
subdomainDict = {}
tokensDict = {}
numofwords = {}
perPageDict = {} 
history= [] 
string3 = f""
'''
class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus):
        self.frontier = frontier
        self.corpus = corpus
        self.subdomainDict = {}
        self.tokensDict = {}
        self.numofwords = {}
        self.perPageDict = {} 
        self.history= [] 
        self.string3 = f""

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.add_url(next_link)

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        global subdomainDict,perPageDict,history,string3,tokensDict,numofwords,val
        outputLinks = []
        if url_data["http_code"] not in range(600-606) and url_data["http_code"] not in range(400-405):
            soup = BeautifulSoup(url_data["content"],"html.parser")
        allLinks = [links.get("href") for links in soup.findAll('a)',attrs={'href':re.compile("^http[s]?://")})]
        subdomainC = 0
        perPage = 0
        if url_data['is_redirected'] == True:
            url = url_data["final_url"]
        else:
            url = url_data['url']
        stopword = open("stopwords.txt", 'r')
        val=[]
        for x in stopword:
            val += x.split('\n')
        file_name = soup.getText().split()
        value1= []
        wordcount = 0
        for x in file_name:
            wordcount+=1
            if x not in val:
                if x.isalnum() == False:
                    string1 = ''
                    for char in x:
                        if char.isalnum() == True:
                            string1+=char
                        else:
                            if len(string1) >0:
                                value1.append(string1)
                            string1 = ''
                    if len(string1)>0:
                        value1.append(string1)
                else:
                    value1.append(x)
        for y in value1:
            if y.lower() not in self.tokensDict.keys():
                self.tokensDict[y.lower()] = 1
            else:
                self.tokensDict[y.lower()] +=1 
        if url not in self.numofwords.keys():
            self.numofwords[url] = wordcount
        parse = tldextract.extract(url)
        perPage = 0
        for item in soup.findAll('a',href=True):
            perPage+=1
            itemP = tldextract.extract(item['href'])
            if itemP.subdomain == parse.subdomain:
                if itemP.subdomain not in self.subdomainDict:
                    self.subdomainDict[itemP.subdomain] = 1
                else:
                    self.subdomainDict[itemP.subdomain] += 1
            data = urlparse(item['href'])
            if len(data[0]) == 0:
                if url_data['is_redirected'] == True:
                    url = url_data["final_url"]
                    tempU = urlparse(urljoin(url,item['href']))
                else:
                    url = url_data['url']
                    tempU = urlparse(urljoin(url,item['href']))
                allLinks.append(f"{tempU.scheme}://{tempU.netloc}{tempU.path}")
        if url not in self.perPageDict.keys():
            self.perPageDict[url] = perPage
        outputLinks = [urldefrag(url)[0] for url in allLinks]
        return outputLinks
        
    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        for val in link:#Avoid loops
            count = 0
            for val1 in link:
                if val == val1:
                    count+=1
            if count <=1:
                filteredfortrap.append(val1)
        print(filteredfortrap,len(filteredfortrap))
        return filteredfortrap
        """
        #global subdomainDict,perPageDict,history,string3,tokensDict,numofwords
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        try:
            if "ics.uci.edu" in parsed.hostname:
                if str(url) in self.history:
                    string3+= f"{str(url)} found in history trap\n"
                    return False
                elif len(str(url)) >= 500:
                    self.history.append(str(url))
                    self.string3+=f"{str(url)} is too long\n"
                    return False
                elif len(parsed.path)>0:
                    count = 0
                    for x in parsed.path:
                        if x == '/':
                            count+=1
                            if count>5:
                                self.history.append(str(url))
                                self.string3+=f"{str(url)} has too many repeating paths\n"
                                return False
                else:
                    self.string3 += f"{str(url)} is not a trap\n"
                    return not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())
                    
            else:
                self.history.append(str(url))
                self.string3+=f"{str(url)} does not have correct domain"
                return False

        except TypeError:
            print("TypeError for ", parsed)
            return False

