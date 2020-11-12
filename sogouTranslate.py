# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:06:48 2020

@author: wanghao87
"""
import os
import uuid
import math
import random
import hashlib
import re
import requests
import sys
import codecs
import time


def translateSogou(content,fromText,toText):
    print fromText,toText
    content = "".join(content)
    #构建uuid 16进制随机
    my_uuid = uuid.uuid4()
    #print my_uuid
    #构建加密算法   data['from'] + data['to'] + data['text'] + secretCode(在common.js里)   md5
    sign = '' + fromText + toText + content + '8511813095152'
    m = hashlib.md5()
    m.update(sign)
    s = m.hexdigest()
    
    data = {
        "from": fromText,
        "to": toText,
        "text": content,
        "client": "pc",
        "fr": "browser_pc",
        "pid": "sogou-dict-vr",
        "dict": "true",
        "word_group": "true",
        "second_query": "true",
        "uuid": my_uuid,
        "needQc": "1",
        "s": s,
    }
    
    #构造请求头 光user-agent不行，会返回errorcode错误 必须有referer和cookie
    url = "https://fanyi.sogou.com/reventondc/translateV2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:68.0) Gecko/20100101 Firefox/68.0",
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        #"Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://fanyi.sogou.com/?keyword=%E6%B2%A1%E9%97%AE%E9%A2%98&transfrom=auto&transto=en&model=general",
        # "Referer": "https://fanyi.sogou.com/?keyword=&transfrom=auto&transto=zh-CHS",
        
        #"Cookie": "CXID=3ACA907C05335FB83B1AC8E4B4380483; SUID=A887DC3C4D238B0A5ECF1B6500032C0D; QIDIANID=/j13mbLilO00Wq0q0ml5Sm+qnPLrfwob3EcXqKKqpJqZGnlUI6NhPgC2RGXGGZpM+6xMxFxL5Csvz3xIBUq6qQ==; usid=WE3uxKlHVQDwKdgv; SUV=001FD62FDF63AAAD5F153E38A2EEB903; ssuid=394195280; sw_uuid=7126842285; IPLOC=CN3706; ABTEST=4|1599649318|v17; SNUID=37FC915C4742E697292D760E48EBA3A1; SGINPUT_UPSCREEN=1599649319775",
        "Cookie": "ABTEST=6|1601446056|v17; SNUID=36DEFF4A787DC7F9CF28C76878D8AD34; IPLOC=CN1100; SUID=4EA9873DCE52A00A000000005F7420A8; SGINPUT_UPSCREEN=1601446062476; SUV=1601446062481; usid=TzJ9WTcUJQSdqock"
    }
    #发送请求，得到response
    res = requests.post(url=url,headers=headers,data=data).json()
    # print(res)
    #最佳结果
    print res['data']['translate']['dit'] 
    #errorcode必须==0
    print res['data']['translate']['errorCode'] 
    return res['data']['translate']['dit']



def saveRes(res):
    # length = res.count('\n')
    try:
        length = res.count('\n')
        assert length == cnt - 1, "数据量和结果数量不一致！"
    except AssertionError as ase:
        print ase
        res = "Error\n" * (cnt-1) + "Error"
    #将翻译结果分段写入文件
    f = codecs.open(outputFile, 'a+', 'utf-8')
    f.write(res)
    f.write('\n')
    f.close()
    


def lang_select(lang):
    langs = {
        "zh":"zh-CHS",
        "en":"en",
        "jp":"ja",
        "th":"th",
        "spa":"es",
        "ara":"ar",
        "fra":"fr",
        "kor":"ko",
        "ru":"ru",
        "de":"de",
        "pt":"pt",
        "it":"it",
        "el":"el",
        "nl":"nl",
        "pl":"pl",
        "fin":"fi",
        "cs":"cs",
        "bul":"bg",
        "dan":"da",
        "est":"et",
        "hu":"hu",
        "rom":"ro",
        "slo":"sl",
        "swe":"sv",
        "vie":"vi",
        "yue":"yue",
        "cht":"zh-CHT"
        # "wyw":"文言文"
        }
    return langs.get(lang,None)

        



if __name__ == '__main__':
    # 参数输入
    # batch: 单次翻译几句
    # sleepTime: 暂停时间
    # fromText: 源语言缩写
    # toText: 目标语言缩写
    # inputFile: 原文件
    # outputFile: 已翻译的文件
    fromText = sys.argv[1]
    toText = sys.argv[2]
    inputFile = sys.argv[3]
    outputFile = sys.argv[4]
    batch = sys.argv[5]
    sleepTime = sys.argv[6]

    batch = int(batch)
    assert batch < 10, "Keep batch<10!"
    sleepTime = float(sleepTime)
    # 未收录语种处理
    if lang_select(fromText) == None :
        print fromText , " 语种未收录"
        sys.exit(0)
    if lang_select(toText) == None :
        print toText , " 语种未收录"
        sys.exit(0)
    fromText = lang_select(fromText)
    toText = lang_select(toText)

    
    cnt = 0
    content_list = []
    #对每个句子循环执行翻译并保存结果到列表
    # res_list = []
    # 逐句读入
    with open(inputFile,'r') as f:
        for line in f:   
            content_list.append(line)
            cnt = cnt + 1
            
            if cnt == batch :
                result = translateSogou(content_list,fromText,toText)
                saveRes(result)
                
                # 准备下一次循环
                cnt = 0 
                content_list = []
                # 暂停
                time.sleep(sleepTime)
        
        # 剩下的不足Batch量的
        result = translateSogou(content_list,fromText,toText)
        
        # print result
        saveRes(result)
        

