from selenium import webdriver
import re
import time
import pickle
scrap_session = None
loadsigns = ['-', '\\', '|', '/']
try:
    with open('ScrapBot.cookie', 'rb') as cookiefile:  # tries to open and load the cookie file
        cookies = pickle.load(cookiefile)
    for cookie in cookies:  # it searches for the cookie needed and sets scrap_session to that cookie
        if cookie['name'] == 'scr_session':
            scrap_session = {'name': 'scr_session',
                             'value': cookie['value'],
                             'secure': True}
            print('Cookies loaded.')
            break
except:
    print('No cookie file was found.')
driver = webdriver.Chrome()  # opens Google Chrome
driver.get('https://scrap.tf/')

if scrap_session:  # it loads the cookie if it was found
    driver.add_cookie(scrap_session)
    driver.get('https://scrap.tf/login/')
    driver.get('https://scrap.tf/raffles/')


def Savecookies():  # saves all cookies found
    with open('ScrapBot.cookie', 'wb') as cookiefile:
        pickle.dump(driver.get_cookies(), cookiefile)
    print('The cookies were saved in the \'ScrapBot.cookie\' file.')


def Rafflebot():
    rafflesURL = []
    currentraffle = 1
    rafflesjoined = 0
    moreraffles = True
    loadsignindex = 0
    driver.get('https://scrap.tf/raffles/')
    while moreraffles:  # scrolls to the bottom of the page to be able to look for all raffles
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        print('Scrolling to the bottom of the page.' +
              loadsigns[loadsignindex % 4], end='\r')
        loadsignindex += 1
        try:
            if re.findall('(:?That\'s all, no more!)|(:?Error loading more raffles.)', driver.page_source.encode('cp850', 'replace').decode('cp850')):
                moreraffles = False
        except:
            pass
    # it will use regex to find all raffles on the page
    matches = re.findall(
        '<div class=\"panel-raffle\" id=\"raffle-box-[A-Z0-9]{6}\" style=\"(?!opacity: \.6;)\">\s+<div class=\"panel-heading \"><div class="raffle-name">(?:<i class.+</i> )?<a href=\"(/raffles/[a-zA-z0-9]{6})\">(.+)</a></div>', driver.page_source.encode('cp850', 'replace').decode('cp850'))
    # it will now print all raffles on the screen then add the url to them to a
    # list
    for match in matches:
        print('https://scrap.tf' + match[0] + ' Raffle name: ' + match[1])
        rafflesURL.append('https://scrap.tf' + match[0])
    print(str(len(rafflesURL)) + ' raffles found.')
    for raffle in rafflesURL:  # goes to every raffle and joins it
        print('Currently at raffle ' + str(currentraffle) +
              ' of ' + str(len(rafflesURL)))
        currentraffle += 1
        driver.get(raffle)
        time.sleep(1)
        # it uses regex to find the button to join the raffle, i am searching
        # for the whole button so it won't join a anti-bot raffle, which can be
        # entered only by bots
        button = re.search(
            '<button rel=\"tooltip-free\" data-placement=\"top\" title=\"(?:This public raffle is free to enter by anyone)?\" data-loading-text=\"Entering...\" class=\"btn btn-embossed btn-info btn-lg\" id=\"raffle-enter\" onclick=\"(ScrapTF.Raffles.EnterRaffle\(\'[A-Z0-9]{6}\', \'[a-z0-9]{64}\'\))\"(?: data-original-title="This public raffle is free to enter by anyone")?><i class=\"fa fa-sign-in\"></i> <i18n>Enter Raffle</i18n></button>', driver.page_source.encode('cp850', 'replace').decode('cp850'))
        if button:  # if the button is found it joins the raffle
            javascript = button.group(1)
            driver.execute_script('javascript:' + javascript)
            rafflesjoined += 1
            print('Raffle joined.')
            for second in range(5):
                print(str(second), end='\r')
                time.sleep(1)
        else:
            print('Can not join this raffle.')
    driver.get('https://scrap.tf/raffles/')
    print('Finished, ' + str(rafflesjoined) + ' raffles were joined.')


def continuous(rafflesleep):
    while True:
        Rafflebot()
        print('%02d:%02d' % (time.localtime().tm_hour, time.localtime().tm_min))
        time.sleep(rafflesleep * 60)
while True:
    print('Enter one of the following commands')
    print('\'/save\' to save the cookies for further use')
    print('\'/once\' to join all the raffles then stop')
    print('\'/continuous X\' to join all the raffles, wait X minutes then start again')
    while True:
        userinput = input(':')
        if userinput == ('/save'):
            Savecookies()
            continue
        elif userinput == ('/once'):
            Rafflebot()
        elif userinput[:11] == ('/continuous'):
            print('All available raffles will be joined once every ' +
                  userinput[12:] + ' minutes')
            continuous(int(userinput[12:]))
