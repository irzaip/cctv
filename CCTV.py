import urllib2
import shutil
import urlparse
import os
import subprocess
import re
import sys
import glob

myfile = ""

url_lewatmana = "http://lewatmana.com"
url_searchlewatmana = "http://lewatmana.com/cari/?q="
tosearch = raw_input("Masukkan nama Kawasan:")

#ambil kata pertama, dan capitalize
tosearch = tosearch.split(" ")[0].capitalize()

url = url_searchlewatmana + tosearch

vlc_arg = []

#remove all mp4 file
for f1 in glob.glob("*.mp4"):
  os.remove(f1)

def caricamera(url):
    #mengambil hasil dari website (namun masih ada error)
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', 'Custom User-Agent')
    w = urllib2.urlopen(req)

    #return query
    match = re.findall('cam-thumb-info.+\s+<.+="(.+)">([\w -]+)<.a>',w.read())

    #parse return query , substracting unnecessary
    result = []
    for x,y in match:
        if y.find(tosearch)>=0:
            result.append((x,y))
    
    if result:
        print result
    else:
        print "Not found"
        sys.exit()
    return result

def loadcam(url,location):
    #cari url data terakhir berkaitan dengan kamera tertentu yg spesifik
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent','Custom User-Agent')
    w = urllib2.urlopen(req)
    match = re.search(r'http.+.mp4\"',w.read())
    if match:
        print "Cam Found! : " + match.group().rstrip("\"")
        download(match.group().rstrip("\""),location)
        vlc_arg.append(str(location)+".mp4")
        return match.group().split("/").pop()
    else:
        print "Cam not found! - ERROR"

def download(url, location, fileName=None):
    def getFileName(url,openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        # if no filename was found above, parse it out of the final URL.
        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])

    r = urllib2.urlopen(urllib2.Request(url))
    try:
        #fileName = fileName or getFileName(url,r)
        fileName = location+".mp4"
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r,f)
    finally:
        r.close()

    return fileName


def playvlc(filename):
    FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
    args = "C:\\Progra~1\\VideoLAN\\VLC\\vlc.exe --fullscreen " + filename
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    return

#myfile = download('http://media.lewatmana.com/cam/smarthotel/246/videoclip20140122_145602.384.mp4')

res = caricamera(url)

for n in range(0,len(res)):
    a = loadcam(url_lewatmana+res[n][0],res[n][1])
    vlcarg = ""
    for i in vlc_arg:
        vlcarg = vlcarg + "\""+str(i)+"\" "
        
playvlc(vlcarg)
