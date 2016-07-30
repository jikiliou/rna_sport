from selenium.common.exceptions import NoSuchElementException

from Crawler_Base import driver, get_sleep
from Database_getId import getOrInsertSubCat
# NEXT STEP
from Crawler_Match import matchTable_crawl

def page_crawl(div, infoLeague) :	
	pages = div.find_elements_by_css_selector("div.clubTable > div.table-paging a[href]")
	if pages :
	
		for page in pages :
			page.click()
		
			match_table = div.find_element_by_xpath("div[@class='clubTable']//div[not(@style)]/table")
			matchTable_crawl(match_table, infoLeague)
	else :
		match_table = div.find_element_by_css_selector("div[class='clubTable'] table")
		matchTable_crawl(match_table, infoLeague)

def select_stats_container(nb) :
	selector = "div[class='stats-container']"
	for i in range(0, nb) :
		selector += " > div[class='stats-container']"

	potential_div = driver.find_elements_by_css_selector(selector)
	
	for div in potential_div :
		if div.is_displayed() :
			return div
	return None

def thirdTabs(infoLeague) :
	# Fais défiler la troisieme ligne d'onglet si elle existe
	try :
		first_tab = driver.find_element_by_xpath("//div[@class='stats-container']/div[@class='stats-container']/ul[@class='whiteTabs sub']/li[contains(@class,'tabId')]//a[@href]")

		# Pour gérer la balise strong avant le lien
		get_sleep(first_tab.get_attribute('href'))
		third_tabs = driver.find_elements_by_xpath("//div[@class='stats-container']/div[@class='stats-container']/ul[@class='whiteTabs sub']/li[contains(@class,'tabId')]//a[@href]")
		
		for tab in third_tabs :
			print(tab.text)
			infoLeague[4] = getOrInsertSubCat(tab.text)
			
			get_sleep(tab.get_attribute('href'))
			page_crawl(select_stats_container(2), infoLeague)
			
			infoLeague[4] = None
			
	except NoSuchElementException:
		page_crawl(select_stats_container(1), infoLeague)
		
def secondTabs(infoLeague) :
	# Fais défiler la seconde ligne d'onglet si elle existe
	try :
		first_tab = driver.find_element_by_xpath("//div[@class='stats-container']/ul[@class='blackTabs sub']/li[contains(@class,'tabId')]//a[@href]")

		# Pour gérer la balise strong avant le lien
		get_sleep(first_tab.get_attribute('href'))
		secondary_tabs = driver.find_elements_by_xpath("//div[@class='stats-container']/ul[@class='blackTabs sub']/li[contains(@class,'tabId')]//a[@href]")
		
		for tab in secondary_tabs :
			print(tab.text)
			infoLeague[3] = getOrInsertSubCat(tab.text)
			
			get_sleep(tab.get_attribute('href'))
			thirdTabs(infoLeague)
			
			infoLeague[3] = None
			
	except NoSuchElementException:
		page_crawl(select_stats_container(0), infoLeague)

def firstTabs(infoLeague) :
	# Fais Défiler les premiers onglets
	first_tab = driver.find_element_by_xpath("//div[@class='boxContentIn']/ul[@class='whiteTabs sub']/li[contains(@class,'tabId')]//a[@href]")
	
	# Pour gérer la balise strong avant le lien
	get_sleep(first_tab.get_attribute('href'))
	principal_tabs = driver.find_elements_by_xpath("//div[@class='boxContentIn']/ul[@class='whiteTabs sub']/li[contains(@class,'tabId')]//a[@href]")

	for tab in principal_tabs :
		print(tab.text)
		infoLeague[2] = getOrInsertSubCat(tab.text)
		
		get_sleep(tab.get_attribute('href'))
		secondTabs(infoLeague)
		
		infoLeague[2] = None