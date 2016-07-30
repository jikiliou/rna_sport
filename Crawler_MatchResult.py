from selenium.common.exceptions import NoSuchElementException
from sqlite3 import OperationalError

import Database_Info as db
from Crawler_Base import driver

saveMatchId = 1

# GERER CAS PARTICULIER DE RESULTAS FINALS | CANCEL POSTPONED AWARDED
# POUR LE MOMENT CA QUITTE JUSTE LE CRAWLING DU MATCH EN COURS

def updateMatchResult(results) :

	db.cursor.execute("""UPDATE Matches SET 
	Result1=?,
	Result2=?,
	Winner=?,
	ResultP1=?,
	ResultP2=?,
	ResultP3=?,
	ResultP4=?

	WHERE id=?;
	""", results)


def parseResultText(match_result, periods_result) :
	# Forme : (0-0, 0-0) (0-0, 0-0, 0-0, 0-0)
	results = list()
	
	splitRes = match_result.split('-')
	clean_periods = periods_result.strip('()')
	periods = clean_periods.split(',')
	
	results += [int(splitRes[0]), int(splitRes[1])]
	if (results[0] > results[1]) :
		results.append(1)
	elif (results[0] < results[1]) :
		results.append(2)
	else :
		results.append(0)
	
	for period in periods :
		results.append(period.strip())
	
	while len(results) < 7 :
		results.append(None)
	
	return results

def crawlMatchResult() :
	event_header = driver.find_element_by_css_selector("div.event-header-wrapper")
	
	# Test si le match est toujours en cours
	try :
		match_result = event_header.find_element_by_css_selector("div.event-header-score > span.result-neutral")
	except NoSuchElementException :
		return None

	periods_results = event_header.find_element_by_css_selector("div.full > p[style][xspeid]").text
	if periods_results == "" :
		return None
	
	return parseResultText(match_result.text, periods_results)
	
def	fillMatchesResult() :
	global saveMatchId
	db.cursor.execute("SELECT id, url FROM Matches WHERE Winner IS Null AND id >= ?", (saveMatchId,))
	rows = db.cursor.fetchall()

	for row in rows :
		url = "http://www.sportstats.com/soccer/" + row['url']
		print(str(row['id']) + " | " + url)
		driver.get(url)
		
		match_result = crawlMatchResult()
		
		saveMatchId = row['id']
		if match_result != None :
			
			match_result.append(row['id'])
			print(match_result)
			updateMatchResult(match_result)
			
			db.con.commit()
			
		


if __name__ == "__main__" :
	while True :
		try :
			fillMatchesResult()
			break
		except Exception as e:
			# db.con.rollback()
			print(e)
			print('\n#### CONTINUE LeagueId: '+ str(saveMatchId) + ' ####\n')
