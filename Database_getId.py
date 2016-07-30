import Database_Info as db

#####FOREIGN KEY FONCTIONNE PAS


## TABLE TEAMS ##
def getTeamId(teamUrl) :
	db.cursor.execute("""SELECT id FROM Teams WHERE url = ? """, (teamUrl,))
	return db.cursor.fetchone()

def	insertTeam(teamName, teamUrl, teamCountry) :
	db.cursor.execute("""INSERT INTO Teams(Name, url, Country) VALUES(?, ?, ?) """,
									(teamName, teamUrl, teamCountry))
	return db.cursor.lastrowid

def getOrInsertTeam(teamName, teamUrl, teamCountry) :
	row = getTeamId(teamUrl)
	if row != None :
		return row['id']
	else :
		return insertTeam(teamName, teamUrl, teamCountry)
## TABLE TEAMS ##


## TABLE LEAGUES ##
def	getLeagueId(leagueUrl) :
	db.cursor.execute("""SELECT id FROM Leagues WHERE url = ? """, (leagueUrl,))
	return db.cursor.fetchone()
## TABLE LEAGUES ##

	
## TABLE SUBCATEGORIES ##
def	getSubCatId(subcatName) :
	db.cursor.execute("SELECT id FROM SubCategories WHERE Name=?", (subcatName,))
	return db.cursor.fetchone()
	# renvoie un tuple
	
def insertSubCat(subcatName) :
	db.cursor.execute("""INSERT INTO SubCategories(Name) VALUES(?) """, (subcatName,))
	return db.cursor.lastrowid

def getOrInsertSubCat(subcatName) :
	row = getSubCatId(subcatName)
	if row != None :
		return row['id']
	else :
		return insertSubCat(subcatName)
## TABLE SUBCATEGORIES ##


## TABLE SEASONS ##
def getSeasonId(leagueId, seasonName) :
	db.cursor.execute("SELECT id FROM Seasons WHERE Name = ? AND League_id = ?", (seasonName, leagueId) )
	return db.cursor.fetchone()
	
def insertSeason(leagueId, seasonName) :
	db.cursor.execute("INSERT INTO Seasons(Name, League_id) VALUES(?, ?)", (seasonName, leagueId) )
	return db.cursor.lastrowid
	
def	getOrInsertSeason(leagueId, seasonName) :
	row = getSeasonId(leagueId, seasonName)
	if row != None :
		return row['id']
	else :
		return insertSeason(leagueId, seasonName)

## TABLE SEASONS ##