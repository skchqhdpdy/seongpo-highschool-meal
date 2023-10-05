from lets_common_log import logUtils as log
from config import *
import requests
import time
import json

#This file is responsible for running the web server and (mostly nothing else)
from flask import Flask, render_template, session, redirect, url_for, request, send_from_directory, jsonify
from colorama import Fore, init
import os
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
log.error(dir(config_read))
print(config_read)
def get_menu(date):
    
    apikey = "Your_API_Key"

    """ try:
        date = int(date) + int(inputDate)
        log.info(f"{inputDate}일 뒤 데이터 조회")
    except:
        log.info("당일 데이터 조회") """

    log.info(f"date = {date}")

    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?key={apikey}&type=json&pIndex=1&pSize=1&ATPT_OFCDC_SC_CODE=J10&SD_SCHUL_CODE=7530765&MLSV_FROM_YMD={date}"
    try:
        response = requests.get(url)
        result = response.json()
        menu = result["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        #필터링 ?
        menu += "<br/>"
        log.debug(menu)

        arr = []
        txt = ""
        for i in menu:
            #if i != " ":
            #log.error(i != " " or i != "<" or i != "b" or i != "r" or i != "/" or i != ">")
            if i == "<" or i == "b" or i == "r" or i == "/" or i == ">":
                if i == ">":
                    arr.append(txt)
                    txt = ""
            #elif i == "(" or i == "." or i == ")" or i.isdigit():
            #    txt += i
            else:
                txt += i
        
        """ for i in range(len(arr) // 2):
            arr.remove("") """
                
        log.debug(arr)
        menu = arr
    except:
        #menu = result["RESULT"]["CODE"] + " (" + result["RESULT"]["MESSAGE"] + ")"
        menu = result
        log.debug(url)
        log.debug(result)
    
    return menu


app = Flask(__name__)
app.secret_key = os.urandom(24) #encrypts the session cookie

@app.route("/")
def home():
    #inputDate = input("오늘 기준 으로 +, - 입력 : ")
    dateNow = time.strftime('%Y%m%d', time.localtime(time.time()))
    date = request.args.get('date')
    if date is None or date == "":
        #date = dateNow
        log.info(f"date Default set {dateNow} & Redirect")
        return redirect(url_for("home", date=dateNow))
    menu = get_menu(date)
    return render_template("test.html", title="오늘의 급식", txt=menu)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port="1337", threaded= False)