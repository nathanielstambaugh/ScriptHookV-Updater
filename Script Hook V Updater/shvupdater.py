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

# String declarations for the various paths

#steam_s = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V\ScriptHookV.dll"
steam_s = r"C:\test\ScriptHookV.dll"
zip_s = "bin/ScriptHookV.dll"
desktop = r"C:\Users\nstam\Desktop"
# desktop = r"C:\Users\Admin\Desktop"
# gamedir = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V"
gamedir = r"C:\test"
# desktop_s = r"C:\Users\Admin\Desktop\bin\ScriptHookV.dll"
desktop_s = r"C:\Users\nstam\Desktop\bin\ScriptHookV.dll"

# This function retrieves the most recent version number available from the site hosting it
def getwebver():
    page = requests.get('http://www.dev-c.com/GTAV/scripthookv')
    soup = BeautifulSoup(page.text, "html.parser")
    anchors = soup.select("table tbody tr td table.tftablew td")
    return anchors[1].text.translate({ord("v"): None})

# This function retrieves the version of the locally installed ScriptHookV.dll file
def getlocalver(filename):
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return str(HIWORD(ms)) + "." + str(LOWORD(ms)) + "." + str(HIWORD(ls)) + "." + str(LOWORD(ls))

# This function will store the version number in a tuple using a '.' as a delimiter. This allows for easy comparison.
def versiontuple(v):
    return tuple(map(int, (v.split("."))))

# This function allows access to the windows messagebox to provide feedback to the user
def mbox(text, title, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

# This function will download the zip file from the hosting site
def download():
    url = "http://www.dev-c.com/GTAV/scripthookv"
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")  <---- Doesn't appear to download the file while in this mode
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

# This function will extract the zip file and takes the full path as an argument
def extractzip(filename):
    try:
        with zipfile.ZipFile(filename) as zip:
            zip.extract(zip_s, desktop)
            print(filename + " extracted successfully!\n")
        if os.path.exists(steam_s):
            os.remove(steam_s)
        shutil.move(desktop_s, gamedir)
        shutil.rmtree(r"C:\Users\nstam\Desktop\bin")
        # shutil.rmtree(r"C:\Users\Admin\Desktop\bin")
        print("files have been moved!\n")
    except Exception:
        print("Couldn't find " + filename)
        exit()


try:
    shzip = r"C:\Users\nstam\Downloads\ScriptHookV_" + getwebver() + ".zip"
    # shzip = r"C:\Users\Admin\Downloads\ScriptHookV_" + getwebver() + ".zip"
    if versiontuple(getwebver()) > versiontuple(getlocalver(steam_s)):
        decision = mbox("Update available! Would you like to update?", "Script Hook Updater", 4)
        if decision == 6:
            download()
            extractzip(shzip)
            mbox("ScriptHookV has been updated successfully!", "Script Hook Updater", 0)
            os.remove(shzip)
    else:
        mbox("No updates at this time", "Script Hook Updater", 0)
except:
    print("Couldn't locate the scripthook dll file. Getting ready to download it...\n")
    download()
    extractzip(shzip)
    mbox("ScriptHookV has been downloaded successfully!", "Script Hook Updater", 0)
    os.remove(shzip)
