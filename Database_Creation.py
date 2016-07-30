import Database_Info as db

with db.con :
	
	### TEAM TABLE ###
	db.cursor.execute("""
	CREATE TABLE	Teams
	
	(id		INTEGER PRIMARY KEY	,
	Name	TEXT				NOT NULL,
	url		TEXT UNIQUE			NOT NULL,
	Country	TEXT							);
	
	""")
	
	### SUB CATEGORY TABLE ###
	db.cursor.execute(""" 
	CREATE TABLE	SubCategories
	
	(id		INTEGER PRIMARY KEY,
	Name	TEXT				NOT NULL);
	
	""")
	
	### LEAGUE TABLE ###
	db.cursor.execute("""
	CREATE TABLE	Leagues
	
	(id		INTEGER PRIMARY KEY,
	Name	TEXT				NOT NULL,
	url		TEXT UNIQUE			NOT NULL,
	Country	TEXT							);
	
	""")
	
	### SEASON TABLE ###
	db.cursor.execute(""" 
	CREATE TABLE	Seasons
	
	(id			INTEGER PRIMARY KEY,
	Name		TEXT				NOT NULL,
	League_id	INTEGER				NOT NULL
	
	 );
	
	""")
	# FOREIGN KEY(League_id) REFERENCES Leagues(id)
	
	### MATCH TABLE ###
	db.cursor.execute("""
	CREATE TABLE	Matches
	
	(id			INTEGER PRIMARY KEY,
	url			TEXT UNIQUE			NOT NULL,
	Time		INTEGER				NOT NULL,
	
	League_id	INTEGER				NOT NULL,
	Season_id	INTEGER				NOT NULL,
	SubCat1_id	INTEGER				NOT NULL,
	SubCat2_id	INTEGER,
	SubCat3_id	INTEGER,
	
	Team1_id	INTEGER				NOT NULL,
	Team2_id	INTEGER				NOT NULL,

	Cote1		REAL,
	CoteN		REAL,
	Cote2		REAL,
	
	Winner		INTEGER,
	Result1		INTEGER,
	Result2		INTEGER,
	ResultP1	TEXT,
	ResultP2	TEXT,
	ResultP3	TEXT,
	ResultP4	TEXT
	);
	""")
	
	# FOREIGN KEY(League_id) REFERENCES Leagues(id),
	# FOREIGN KEY(Season_id) REFERENCES Seasons(id),
	# FOREIGN KEY(Subcat1_id) REFERENCES SubCategories(id),
	# FOREIGN KEY(Subcat2_id) REFERENCES SubCategories(id),
	# FOREIGN KEY(Subcat3_id) REFERENCES SubCategories(id),

	# FOREIGN KEY(Team1_id)  REFERENCES Teams(id),
	# FOREIGN KEY(Team2_id)  REFERENCES Teams(id)

	
	db.con.commit()
	
	

