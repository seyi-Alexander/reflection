"""import urllib2


def get_page(url):
    page = urllib2.urlopen(url)
    data= page.read()
    return data"""
import time

def time_execution(code):
    start = time.clock()
    result = eval(code)
    run_time = time.clock() - start
    return result, run_time

def spin_loop(n):
    i = 0
    while i<n:
        i = i + 1

    
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link =page.find('<a href=')
    if (start_link == -1):
        return None, 0
    start_quote = page.find('"',start_link)
    end_quote = page.find('"',start_quote+1)
    url = page[start_quote+1:end_quote]
    return url, end_quote    
    
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(p,q):
    for e in q:
        if e not in p:
           p.append(e)
           
def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph ={}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            outlink = get_all_links(content)
            graph[page] = outlink
            union(tocrawl,outlink)
            crawled.append(page)      
    return index, graph

def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]  

def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index,word,url)

def hash_string(keyword, bucket):
    count = 0
    for entry in keyword:
        count = (count + ord(entry)) % bucket
    return  count

def make_hash_table(bucket):
    table = [] 
    for unused in range(0,bucket):
        table.append([])     
    return table
    
def hashtable_get_bucket(htable,key):
    return htable[hash_string(key, len(htable))]
    
def hashtable_add(htable,key,value):
    hashtable_get_bucket(htable,key).append([key,value])
    
def hashtablbe_lookup(htable,key):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None

def hashtable_update(htable, key, value):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            entry[1]=value
            return
    bucket.append([key,value])
    
def compute_rank(graph):
    d = 0.8 #damping factor
    numloops = 10
    
    ranks  = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
        
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            # update by summing in the inlinks rank
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def lucky_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        if ranks[candidate] > ranks[best_page]:
            best_page = candidate
    return best_page

def fact(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    n * fact(n-1)
    return n

n = int(raw_input())
print fact(n)