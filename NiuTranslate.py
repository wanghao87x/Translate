# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 12:12:25 2020

@author: 11982
"""

import sys,time
import codecs
from selenium import webdriver
import pyperclip
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def translateNiu():

    tran_btn = drive.find_element_by_class_name('trans-button-box')
    drive.execute_script("arguments[0].scrollIntoView();", tran_btn)
    tran_btn.click()
    
    drive.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    result = drive.find_element_by_class_name('el-icon-document-copy')
    drive.execute_script("arguments[0].click();", result)
    
    webdriver.ActionChains(drive).move_to_element(result).click(result).perform()

    print(pyperclip.paste())
    result_tran = pyperclip.paste()
    time.sleep(1)
    drive.find_element_by_class_name('source-container').clear()
    return result_tran


def lang_select(lang):
    langs = {
        "zh":"中文(简体)",
        "en":"英语",
        "jp":"日语",
        "th":"泰语",
        "spa":"西班牙语",
        "ara":"阿拉伯语",
        "fra":"法语",
        "kor":"韩语",
        "ru":"俄语",
        "de":"德语",
        "pt":"葡萄牙语",
        "it":"意大利语",
        "el":"希腊语",
        "nl":"荷兰语",
        "pl":"波兰语",
        "fin":"芬兰语",
        "cs":"捷克语",
        "bul":"保加利亚语",
        "dan":"丹麦语",
        "est":"爱沙尼亚语",
        "hu":"匈牙利语",
        "rom":"罗马尼亚语",
        "slo":"斯洛文尼亚语",
        "swe":"瑞典语",
        "vie":"越南语",
        "yue":"粤语",
        "cht":"中文(繁体)",
        "wyw":"文言文"
        }
    return langs.get(lang,None)

def selectLang(text) :
    # a = unicode(i, 'utf-8')
    text = unicode(lang_select(text),'utf-8')
    # search_box = 
    drive.find_element_by_xpath('//*[@id="language"]/div[2]/div/div[1]/input').send_keys(text)
    # lang_click = 
    drive.find_element_by_xpath('//*[@id="language"]/div[2]/div/div[2]/div[1]/div/div/div/ul/li/button').click()

if __name__ == '__main__':
    # 参数输入
    # fromText: 源语言缩写
    # toText: 目标语言缩写
    # inputFile: 原文件
    # outputFile: 已翻译的文件
    # batch: 单次翻译几句
    # sleepTime: 暂停时间
    fromText = sys.argv[1]
    toText = sys.argv[2]
    inputFile = sys.argv[3]
    outputFile = sys.argv[4]
    batch = sys.argv[5]
    sleepTime = sys.argv[6]
    
    batch = int(batch)
    assert batch < 10, "Keep batch < 10!"
    sleepTime = float(sleepTime)
    # 未收录语种处理
    if lang_select(fromText) == None :
        print fromText , " 未收录"
        sys.exit(0)
    if lang_select(toText) == None :
        print toText , " 未收录"
        sys.exit(0)
    # 启动webdriver
    drive = webdriver.Chrome()  # 打开谷歌浏览器
    drive.maximize_window()     # 最大化窗口
    drive.get('https://niutrans.com/Trans?type=text')  # 打开网址
    drive.implicitly_wait(20)   # 等待页面加载

    # 选择语言
    select_bnt = drive.find_element_by_xpath('//*[@id="language"]/div/div[1]/div/p/button[5]/i').click()
    selectLang(fromText)
    select_bnt = drive.find_element_by_xpath('//*[@id="language"]/div/div[3]/div/p/button[4]/i').click()
    selectLang(toText)
    #读取文件 

    
    cnt = 0
    
    # 翻译结果
    res_list = []
    
    # 逐句读入
    with open(inputFile,'r') as f:
        for line in f:
            
            cnt = cnt + 1

        
            if cnt <= batch :
                drive.find_element_by_class_name('source-container').send_keys(unicode(line,'utf-8'))
            else:
                # 翻译 获得结果
                result = translateNiu()
                
                try:
                    length = result.count('\n')
                    print length,batch
                    assert length == batch, "数据量和结果数量不一致！"
                except AssertionError as ase:
                # if length != batch:
                    print ase
                    result = "Error\n" * batch
                # 存下结果
                res_list.append(result)
                # length = 0
                cnt = 0
                time.sleep(sleepTime)   
        # 最后剩下
        result = translateNiu()
        try:
            length = result.count('\n')
            print length,cnt
            assert length == cnt-1, "数据量和结果数量不一致！"
        except AssertionError as ase:
        # if length != batch:
            print ase
            result = "Error\n" * cnt
        res_list.append(result)
    # 关闭driver
    drive.close()

    #将翻译结果分段写入文件
    f = codecs.open(outputFile,'a+','utf-8')
    for line in res_list:
        f.write(line)

    f.write('\n')
    f.close()
