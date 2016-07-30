from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from sqlite3 import IntegrityError

import Database_Info as db
from Database_getId import getOrInsertTeam


def insertMatch(matchInfo) :
	try :
		db.cursor.execute("""
			INSERT INTO Matches(url, Time, League_id, Season_id, SubCat1_id, SubCat2_id, SubCat3_id,
							Team1_id, Team2_id, Cote1, CoteN, Cote2, Result1, Result2, Winner) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """, matchInfo)
	except IntegrityError :
		print('UNIQUE URL ERROR')
	
		
def parseDate(date, hour_min) :
	date_split = date.split()
	day_month_year = date_split[1].split('.')
	
	day = int(day_month_year[0])
	month = int(day_month_year[1])
	year = int(day_month_year[2])
	
	hour_split = hour_min.split(':')
	hour = int(hour_split[0])
	min = int(hour_split[1])
	
	d = datetime(year, month, day, hour, min)
	return d.timestamp()

def getTeamCountry_Url(teamUrl) :
	elems = teamUrl.rsplit('/', 4)
	return elems[1], elems[3]
	
def crawlTeam(match) :
	team1 = match.find_element_by_xpath("td[@class='table-home']/a")
	team2 = match.find_element_by_xpath("td[@class='table-away']/a")
	
	team1Country, team1Url = getTeamCountry_Url(team1.get_attribute("href"))
	team2Country, team2Url = getTeamCountry_Url(team2.get_attribute("href"))
	
	team1_id = getOrInsertTeam(team1.text, team1Url, team1Country)
	team2_id = getOrInsertTeam(team2.text, team2Url, team2Country)
	
	return team1_id, team2_id

def crawlCotes(match) :
	cotes_div = match.find_elements_by_class_name("odds")
	
	cotes = list()
	for cote in cotes_div :
		if cote.text == "-" :
			cotes.append(None)
		else :
			cotes.append(float(cote.text))
	
	return cotes

def parseScore(score) :
	# Si le match est cancel, postp or anything return None
	if score.find('-') == -1 :
		return [None, None, None]

	results = list()
		
	scoreSplit = score.split('-')
	results += [int(scoreSplit[0]), int(scoreSplit[1][:3])]
	
	if (results[0] > results[1]) :
		results.append(1)
	elif (results[0] < results[1]) :
		results.append(2)
	else :
		results.append(0)
		
	return results
	
	
def matchLine_crawl(match, date, infoLeague) :
	# Si il ne trouve pas c'est que le match est en cours,
	# la classe est "result-stats result-live" pendant le match
	try :
		score = match.find_element_by_xpath("td[@class='result-neutral']/a")

	except NoSuchElementException :
		return
	# Result Possibility : "0 - 0" "1 - 0 pen." "1 - 0 ET" "canc." "awa." "postp."
	
	match_url = score.get_attribute("href").split('/', 4)[4]

	print(match_url)
	hour_min = match.find_element_by_class_name("datet").text
	if hour_min != "" :
		timestamp = parseDate(date, hour_min)
	else :
		timestamp = parseDate(date, "00:00")
	
	team1_id, team2_id = crawlTeam(match)
	
	cotes = crawlCotes(match)
	
	results = parseScore(score.text)
	
	matchInfo = list()
	matchInfo += [match_url, timestamp]
	matchInfo += infoLeague
	matchInfo += [team1_id, team2_id]
	matchInfo += cotes
	matchInfo += results
	
	insertMatch(matchInfo)



def matchTable_crawl(table, infoLeague) :
	dates = table.find_elements_by_xpath("thead/tr[@class]/th/span")
	tbodys = table.find_elements_by_tag_name("tbody")
	
	tlen = len(tbodys)
	print(tlen)
	for i in range(tlen) :
		date = dates[i].text
		day_matches = tbodys[i].find_elements_by_tag_name("tr")

		for match in day_matches :
			matchLine_crawl(match, date, infoLeague)