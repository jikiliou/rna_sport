from selenium.common.exceptions import NoSuchElementException

import Database_Info as db
from Crawler_Base import driver, get_sleep
from Database_getId import getOrInsertSeason
# NEXT STEP
from Crawler_LeagueTabs import firstTabs

saveLeagueId = 523
saveSeasonYear = "2012"

# Il ne fait pas les leagues sans plusieurs saisons !

# (Optionel) Gerer les reprises du crawling après erreurs / coupures par saison

# (Optionel) FAIRE PARALLELISATION (Probleme sqlite mais surement gérable)

# (Optionel) GERER L'ERREUR DE MATCH UNIQUE DIFFEREMENT


		
def	getSeasons() : 
	# RENVOIE UNE LISTE DES SAISON D'UNE LEAGUE CONTENANT : URL + YEAR
	# [ {url : "fdsq", year : "0000(/0000)"}, {...} ]
	seasons_list = list()

	every_season = driver.find_elements_by_xpath("//div[@class='fakeSelectIn']/ul/li//a")

	for season in every_season :
		seasons_list.append( {"url": season.get_attribute("href"),
					"year": season.get_attribute("text").replace('/', '-') })
					
	return seasons_list
		
def	leagueSeason_crawl(leagueId, maxSeason) :
	# CRAWL TOUS LES RESULTAT D' UNE LEAGUE
	global saveSeasonYear
	
	infoLeague = [leagueId, None, None, None, None]
	seasons = getSeasons()
	
	# driver.get(seasons[0]['url'])
	# infoLeague[1] = getOrInsertSeason(leagueId, seasons[0]['year'])
	# firstTabs(infoLeague)
	
	i = 0
	for season in seasons :
		
		if i >= maxSeason :
			return
		if saveSeasonYear != "" and saveSeasonYear != season['year'] :
			continue
		saveSeasonYear = season['year']
		
		print(season['year'])
		driver.get(season['url'])
		
		infoLeague[1] = getOrInsertSeason(leagueId, season['year']) 
		firstTabs(infoLeague)
		infoLeague[1] = None
		i += 1
		
		db.con.commit()
		saveSeasonYear = ""
		
	
def leaguesCrawling() :
	global saveLeagueId
	db.cursor.execute("SELECT * FROM Leagues WHERE id >= ?", (saveLeagueId,))
	rows = db.cursor.fetchall()
	
	for row in rows :
		print(row['url'] + " ID : " + str(row['id']))
		final_url = "http://www.sportstats.com/soccer/" + row['url'] + "/results/"
		driver.get(final_url)
		saveLeagueId = row['id']
		leagueSeason_crawl(row['id'], 5)
		
		
		
	
		####### MAIN #######


if __name__ == "__main__" :
	while True :
		try :
			leaguesCrawling()
			break
		except Exception as e:
			db.con.rollback()
			print(e)
			print('\n#### CONTINUE LeagueId: '+ str(saveLeagueId) + " | " + saveSeasonYear + ' ####\n')
			
	driver.close()

