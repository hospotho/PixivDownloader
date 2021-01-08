from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import json
import time
import sys


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


def isLogin():
    device_token = driver.get_cookie("device_token")
    if device_token != None:
        return True
    else:
        return False


def loginPixiv():
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options, service_log_path="NUL")
    driver.get("https://www.pixiv.net/")
    print("Please login")
    while isLogin() == False:
        pass
    driver.close()
    print("login successfully, restarting in headless mode")


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
            'download [option[attributes]] [[sorts[attributes]]] Alias: "d"',
            'When not specify sorts or modify setting, no sort will be applied',
            'Option:',
            '   user /u [user_id]',
            '   artworks /a [artworks_id]',
            f'   ranking /r [daily,d,weekly,w,monthly,m,rookie,r,original,o,male,m,female,f{",male_r18,m18,female_r18,f18" if (setting["r18Mode"]==True) else ""}]',
            'Sort:',
            '   date, artworks_id [-after,-before] [date,artworks_id]',
            '   like, bookmark, view [-lmax,-lmin,-bmax,-bmin,-vmax,-vmin,] [count]', sep="\n"
        )
    elif command in ("setting", "s"):
        print(
            'setting [option[attributes]] Alias: "s"',
            'When there is no attribute, this command will display current setting',
            'Option:',
            '   reset /r [attribute,all]',
            '   modify /m [attribute] [value]', sep="\n"
        )
    elif command == "exit":
        print('exit\nExit the program')
    else:
        print('no such command')


def CommandParser(commandStr):
    if commandStr is None:
        printhelp()
        return
    if len(commandStr) == 1:
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
    if len(sys.argv) > 1 and sys.argv[1] in ("help", "h", "-h", "exit"):
        printhelp()
        sys.exit(0)
    # Initialization
    print("Program starts")
    setting = loadJson()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_argument('--incognito')
    try:
        driver = webdriver.Chrome(options=chrome_options, service_log_path="NUL")
        driver.get("https://www.pixiv.net/")
    except:
        sys.exit("Webdriver version too old, please upgrade to latest version")
    # check is there cookie for Pixiv
    if isLogin() == False:
        print("Not yet login, restarting in normal mode")
        driver.close()
        loginPixiv()
        driver = webdriver.Chrome(options=chrome_options, service_log_path="NUL")
    # start fetch command
    if len(sys.argv) > 1:
        print(">"+" ".join(sys.argv[1:]))
        CommandParser(sys.argv[1:])
    endProgram = False
    while not endProgram:
        print("Ready for new command")
        command = input(">").lower().split()
        CommandParser(command)
    input("Program ends")

    # import pdb;pdb.set_trace()
