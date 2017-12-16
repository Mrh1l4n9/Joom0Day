#By MakMan - 25-10-2015
 
import requests, re, sys
from functools import partial
from multiprocessing import Pool
 
 
def get_urls(search_string, start):
    temp        = []
    url         = 'https://www.google.com/search'
    payload     = { 'q' : search_string, 'start' : start , 'num' : '100' }
    # Set Cookies in my_headers from your browser, in case it doesn't get any results.
    my_headers  = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0', 'Cookie' : '' }
    r           = requests.get( url, params = payload, headers = my_headers )
    # print( r.text.encode('utf-8') )
    temp.extend( re.findall( '<h3 class="r"><a href="(.+?)"', r.text ) )
    # print(temp)
    return temp
 
def dork_scanner(search, pages, processes):
    result      = []
    search      = search
    pages       = pages
    processes   = int( processes )
    make_request = partial( get_urls, search )
    pagelist     = [ str(x*100) for x in range( 0, int(pages) ) ]
    with Pool(processes) as p:
        tmp = p.map(make_request, pagelist)
    for x in tmp:
        result.extend(x)
    result = list( set( result ) )
    return result
 
# Fuck You
