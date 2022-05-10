from requests import get
from bs4 import BeautifulSoup
from win32api import GetFileVersionInfo, LOWORD, HIWORD
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
from os import remove, path, getlogin
from shutil import rmtree, move
from socket import gethostname
import easygui
import sys

# get the computer hostname
hostname = gethostname()

# defining the bool values for command-line arguments
verbose = False

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "-v":
        verbose = True
    else:
        print("Invalid argument supplied: " + sys.argv[i])
        print("exiting...")
        exit()

# String declarations for the various paths based on computer name
if hostname == "STRIX" or hostname == "KG-348":
    if verbose:
        print("got hostame " + hostname + "....executing testing code block")
        sleep(3)
    steam_s = r"C:\test\ScriptHookV.dll"
    zip_s = "bin/ScriptHookV.dll"
    desktop = r"C:\Users\nstam\Desktop"
    gamedir = r"C:\test"
    desktop_s = r"C:\Users\nstam\Desktop\bin\ScriptHookV.dll"
    bin_folder = r"C:\Users\nstam\Desktop\bin"
    downloads = r"C:\Users\nstam\Downloads\ScriptHookV_"
    download_dir = r"C:\Users\nstam\Downloads"
elif hostname == "DigitalStorm-PC":
    if verbose:
        print("got hostname " + hostname + "....executing buzz code block")
        sleep(3)
    steam_s = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V\ScriptHookV.dll"
    desktop = r"C:\Users\Admin\Desktop"
    gamedir = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V"
    desktop_s = r"C:\Users\Admin\Desktop\bin\ScriptHookV.dll"
    bin_folder = r"C:\Users\Admin\Desktop\bin"
    downloads = r"C:\Users\Admin\Downloads\ScriptHookV_"
    download_dir = r"C:\Users\Admin\Downloads"
else:
    if verbose:
        print("got hostname " + hostname + "....executing public code block")
        sleep(3)
    easygui.msgbox("Please choose your installation directory for GTA 5", "Script Hook Updater")
    gamedir = easygui.diropenbox()
    uname = getlogin()
    steam_s = gamedir + "\\" + "ScriptHookV.dll"
    desktop = "C:\\Users\\" + uname + "\\Desktop"
    bin_folder = desktop + "\\bin"
    desktop_s = bin_folder + "ScriptHookV.dll"
    downloads = "C:\\Users\\" + uname + "\\Downloads\\ScriptHookV_"
    download_dir = "C:\\Users\\" + uname +"\\Downloads"

# The next function retrieves the most recent version number available from the site hosting it


def getwebver():
    page = get('http://www.dev-c.com/GTAV/scripthookv')
    soup = BeautifulSoup(page.text, "html.parser")
    anchors = soup.select("table tbody tr td table.tftablew td")
    if verbose:
        print("got version " + anchors[1].text.translate(({ord("v"): None})) + " using getwebver() function")
    return anchors[1].text.translate({ord("v"): None})


# This function will enable downloads in headless mode


def enable_download(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)


# The next function retrieves the version of the locally installed ScriptHookV.dll file


def getlocalver(filename):
        if verbose:
            print("getlocalver() called and was passed " + filename)
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return str(HIWORD(ms)) + "." + str(LOWORD(ms)) + "." + str(HIWORD(ls)) + "." + str(LOWORD(ls))

# The next function will store the version number in a 4-tuple using a '.' as a delimiter.
# The map function will convert iterable objects to 'int' type


def versiontuple(v1, v2):
    if verbose:
        print("versiontuple() called and was passed " + v1 + " and " + v2)
    t1 = tuple(map(int, (v1.split("."))))
    t2 = tuple(map(int, (v2.split("."))))
    if verbose:
        if t1 > t2:
            print("update is available..asking user")
        else:
            print("no update available")
    return t1 > t2

# Download the file using browser automation libraries


def download():
    url = "http://www.dev-c.com/GTAV/scripthookv"
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Edge(options=options)
    enable_download(driver)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        wait.until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Download")))
        driver.find_element(by=By.LINK_TEXT, value="Download").click()
        if verbose:
            print("Element was clicked")
        sleep(10)
    except:
        if verbose:
            print("Element wasn't clicked")
        exit()

# Extract the zip file and remove any erroneous files afterwards


def extractzip(filename):
    try:
        if verbose:
            print("extractzip() function called and was passed " + filename)
            sleep(3)
        with zipfile.ZipFile(filename) as zip:
            zip.extract(zip_s, desktop)
            if verbose:
                print(filename + " extracted successfully!")
        if path.exists(steam_s):
            remove(steam_s)
        move(desktop_s, gamedir)
        rmtree(bin_folder)
        if verbose:
            print("files have been moved!")
            sleep(3)
    except Exception:
        easygui.msgbox("Couldn't find " + filename, "Script Hook Updater", "OK")
        exit()

# Assign variables to for web version and local version and the full path of the downloaded zip file


webver = getwebver()
shzip = downloads + webver + ".zip"

# main execution block that will call all the functions to download and extract the zip file

if not path.exists(steam_s):
    easygui.msgbox("Couldn't locate the scripthook dll file. Getting ready to download it", "Script Hook Updater", "OK")
    download()
    extractzip(shzip)
    easygui.msgbox("ScriptHookV has been downloaded successfully!", "Script Hook Updater")
    remove(shzip)
    localver = getlocalver(steam_s)
else:
    localver = getlocalver(steam_s)
    if versiontuple(webver, localver):
        if easygui.ynbox("Update available! Would you like to update?", "Script Hook Updater", ["Yes", "No"]):
            if verbose:
                print("user answered yes")
            download()
            extractzip(shzip)
            easygui.msgbox("ScriptHookV has been updated successfully!", "Script Hook Updater")
            remove(shzip)
            if verbose:
                print(shzip + " has been removed")
    else:
        easygui.msgbox("No updates at this time", "Script Hook Updater", "OK")


