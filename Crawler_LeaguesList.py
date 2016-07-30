import Database_Info as db
from Crawler_Base import driver




def insertLeague(list) :
	db.cursor.executemany(
	"""INSERT INTO 	Leagues(Name, url, Country) VALUES(?, ?, ?)""", list)

def getLeagueCountry_Url(leagueUrl) :
	elems = leagueUrl.rsplit("/", 3)
	return elems[1], elems[1] + '/' + elems[2]
	
def	listLeagues_crawl() :

	table_div = driver.find_element_by_css_selector("div.clubTable.leagueTable")
	all_links = table_div.find_elements_by_xpath("table/tbody/tr/td/a")
	
	league_info = list()
	for link in all_links :
	
		name = link.get_attribute("text")
		country, url = getLeagueCountry_Url(link.get_attribute("href"))
		league_info.append([name, url, country])
	
	insertLeague(league_info)
	db.con.commit()
	
	
if __name__ == "__main__" :	
	url = "http://www.sportstats.com/soccer/leagues/"

	driver.get(url)
	listLeagues_crawl()
	driver.close()