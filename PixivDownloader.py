from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import json
import time
import sys
import os.path


def printJson(json_data):
    json_formatted_str = json.dumps(json_data, indent=2)
    print(json_formatted_str)


def saveJson(setting):
    with open("setting.json", "w") as f:
        json.dump(setting, f)


def loadJson():
    with open("setting.json") as f:
        data = json.loads(f.read())
        return data


def saveCookie():
    with open(os.path.dirname(__file__)+"/cookie.json", "w") as c:
        json.dump(driver.get_cookies(), c)


def loadCookie():
    global driver
    if os.path.isfile(os.path.dirname(__file__)+"/cookie.json"):
        with open(os.path.dirname(__file__)+"/cookie.json", "r") as c:
            cookies = json.load(c)
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()


def isLogin():
    cookie = driver.get_cookie("device_token")
    if cookie is None:
        return False
    try:
        driver.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/a[2]')
    except:
        return True
    else:
        return False


def loginPixiv():
    global driver
    print("Please login")
    print("Restarting in normal mode")
    driver.close()
    normal_options = Options()
    normal_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=normal_options, service_log_path="NUL")
    driver.get("https://www.pixiv.net/")
    while isLogin() == False:
        pass
    saveCookie()
    driver.close()
    print("login successfully, restarting in headless mode")
    driver = webdriver.Chrome(options=headless_options, service_log_path="NUL")
    driver.get("https://www.pixiv.net/")
    loadCookie()


def printhelp(command="help"):
    if command in ("help", "h"):
        print(
            'This is a downloader for pixiv, which based on selenium and chromedriver',
            'check help [command] for more information',
            'Command list:',
            '   help',
            '   exit',
            'Commands working in progress:',
            '   download',
            '   setting',
            '   logout',
            '   login in headless',
            '   zip',
            '   select image size',
            '   ugoira', sep="\n"
        )
    elif command in ("download", "d"):
        print(
            'download [option[attribute]] [[sorts[attributes]]] Alias: "d"',
            'When not specify sorts or modify setting, no sort will be applied',
            'Option:',
            '   user /u [user_id]',
            '   artworks /a [artworks_id]',
            '   ranking /r [daily,d,weekly,w,monthly,m,rookie,r,original,o,male,m,female,f,male_r18,m18,female_r18,f18]',
            'Sort:',
            '   date, artworks_id [-dafter,-dbefore,-aafter,-abefore] [date,artworks_id]',
            '   like, bookmark, view [-lmax,-lmin,-bmax,-bmin,-vmax,-vmin,] [count]',
            '   normal, r18 [-n,-r18]', sep="\n"
        )
    elif command in ("setting", "s"):
        print(
            'setting [option[attribute]] Alias: "s"',
            'When there is no attribute, this command will display current setting',
            'Option:',
            '   reset /r [attribute,all]',
            '   modify /m [attribute]', sep="\n"
        )
    elif command == "exit":
        print('exit\nExit the program')
    else:
        print('no such command')


def CommandParser(commandStr):
    if commandStr is None:
        printhelp()
        return
    if len(commandStr) == 1 and commandStr[0] != "exit":
        printhelp(commandStr[0])
        return
    command = commandStr[0]
    if command in ("help", "h"):
        printhelp(commandStr[1])
    if command in ("download", "d"):
        pass
    if command in ("setting", "s"):
        pass
    if command == "exit":
        global endProgram
        endProgram = True


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ("help", "h", "-h", "?", "exit"):
        printhelp()
        sys.exit(0)
    # Initialization
    print("Program starts")
    setting = loadJson()
    print("Opening chrome in headless mode")
    headless_options = Options()
    headless_options.add_argument('--headless')
    headless_options.add_argument('--disable-gpu')
    headless_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # headless_options.add_argument('--incognito')
    try:
        driver = webdriver.Chrome(options=headless_options, service_log_path="NUL")
        driver.get("https://www.pixiv.net/")
    except:
        sys.exit("Webdriver version too old, please upgrade to latest version")
    # login to Pixiv
    print("Loading cookies")
    loadCookie()
    if isLogin() == False:
        loginPixiv()
    # start fetch command
    if len(sys.argv) > 1:
        print("Command form arguments\n>"+" ".join(sys.argv[1:]))
        CommandParser(sys.argv[1:])
    endProgram = False
    while not endProgram:
        print("Ready for new command")
        command = input(">").lower().split()
        CommandParser(command)
    print("program exiting")
    try:
        driver.close()
    except:
        pass
    # import pdb;pdb.set_trace()
