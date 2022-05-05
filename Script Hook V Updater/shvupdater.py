from requests import get
from bs4 import BeautifulSoup
from win32api import GetFileVersionInfo, LOWORD, HIWORD
from ctypes import windll
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
from os import remove, path
from shutil import rmtree, move
from socket import gethostname

# String declarations for the various paths based on computer name
if gethostname() == "STRIX" or gethostname() == "KG348":
    steam_s = r"C:\test\ScriptHookV.dll"
    zip_s = "bin/ScriptHookV.dll"
    desktop = r"C:\Users\nstam\Desktop"
    gamedir = r"C:\test"
    desktop_s = r"C:\Users\nstam\Desktop\bin\ScriptHookV.dll"
    bin_folder = r"C:\Users\nstam\Desktop\bin"
    downloads = r"C:\Users\nstam\Downloads\ScriptHookV_"
elif gethostname() == "DigitalStorm-PC":
    steam_s = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V\ScriptHookV.dll"
    desktop = r"C:\Users\Admin\Desktop"
    gamedir = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V"
    desktop_s = r"C:\Users\Admin\Desktop\bin\ScriptHookV.dll"
    bin_folder = r"C:\Users\Admin\Desktop\bin"
    downloads = r"C:\Users\Admin\Downloads\ScriptHookV_"


# This function retrieves the most recent version number available from the site hosting it
def getwebver():
    page = get('http://www.dev-c.com/GTAV/scripthookv')
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
    return windll.user32.MessageBoxW(0, text, title, style)

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
        # print("Element was clicked....\n")
        sleep(10)
    except:
        # print("Element wasn't clicked\n")
        exit()

# This function will extract the zip file and takes the full path as an argument
def extractzip(filename):
    try:
        with zipfile.ZipFile(filename) as zip:
            zip.extract(zip_s, desktop)
            # print(filename + " extracted successfully!\n")
        if path.exists(steam_s):
            remove(steam_s)
        move(desktop_s, gamedir)
        rmtree(bin_folder)
        # print("files have been moved!\n")
    except Exception:
        mbox("Couldn't find " + filename, "Script Hook Updater", 0)
        exit()

shzip = downloads + getwebver() + ".zip"
try:
    if versiontuple(getwebver()) > versiontuple(getlocalver(steam_s)):
        decision = mbox("Update available! Would you like to update?", "Script Hook Updater", 4)
        if decision == 6:
            download()
            extractzip(shzip)
            mbox("ScriptHookV has been updated successfully!", "Script Hook Updater", 0)
            remove(shzip)
    else:
        mbox("No updates at this time", "Script Hook Updater", 0)
except:
    mbox("Couldn't locate the scripthook dll file. Getting ready to download it", "Script Hook Updater", 0)
    download()
    extractzip(shzip)
    mbox("ScriptHookV has been downloaded successfully!", "Script Hook Updater", 0)
    remove(shzip)
