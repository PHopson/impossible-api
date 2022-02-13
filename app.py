import random
import re
import string

from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask('impossible',static_folder='./build',static_url_path='')
cors = CORS(app)

@app.route('/')
def serveReact():
    return send_from_directory(app.static_folder, 'index.html')

#route for generating the MBI
@app.route('/generate/', methods=['GET'])
@cross_origin()
def generate():
    #Initialize usable characters
    rangeDigit = list(range(10))

    rangeAlpha = list(string.ascii_uppercase)
    rangeAlpha.remove("B")
    rangeAlpha.remove("I")
    rangeAlpha.remove("L")
    rangeAlpha.remove("O")
    rangeAlpha.remove("S")
    rangeAlpha.remove("Z")


    #Build the MBI string
    resString = ""
    for i in range(1,12):
        if i==1:
            resString += str( random.choice(rangeDigit[1:]) )
        elif i==2 or i==5 or i==8 or i==9:
            resString += random.choice(rangeAlpha)
        elif i==3 or i==6:
            resString += str( random.choice(rangeDigit+rangeAlpha) )
        elif i==4 or i==7 or i==10 or i==11:
            resString += str( random.choice(rangeDigit) )

    return {'MBI':resString}

#route for validation
@app.route('/verify', methods=['POST'])
@cross_origin()
def verify():
    check = request.get_json()["verify"]
    #print(check)

    #a is usable alpha characters
    #an is the combination of digits and alpha characters
    #n is digits
    a = "[AC-HJKMNPQRT-Y]"
    an = "[0-9AC-HJKMNPQRT-Y]"
    n = "[0-9]"
    
    pattMBI = "^[1-9]"+a+an+n+a+an+n+a+a+n+n+"$"
    
    if re.match(pattMBI,check):
        return {'valid':True}
    else:
        return {'valid':False}