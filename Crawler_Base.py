from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# firefox_capabilities = DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True
# firefox_capabilities['binary'] = "C:\\Users\\johnny\\AppData\\Local\\Programs\\Python\\Python35-32\\"

driver = webdriver.Firefox()
driver.implicitly_wait(1)

def get_sleep(url) :
	driver.get(url)
	sleep(0.1)
