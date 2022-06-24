import zipfile
from os import remove, path, getlogin
from shutil import rmtree, move
from socket import gethostname
from time import sleep
from win32api import HIWORD, GetFileVersionInfo, LOWORD
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# get the computer hostname
hostname = gethostname()

# String declarations for the various paths based on computer name

if hostname == "STRIX" or hostname == "TheBeast":
    print("got hostame " + hostname)
    sleep(2)
    steam_s = r"C:\test\ScriptHookV.dll"
    zip_s = "bin/ScriptHookV.dll"
    desktop = r"C:\Users\nstam\Desktop"
    gamedir = r"C:\test"
    desktop_s = r"C:\Users\nstam\Desktop\bin\ScriptHookV.dll"
    bin_folder = r"C:\Users\nstam\Desktop\bin"
    downloads = r"C:\Users\nstam\Downloads\ScriptHookV_"
    download_dir = r"C:\Users\nstam\Downloads"
elif hostname == "DigitalStorm-PC":
    print("got hostname " + hostname)
    sleep(2)
    steam_s = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V\ScriptHookV.dll"
    zip_s = "bin/ScriptHookV.dll"
    desktop = r"C:\Users\Admin\Desktop"
    gamedir = r"D:\SteamLibrary\steamapps\common\Grand Theft Auto V"
    desktop_s = r"C:\Users\Admin\Desktop\bin\ScriptHookV.dll"
    bin_folder = r"C:\Users\Admin\Desktop\bin"
    downloads = r"C:\Users\Admin\Downloads\ScriptHookV_"
    download_dir = r"C:\Users\Admin\Downloads"
else:
    print("got hostname " + hostname)
    sleep(2)
    gamedir = input("\n\nPlease enter the installation directory for GTA 5: ")
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
    print("got version " + anchors[1].text.translate(({ord("v"): None})) + " using getwebver() function")
    return anchors[1].text.translate({ord("v"): None})


# This function will enable downloads in headless mode

def enable_download(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)


# The next function retrieves the version of the locally installed ScriptHookV.dll file

def getlocalver(filename):
    print("getlocalver() called and was passed " + filename)
    info = GetFileVersionInfo(filename, "\\")
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    return str(HIWORD(ms)) + "." + str(LOWORD(ms)) + "." + str(HIWORD(ls)) + "." + str(LOWORD(ls))

# The next function will store the version number in a 4-tuple using a '.' as a delimiter.
# The map function will convert iterable objects to 'int' type


def versiontuple(v1, v2):
    print("versiontuple() called and was passed " + v1 + " and " + v2)
    t1 = tuple(map(int, (v1.split("."))))
    t2 = tuple(map(int, (v2.split("."))))
    return t1 > t2

# Download the file using browser automation libraries


def download():
    print("download() called....setting up the edge webdriver")
    sleep(2)
    url = "http://www.dev-c.com/GTAV/scripthookv"
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Edge(options=options)
    enable_download(driver)
    print("webdriver setup complete!")
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        wait.until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Download")))
        driver.find_element(by=By.LINK_TEXT, value="Download").click()
        print("Element was clicked....waiting for download to complete")
        sleep(10)
    except:
        input(print("Element wasn't clicked....quitting program"))
        exit()

# Extract the zip file and remove any erroneous files afterwards


def extractzip(filename):
    try:
        print("extractzip() function called and was passed " + filename)
        sleep(3)
        with zipfile.ZipFile(filename) as zip:
            zip.extract(zip_s, desktop)
            print(filename + " extracted successfully!")
        if path.exists(steam_s):
            remove(steam_s)
        move(desktop_s, gamedir)
        rmtree(bin_folder)
        print("file " + desktop_s + " has been moved to " + gamedir)
        sleep(2)
    except OSError as ose:
        print("An error occurred: " + ose)
        input("Press any key to exit")
        exit()

# Assign variables to for web version and the full path of the downloaded zip file


webver = getwebver()
shzip = downloads + webver + ".zip"

# main execution block that will call all the functions to download and extract the zip file

if not path.exists(steam_s):
    inp = input("\n\nCouldn't locate the scripthook dll file. Would you like to download it? [Yy] [Nn]: ")
    if inp == 'Y' or inp == 'y':
        download()
        extractzip(shzip)
        input("ScriptHookV has been downloaded successfully!")
        remove(shzip)
    elif inp == 'N' or inp == 'n':
        input("Exiting...")
else:
    localver = getlocalver(steam_s)
    if versiontuple(webver, localver):
        inp = input("\n\nUpdate available! Would you like to update?" "[Yy] [Nn]:")
        if inp == 'Y' or inp == 'y':
            download()
            extractzip(shzip)
            remove(shzip)
            print(shzip + " has been removed")
            print("ScriptHookV has been updated successfully!")
            input("\n\nPress any key to exit")
        elif inp == 'N' or inp == 'n':
            input("Exiting...")
    else:
        input("\n\nNo updates at this time!")


