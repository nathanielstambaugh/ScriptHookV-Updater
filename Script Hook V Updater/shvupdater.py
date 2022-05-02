import traceback
import requests
from bs4 import BeautifulSoup
from win32api import GetFileVersionInfo, LOWORD, HIWORD
import ctypes
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import os
import shutil

#steam_d = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V\dinput8.dll"
#steam_n = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V\NativeTrainer.asi"
#steam_s = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V\ScriptHookV.dll"
steam_d = r"C:\test\dinput8.dll"
steam_n = r"C:\test\NativeTrainer.asi"
steam_s = r"C:\test\ScriptHookV.dll"
zip_d = "bin/dinput8.dll"
zip_n = "bin/NativeTrainer.asi"
zip_s = "bin/ScriptHookV.dll"
desktop = r"C:\Users\nstam\Desktop"
#desktop = r"C:\Users\Admin\Desktop"
#gamedir = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V"
gamedir = r"C:\test"
#desktop_d = r"C:\Users\Admin\Desktop\bin\dinput8.dll"
#desktop_n = r"C:\Users\Admin\Desktop\bin\NativeTrainer.asi"
#desktop_s = r"C:\Users\Admin\Desktop\bin\ScriptHookV.dll"
desktop_d = r"C:\Users\nstam\Desktop\bin\dinput8.dll"
desktop_n = r"C:\Users\nstam\Desktop\bin\NativeTrainer.asi"
desktop_s = r"C:\Users\nstam\Desktop\bin\ScriptHookV.dll"



def getwebver():
    page = requests.get('http://www.dev-c.com/GTAV/scripthookv')
    soup = BeautifulSoup(page.text, "html.parser")
    anchors = soup.select("table tbody tr td table.tftablew td")
    version = anchors[1].text
    finalversion = version.translate({ord("v"): None})
    return finalversion


def getlocalver(filename):
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)


def versiontuple(v):
    return tuple(map(int, (v.split("."))))

def mbox(text,title,style):
    return ctypes.windll.user32.MessageBoxW(0,text,title,style)

def download():
    url = "http://www.dev-c.com/GTAV/scripthookv"
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    driver = webdriver.Edge(options=options)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        wait.until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Download")))
        driver.find_element(by=By.LINK_TEXT, value="Download").click()
        print("Element was clicked....\n")
        time.sleep(10)
    except:
        print("Element wasn't clicked\n")
        exit()

def extractzip(filename):
    try:
        with zipfile.ZipFile(filename) as zip:
            zip.extract(zip_d, desktop)
            zip.extract(zip_n, desktop)
            zip.extract(zip_s, desktop)
            print(filename + " extracted successfully!\n")
        if os.path.exists(steam_d):
            os.remove(steam_d)
        if os.path.exists(steam_s):
            os.remove(steam_s)
        if os.path.exists(steam_n):
            os.remove(steam_n)
        shutil.move(desktop_d, gamedir,)
        shutil.move(desktop_n, gamedir)
        shutil.move(desktop_s, gamedir)
        shutil.rmtree(r"C:\Users\nstam\Desktop\bin")
        #shutil.rmtree(r"C:\Users\Admin\Desktop\bin")
        print("files have been moved!\n")
    except Exception:
        print("Couldn't find " + filename)
        exit()



webver = getwebver()
shzip = r"C:\Users\nstam\Downloads\ScriptHookV_" + webver + ".zip"
#shzip = r"C:\Users\Admin\Downloads\ScriptHookV_" + webver + ".zip"

try:
    localver = ".".join(
    [str(i) for i in getlocalver(steam_s)])
except:
     print("Couldn't locate the scripthook dll file. Getting ready to download it...\n")
     download()
     extractzip(shzip)
     mbox("ScriptHookV has been downloaded successfully!", "Script Hook Updater", 0)
     os.remove(shzip)
     exit()

version = versiontuple(webver) > versiontuple(localver)

if version == True:
    decision = mbox("Update available! Would you like to update?", "Script Hook Updater", 4)
else:
    mbox("No updates at this time", "Script Hook Updater", 0)
    exit()

if decision == 6:
    download()
    extractzip(shzip)
    mbox("ScriptHookV has been updated successfully!", "Script Hook Updater", 0)
    os.remove(shzip)
else:
    exit()
