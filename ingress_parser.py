import cookielib
import json
import mechanize
import requests
import re
from math import pi, cos, tan, radians, log

GOOGLE_USER = '__________@gmail.com'
GOOGLE_PASS = '____________'
LAT = 43.668104
LONG =  -79.778139
ZOOM = 15

def calc_tile(lng, lat, zoomlevel):
    tilecounts = [1,1,1,40,40,80,80,320,1E3,2E3,2E3,4E3,8E3,16E3,16E3,32E3]
    rlat = radians(lat)
    tilecount = tilecounts[zoomlevel]
    xtile = int((lng + 180.0) / 360.0 * tilecount)
    ytile = int((1.0 - log(tan(rlat) + (1 / cos(rlat))) / pi) / 2.0 * tilecount)
    return xtile, ytile

def getLocations(lng, lat):
    LONG = lng
    LAT = lat
    cookiejar = cookielib.LWPCookieJar()
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.set_cookiejar(cookiejar)
    browser.addheaders = [('User-agent', 'Firefox')]

    browser.open('http://ingress.com/intel')
    for link in browser.links(url_regex='ServiceLogin'):
        browser.follow_link(link)

        browser.select_form(nr=0)
        browser.form['Email'] = GOOGLE_USER
        browser.submit()

    browser.select_form(nr=0)
    browser.form['Passwd'] = GOOGLE_PASS
    response = browser.submit()

    for cookie in cookiejar:
            if cookie.name == 'SACSID':
                SACVALUE = cookie.value
            elif cookie.name == 'csrftoken':
                CSRFVALUE = cookie.value


    cookieStr = 'SACSID='+SACVALUE+'; '+'csrftoken='+CSRFVALUE+'; ingress.intelmap.shflt=viz; ingress.intelmap.lat='+str(LAT)+'; ingress.intelmap.lng='+str(LONG)+'; ingress.intelmap.zoom='+str(ZOOM)
    cookies = cookieStr.strip()

    headers = {
                'accept-encoding' :'gzip, deflate, br',
                'content-type': 'application/json; charset=UTF-8',
                'cookie': cookies,
                'origin': 'https://www.ingress.com',
                'referer': 'https://www.ingress.com/intel',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                'x-csrftoken': CSRFVALUE,
            }
    request = requests.get('https://www.ingress.com/intel', headers=headers)
    version = re.findall(r'gen_dashboard_(\w*)\.js', request.text)[0]

    url = 'https://www.ingress.com/r/getEntities'
    tileTuple = calc_tile(LONG,LAT,ZOOM) 
    #(8908, 11676)
    tilekey = str(ZOOM)+'_'+str(tileTuple[0])+'_'+str(tileTuple[1])+'_0_8_100'
    keys = [tilekey]
    data2 = {'tileKeys':keys,
             'v': version}


    finalResponse = requests.post(url, data=json.dumps(data2), headers=headers)
    jsonArr = finalResponse.json()['result']
    resultArr = []
    for key in keys:
        for i in jsonArr['map'][key]['gameEntities']:
            if len(i[2]) > 7 and isinstance(i[2][7],basestring):
                if 'http' in i[2][7]:
                    locationArr = {'latitude':i[2][2],
                                   'longitude':i[2][3],
                                   'image':i[2][7],
                                   'name':i[2][8]}
                    resultArr.append(locationArr)
    cookiejar.clear()
    browser.close()
    responseToClient = {}
    responseToClient['locations'] = resultArr
    return json.dumps(responseToClient)