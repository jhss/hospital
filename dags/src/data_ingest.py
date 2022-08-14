import requests
import json
import urllib.request
import xml.etree.ElementTree as et
import pandas as pd
import s3fs
import subprocess
import logging
from urllib.parse import unquote, urlencode, quote_plus

from bs4 import BeautifulSoup

def data_ingest():
    service_url = "http://apis.data.go.kr/B551182/spclMdlrtHospInfoService"
    service_op  = "getSpclMdlrtHospList"
    service_key = unquote("XBUbrtp%2F70EWXZJTwyYyNcTkkDnZhwDVXfeGIOwnYhJKBWQ0KOCxwCz3hCYGveiaCVdTldbNr0FJQk0AB7%2FJgQ%3D%3D")

    # Hospital Treatment Information
    srch_list = ["03", "04", "05", "08", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
                 "24", "25", "26", "27", "28", "29", "30", "56", "57", "58", "59", "60", "61", "62", "63", "64",
                 "71", "72", "73", "74", "99"]

    rows = []
    for srch in srch_list:
        query_params = '?' + urlencode(
            {
                "ServiceKey": service_key,
                "srchCd": srch,
                "numOfRows": 10000
            }
        )

        URL = f"{service_url}/{service_op}{query_params}"

        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'lxml-xml')

        items = soup.find_all("item")

        if len(items) == 0:
            print("There are no items")
            continue

        for item in items:
            name  = item.find("yadmNm").text
            ykiho = item.find("ykiho").text
            addr  = item.find("addr").text

            rows.append({"ykiho": ykiho, "name": name, "addr": addr, "srch": srch})


    result = pd.DataFrame(rows, columns=['ykiho', 'name', 'addr', 'srch'])
    result.to_csv("HospitalTreatment.csv")
    #subprocess.call(['aws', 's3', 'cp', 'HospitalTreatment.csv', 's3://hospital-infor'])

# Hospital Evaluation Information

    service_url_eval = "http://apis.data.go.kr/B551182/hospAsmInfoService"
    service_op = "getHospAsmInfo"

    query_params = '?' + urlencode(
        {
            "ServiceKey": service_key,
            "numOfRows": 100000
        }
    )

    URL = f"{service_url_eval}/{service_op}{query_params}"
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, 'lxml-xml')

    items = soup.find_all("item")

    rows = []

    key2int = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "등급제외": 0, "양호": 1}

    for item in items:
        name = item.find("yadmNm").text
        ykiho = item.find("ykiho").text
        item_dict = {"name": name, "ykiho": ykiho}

        for i in range(1, 24):
            key = "asmGrd{:02}".format(i)
            ret_txt = item.find(key)
        
            if ret_txt != None:
                item_dict[key] = key2int[ret_txt.text]
            else:
                item_dict[key] = 0
        rows.append(item_dict)

    result = pd.DataFrame(rows, columns=rows[0].keys())
    result.to_csv("HospitalEvaluation.csv")
    #subprocess.call(['aws', 's3', 'cp', 'HospitalEvaluation.csv', 's3://hospital-infor'])


'''
service_url_cnt = "http://apis.data.go.kr/B551182/hospDiagInfoService1"
service_op = "getClinicTop5List1"
eval_data = pd.read_csv("./HospitalEvaluation.csv")

rows = []
range_list = eval_data['ykiho'].tolist()
no_item_cnt = 0

total_len = len(range_list)

f = open("top5.log", "w")

for idx in range(total_len):
    ykiho = range_list[idx]
    query_params = '?' + urlencode(
        {
            "ServiceKey": service_key,
            "numOfRows": 100,
            "pageNo": 1,
            "ykiho": ykiho
        }
    )
    URL = f"{service_url_cnt}/{service_op}{query_params}"

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml-xml')
    items = soup.find_all("item")
    
    f.write(response.text + "\n")

    if len(items) == 0: 
        no_item_cnt += 1
        continue

    if (idx+1) % 100 == 0:
        print(f"{idx} .........\n\n {items}")

    for item in items:
        year = item.find("crtrYm")
        
        top5 = []
        for i in range(1, 6):
            element = item.find(f"mfrnIntrsIlnsCdNm{i}")

            if element == None: continue
            top5.append(element.text)

        if (idx+1) % 100 == 0:
            print(top5)
        name = eval_data[eval_data['ykiho'] == ykiho]['name'].values[0]
        rows.append({"name": name, "ykiho": ykiho, "top5": top5})


f.close()
print(f"no_item_cnt: {no_item_cnt}")
result = pd.DataFrame(rows, columns = rows[0].keys())
result.to_csv("HospitalTop5_final.csv")
'''
