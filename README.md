## Introduction
A web application for catalog management. The Item Catalog web application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

###Program Features.
	
1. ** Responsive Web Interface: ** The web interface for the application is responsive and supports multiple screen sizes.
1. ** Administration Module: ** Application supports an administration module. If your are logged in as an Administrator you can add new categories and modify items posted by any user. Admin user can enable and disable users, categories and items. 
   ** Default Login Information for Administrator **

| User Name | admin@itemcatalog.com |
|:---------:|:---------------------:|
|  Password |         123456        | 

1. ** Sub-Categories: ** Application supports one level of sub categories Like the category Electronics and Computers  can have sub categories Headphones, Video Games , Laptops and Tablets.
1. ** Pagination: ** Pagination of results for easy readability on most of the pages.
1. ** Moderation: ** Administrator can enable and disable users, categories and items. The disabled items and categories will not show up in the catalog but will still be available in the users 
1. ** Third Party Login :** The application allows you to use you google account to login.
1. ** CRUD :** The application allows a logged in user to perform CRUD operations on their items. An administrator can update all items.
1. ** Item Images :** The application allows a logged in user to specify a picture / image url for there items these images are used in the listings.
1. ** Latest Items :** The application displays latest items in a carousel on the home page. The number of Items and the cut of date can be changed in code. The default values are 7 days and 9 Items.
1. ** XML Catalog :** The application has an option to get the entire catalog as an XML. You can use the following URL ** http://localhost:5000/catalog/xml ** this is assuming the server is running on port 5000



## Table of Contents

1. [Introduction ](#introduction)
	- [Program Features](#program-features)
1. [Setup ](#setup)
    - [Prerequisites ](#prerequisites)
    - [Creating The Database ](#creating-the-database)   
    - [Populate Basic Data](#populate-basic-data)   
    - [Testing ](#testing)
1. [Assumptions](#assumptions)
1. [Extra Credit Features](#extra-credit-features)
1. [Code Documentation ](#code-documentation)

1. [Database Structure ](#database-structure)
    - [Tables](#tables)
    - [Functions ](#functions)
    - [Views ](#views)

---


## Setup
### Prerequisites
1.  Python v2.7 or greater should be installed.
2.  PYTHON environment variable should be correctly set with the path to python executable.
3.  PYTHONPATH environment variable should be set with the python root folder
4.  PostgreSQL installation
5.  Vagrant installation if required 
6.  install WTForms (pip install WTForms or sudo pip install WTForms)
7.  install werkzeug version 0.8.3 (pip install werkzeug==0.8.3 or sudo pip install werkzeug==0.8.3)
8.  install flask 0.9 (pip install flask==0.9 or sudo pip install flask==0.9)
9.  install Flask-Login (pip install Flask-Login==0.1.3 or sudo pip install Flask-Login==0.1.3)
10. Clone this repository to some location on your system. 
11. A version of the database is included in the repo. In case you want to the catalog database should be created as mentioned in the [Creating The Database ](#creating-the-database) section. 
12. If you create a new datab.se please run database scripts as mentioned in the [Populate Basic Data](#populate-basic-data) section.


###Creating The Database
Asuming you are already logged in to vagrant ssh
1. Navigate to the folder where the repository has been cloned.
2. Use the `python -m src.catalogdb.database_setup` command to create a catalogdatabase.db.



###Populate Basic Data 
Asuming you are already logged in to vagrant ssh and have already created the database as mentioned in section [Creating The Database ](#creating-the-database).
1. Navigate to the folder where the repository has been cloned.
2. Use the `python -m src.catalogdb.catalog_data_script' This will insert some data and most importantly the admin user information.



## Testing

The file `tournament_test.py` contains the requited test to verify the functionality.

Some new test cases have been added to verify the additional features this version of code supports

** How to run the tests**
1. Navigate to the `tournament` folder.
1. Run the command `python tournament_test`
1. Alternatively run command `python tournament_test >> tournamentTest.log` to pipe output to a log file for easy viewing of the log.


**[Back to top](#table-of-contents)**

---

## Assumptions

1. There is no web interface required for this phase of the project.
1. This version of code support both even and odd number of players.
1. The user will have to manually switch the game number and round number whenever reporting the matches
1. The current code has been tested for up to 3 rounds and 3 games per round.
1. When paring the code randomly decides who plays who within the same score group and if there are odd number of players it pushes the first player form the group to the next lower scoring group
1. If there are odd Number of players one of the player receives  a bye win and rest are randomly matched 
1. Most of the scoring and paring logic is based of [SWISS-STYLE PAIRING SYSTEM ](http://www.wizards.com/dci/downloads/swiss_pairings.pdf) by the wizards of the coasts.
1. The test cases have been modified for the additional features.
1. The required environment is available to run the code.
1. Delete all players used in the test cases are only for housekeeping and are not mandatory to be run


**[Back to top](#table-of-contents)**

---

## Extra Credit Features

1. ** Sub-Categories: ** Application supports one level of sub categories Like the category Electronics and Computers  can have sub categories Headphones, Video Games , Laptops and Tablets.
1. ** Pagination: ** Pagination of results for easy readability on most of the pages.
1. ** Moderation: ** Administrator can enable and disable users, categories and items. The disabled items and categories will not show up in the catalog but will still be available in the users 
1. ** Item Images :** The application allows a logged in user to specify a picture / image url for there items these images are used in the listings.
1. ** Latest Items :** The application displays latest items in a carousel on the home page. The number of Items and the cut of date can be changed in code. The default values are 7 days and 9 Items.
1. ** XML Catalog :** The application has an option to get the entire catalog as an XML. You can use the following URL ** http://localhost:5000/catalog/xml ** this is assuming the server is running on port 5000

**[Back to top](#table-of-contents)**

---
##Code Documentation

The file tournament.py is where all the code for this module is. The details of all the functions is listed below.

### calculatePlayerMatchScore(eventId, gameNumber, winnerId, loserId=None,isDraw=False, isBye=False)

Calculates the match score for a player;

* Arguments:
    * gameNumber: the gamenumber for which the scoring is done
    * eventId: the event id
    * matchId: the match Id
    * winnerId: the playerID from the eventmatches table. if it
        is a bye sent the player receiving a bye as winner
    * loserId the playerId from the eventmatches table for the
        losing player.
    * isDraw: true or false depending on if this was a draw
        or not. this
        should be null in case of a bye
    * isBye: true or false depending on if this was a bye win.
        remember only one bye is allowed per event for a player.
* Returns:
    * score = {"winnerScore": <score>, "loserScore": <score>}
        Based on the following rule.
            * 0 (zero) if this is not the last game for the match
                or match lost
            * 3 if matches won
            * 1 if the match was a draw.
            * Match won 3 points
            * Match drawn 1 point
            * Match lost 0 points


**[Back to top](#table-of-contents)**

---

### connect()
    
Connect to the PostgreSQL database.

* Returns
    * returns a database connection.

**[Back to top](#table-of-contents)**

---

### countRegisteredPlayers()
Returns the number of players currently registered.

* Returns:
    * The count of number of players currently registered.
    
**[Back to top](#table-of-contents)**

---

### countEventPlayers(eventid)

Returns the number of players currently registered for a
particular event.

* Arguments:
    * eventid: the event for which the count of players is required

* Returns:
    * The count of number of players currently registered for an event.

**[Back to top](#table-of-contents)**

---

### countEventMatches(eventId)
    
Counts the number of matches for an event.

* Arguments
    * eventId: The event Id for which the count is required.

* Returns
    * Returns the count of matches already registered.

**[Back to top](#table-of-contents)**

---

### countEventMatchesPlayed(eventId)
    
Counts the number of matches already played for an event.

* Arguments
    * eventId: The event Id for which the count is required.

* Returns
    * Returns the count of matches already registered and played.

**[Back to top](#table-of-contents)**

---

### countGamesPerRound(eventId)
    
Counts the number of games played per round for an event.

* Arguments
    * eventId: The event Id for which the count is required.

* Returns
    * Returns the count of games played per round for an event.


**[Back to top](#table-of-contents)**

---

### countRoundPerEvent(eventId)
    
Counts the number of rounds played per  event.

* Arguments
    * eventId: The event Id for which the count is required.

* Returns
    * Returns the count of rounds played per event.


**[Back to top](#table-of-contents)**

---

### createevent(eventName, rounds=1, games=1)

Create a new event and return the event ID for it

* Arguments:
    * eventName: the name of the new event
    * rounds: how many rounds will be played for an event.Defaults to 1 if not passed.  
    * games: how many games will be played for per round.Defaults to 1 if not passed.  

**[Back to top](#table-of-contents)**

---

### creategamesperround(eventId, games, DB)
    
Inserts game mapping records for eventfulness

* Arguments:
    * eventId: the event for which the games have to be mapped
    * games: the number of games that need to be added
    * DB: the database connection

**[Back to top](#table-of-contents)**

---

### createParingGroups(currentStandings)

Breaks the standings in smaller groups based on points

* Arguments
    * currentStandings : the events current standings.


**[Back to top](#table-of-contents)**

---

### createParings(currentStandings, eventId)

Creates the parings for the event.

* Arguments
    * currentStandings : the events current standings.
    
**[Back to top](#table-of-contents)**

---

### createByeRecord(byePlayer, eventId)
    
Processes the bye record. This function will created a bye match and
then report the score for it

*  Arguments:
    
**[Back to top](#table-of-contents)**

---

### createroundsperevent(eventId, games, DB)

Inserts game mapping records for eventfulness

* Arguments:
    * eventId: the event for which the games have to be mapped
    * rounds: the number of rounds that need to be added for the
         event
    * DB: the database connection

**[Back to top](#table-of-contents)**

---

### deleteEvent(eventId)
    
Deletes the event and all related records.

* Arguments:
    * eventId: The event id for which the matches have to be deleted.
* Returns:
    * Returns the number of records deleted.

**[Back to top](#table-of-contents)**

---

### deleteMatches(eventId, matchId=None)
    
Remove all the match records from the database. if a matchId is passed
only that specific match record will be deleted.
when the match record is deleted the scores are
also deleted automatically

* Arguments:
    * eventId: The event id for which the matches have to be deleted.
    * matchId: if match id is passed only this match record is deleted.

* Returns:
    * Returns the number of records deleted.


**[Back to top](#table-of-contents)**

---

### deleteNonUniquePlayers(name)
    
If there are more than one players with the same name
this function shows the user a list of players to choose from
The user can choose "ALL" to delete all the players with a name
The user can also choose 0 to skip Deletion.
The user can select an ID to delete on of the players form the list

* Arguments:
    
**[Back to top](#table-of-contents)**

---

### deleteAllPlayers()
    
This function deletes all the registered players.

**[Back to top](#table-of-contents)**

---

### deletePlayers(playername)
    
Deletes the player records from the database with a name.

* Arguments:
    * playername: the player's full name (need not be unique).


**[Back to top](#table-of-contents)**

---

### deletePlayersByID(playerId)
    
Deletes one single player from the players table
based on the player_playerId

* Arguments:
    * playerId: the players Id that needs to be deleted

* Returns:
    * The number of records deleted

**[Back to top](#table-of-contents)**

---

### deleteUniquePlayer(name)
    
Deletes all players with a unique name.

* Arguments:
    * name: the player that has to be deleted.

* Returns:
    * the number of records deleted

**[Back to top](#table-of-contents)**

---

### getCurrentParings(eventId)
    
Fetches the list of current mappings

* Argument
    * eventId: the event Id for which the records are being inserted.

* Returns
    
**[Back to top](#table-of-contents)**

---

### getDummyUserId(eventId)

Finds and returns the eventPlayerID for the dummy user

*  Arguments:
    *  eventId : the eventId

* Returns:
    * Returns the Dummy users player Id


**[Back to top](#table-of-contents)**

---

### getEventName(eventId)
    
Finds and returns the name for the event

*  Arguments:
    *  eventId : the eventId

* Returns:
    
**[Back to top](#table-of-contents)**

---

### getIndividualPlayerStanding(eventId, playerId)
    
Get the player standing for a single player

* Arguments:
    * playerId:   the Id of the player for whom the score is required.
    * eventId:    the event for which scoring is done;
* Returns: 
    * A row with player standing

**[Back to top](#table-of-contents)**

---

### getMaxGameNumber(eventId)

Returns the max number of games allowed per match

* Arguments :
    * eventId: the event's id for which information is required.
* Returns:
    * Number of games played per round.


**[Back to top](#table-of-contents)**

---

### insertMatchRecord(eventId, paring, DB)

Inserts the match record in the event matches table

* Argument
    * eventId: the event Id for which the records are being inserted.
    * praring:  Paring for the current players
    * DB: The database connection

* Returns
    * returns the id for the current inserted record

**[Back to top](#table-of-contents)**

---

### insertPlayerScore(eventId, matchId, playerId, gameNumber, roundNumber, matchResult, gameScore, matchScore)
    
Inserts the score record for the player for a match

* Arguments:
    * eventId: the event id
    * matchId: the match Id
    * playerId: the Id for the player from the eventplayers table
    * roundNumber: the round number what is played
    * gameNumber: The game number for the round for which the score
        is recorded
    * matchResult: The result for the player won lost
        draw or bye
    * gameScore: points for the game
    
**[Back to top](#table-of-contents)**

---

### mapPlayersAndEvent(eventId, playerId)
    
Inserts a mapping record for the registered players to an event.
In this version the game number round number have to manually managed

* Arguments:
    * eventId: the event in question
    * playerId: the id of the Player to be mapped to this event

**[Back to top](#table-of-contents)**

---

### printErrorDetails(errorOccurance, messageStr=None)
    
Prints the error details
* Argument
    * errorOccurance: Error Object.
    * messageStr: Any specific message that has to be
        printed before the error details.

**[Back to top](#table-of-contents)**

---

### printPlayerScores(eventId)
    
Prints the current player standings for an event.

**[Back to top](#table-of-contents)**

---

### processDeletion(msgStr, valid_ids, name)

This function is called from deleteNonUniquePlayers function
If there are more than one players with the same name
this function shows the user a list of players to choose from
The user can choose "ALL" to delete all the players with a name
The user can also choose 0 to skip Deletion.
The user can select an ID to delete on of the players form the list

* Arguments:
    *  msgStr: the Message that needs to be displayed
    *  valid_ids: a list of valid ids that the user can choose from
    
**[Back to top](#table-of-contents)**

---

### playerStandings(eventId)

Returns a list of the players and their win records, sorted by wins.
The first entry in the list should be the player in first place for
the event, or the player tied for first place if there is currently a tie.
The results are returned sorted in the following order
totalpoints desc ,matchesplayed desc, won desc, lost desc , draw desc
ep.event_id asc, ep.player_id asc
    
* Arguments:
    * eventId: The id for the event for which the player
         standings are required.
* Returns:
    * A list of tuples, each of which contains the following:
        * event_id:The event id for the event for which the
         standings are requested
        * playerid:the player's id assigned for the event
        (assigned by the database)
        * player_name: the player's full name (as registered)
        * gamepoints: the total of gam points
        * matchpoints: the total of match points
        * totalpoints: the total score for the player
        * matchesplayed:the number of matches the player has
                    played
        * won: the number of matches the player has won
        * lost:the number of matches the player has lost
        * draw:the number of matches the player that were
                 draw
        * bye:the number of matches the player has a bye win

**[Back to top](#table-of-contents)**

---

### registerPlayer(name, email)

Adds a player to the tournament database.
The database assigns a unique serial id number for the player. This
is handled by the SQL database schema.

* Arguments:
    * name: the player's full name (need not be unique).
    * email: the email address of the player.
* Returns:
    * The new players player id

**[Back to top](#table-of-contents)**

---

### reportMatch(eventId, matchId, roundNumber, gameNumber, winnerId,loserId=None, isDraw=False, isBye=False)
    
Records the outcome of a single match between two players.
An entry for the match should exist in the event matches table.
If there are more than one rounds for games between the same players
per match, multiple entries are allowed. The games and rounds should be
mapped in the eventgamemapper and eventgamerounds.
Scoring is based on [Wizard of the Coast ](http://www.wizards.com/dci/downloads/swiss_pairings.pdf)

Games and matches are worth the following points during Swiss rounds

* Game won 3 points
* Game drawn 1 point
* Game lost 0 points
* Unfinished Game 1 point same as draw
* Unplayed Game 0 points

Status

1 'WON'
2 'LOST'
3 'DRAW'
4 'BYEWIN'

* Arguments:
    * eventId: the event id
    * matchId: the match Id
    * roundNumber: the round number what is played
    * gameNumber: The game number for the round for which the
         score is recorded
    * winnerId: the playerID from the eventmatches table
    * loserId the playerId from the eventmatches table for the
         losing player.
    * isDraw: true or false depending on if this was a draw or not
    * isBye: true or false depending on if this was a bye win.
         remember only one bye is allowed per event for a player.

**[Back to top](#table-of-contents)**

---


### randomizeGroup(group)
    
Returns the shuffled group

* Argument
        * group: List of players registered for the match

**[Back to top](#table-of-contents)**

---


### showAllPlayers()
   
Display the list of players registered can be used to when creating event mappings etc

**[Back to top](#table-of-contents)**

---

### swissPairings(eventId)
    
Pairs the players for the next round of a match and inserts the match.
records in this process.The function tries to randomly match the players with the similar match records.
 If the group of players playing in this event are odd then one players receives a bye win that is also recorded during this process.

* Arguments:
    * eventId : the event for which the standings are required
* Returns:
    * A list of tuples, each of which contains (Player1,Player2,matchId)
        * Player1: The first player's details with current standing
        * Player2: The details for the second with the current standings
        * matchId: The new matchId for the match between these players

**[Back to top](#table-of-contents)**

---


### updateMatchPlayedStatus(matchId, DB)

Updates the match played record.

* Arguments
    * matchId: the match in question for which the record is to be updated.
    * DB: The database connection

* Returns
    * Returns the number of records updated.

**[Back to top](#table-of-contents)**

---

### verifyPairs(currentPairings, newParing)
    
Checks if the new pairs are unique.

* Argument
    * currentPairings: the list of current pairs.
    * newParing: The new pairs that were just created.
* Returns
    * True or false based on the uniqueness of the pairs

**[Back to top](#table-of-contents)**

---

##Database Structure

## Tables

### TABLE resultmaster
Contains the master mappings for the different result status

* Columns and Constraints
    * id serial PRIMARY KEY
    * name TEXT NOT NULL

    1,'WON'
    2,'LOST'
    3,'DRAW'
    4,'BYEWIN'


---

### TABLE players
Contain detail of the players with their unique id. This table should always contain one record with the id 0 
with a dummy uses this is used for the bye scenarios.

* Columns and Constraints
    * player_id serial PRIMARY KEY
    * player_name Text not null
    * player_email Text

---

### TABLE events 
This table contains the names and Ids of the different events

* Columns and Constraints
    * id serial PRIMARY KEY
    * name Text NOT NULL

---
### TABLE eventplayers 
Table eventplayers Contains information of which of the registered players are playing in a  tournament

* Columns and Constraints
    * id serial UNIQUE,
    * event_id integer REFERENCES events ON DELETE CASCADE, 
    * player_id integer REFERENCES players (player_id) ON DELETE CASCADE,
    * PRIMARY KEY (event_id, player_id)

---
### TABLE eventgamemapper
Table eventgamemapper should have at least one row in this table and one row for number of games played per match

* Columns and Constraints
    * game_id serial UNIQUE
    * event_id integer REFERENCES events(id) ON DELETE CASCADE
    * game_number integer
    * PRIMARY KEY (game_number, event_id)
---

### TABLE eventgamerounds
Table eventgamerounds should have at least one row in this table and one row for number of round played per match

* Columns and Constraints
    * round_id serial UNIQUE
    * event_id integer REFERENCES events(id) ON DELETE CASCADE
    * round_number integer
    * PRIMARY KEY (round_number, event_id)

---

### TABLE eventmatches

Table eventmatches  table will contain the details for who plays against whom and for what event.
The played field is used to check if the match has been played or not

* Columns and Constraints
    * event_id integer REFERENCES events ON DELETE CASCADE
    * match_id serial UNIQUE
    * player1_id integer REFERENCES eventplayers(id) ON DELETE CASCADE
    * player2_id integer REFERENCES eventplayers(id) ON DELETE CASCADE
    * played boolean DEFAULT FALSE, PRIMARY KEY (event_id, player1_id, player2_id)

---

### TABLE playerscore
Table playerscore Table contains the score for various eventmatches for each of the players registered for the event

* Columns and Constraints
    * event_id integer REFERENCES events ON DELETE CASCADE
    * match_id integer REFERENCES eventmatches(match_id) ON DELETE CASCADE
    * player_id integer REFERENCES eventplayers(id) ON DELETE CASCADE
    * game_number integer
    * round_number integer
    * match_result integer REFERENCES resultmaster(id)
    * game_score integer DEFAULT 0
    * match_score integer DEFAULT 0
    * PRIMARY KEY (player_id,match_id,game_number,round_number)
    * FOREIGN KEY (game_number, event_id) REFERENCES eventgamemapper (game_number, event_id)
    * FOREIGN KEY (round_number, event_id) REFERENCES eventgamerounds (round_number, event_id)

---
### TABLE eventbyewinners
Table eventbyewinners contains information if any player won by a bye of free win.

* Columns and Constraints
    * event_id integer REFERENCES events(id) ON DELETE CASCADE
    * match_id integer REFERENCES eventmatches(match_id) ON DELETE CASCADE
    * player_id integer REFERENCES players ON DELETE CASCADE
    * PRIMARY KEY (event_id, player_id,match_id) 

**[Back to top](#table-of-contents)**

---

## Functions
---
### FUNCTION playercount(eventId) 

Returns the count of number of players in each event

* Arguments:
    * eventId: an integer event id.


---
### FUNCTION matchresultcount(playerId,matchResultStatus,eventId) 

Returns the count of number of occurrences for an specific player match result and event combination

* Arguments:
    * playerId: an integer  player id for which this count is required
    * matchResultStatus: and integer representing the desired status
    * eventId: an integer event id.

* Returns:
    * an integer count matching result status

---
### FUNCTION playermatchcount(player_id,event_id)
Returns the count of matches played by a player in an event

* Arguments:
    * player_id: an integer  player id for which this count is required
    * event_id: an integer event id.

* Returns:
    * an integer count the number of matches played and scored.

---
### FUNCTION getMatchCount(event_id) 
Count the number of matches for an event.

* Arguments:
    * event_id: an integer event id.

* Returns:
    * an integer count the number of matches registered for an event.


---
### FUNCTION getMatchesPlayedCount(event_id) 

Count the number of matches already played for an event.

* Arguments:
    * event_id: an integer event id.

* Returns:
    * an integer count the number of matches registered and played for an event.


---
### FUNCTION getTotalGamesCount(event_id) 
Count the number of games allowed per match for an event.

* Arguments:
    * event_id: an integer event id.

* Returns:
    * an integer count the number of games allowed per round.

---
### FUNCTION getTotalRoundsCount(event_id) 

Count the number of rounds allowed per match for an event.

* Arguments:
    * event_id: an integer event id.

* Returns:
    * an integer count the number of rounds allowed per match for an event.

**[Back to top](#table-of-contents)**

---

## VIEWS

---
### VIEW match_details 

Lists the matches along with the player name

* Returns: A list of following fields
    * event_id
    * match_id
    * player1
    * player2 

---
### VIEW player_standing 
Lists the player standings ordered by the events and other required fields

* Returns A row for each player registered for the event. with the following fields.
    * event_id
    * playerId
    * player_name
    * gamepoints: The total of game points for all the matches played for the event
    * matchpoints:  The total of all the match point for the matched played for the event 
    * totalpoints:  The total of matchpoints + gamepoints
    * matchesplayed : The number of matches played
    * won : The number of matches won
    * lost: The number of matches lost
    * draw: The number of matches bye
    * bye: The number of matches bye
    

**[Back to top](#table-of-contents)**

---


## Introduction
A simple web application for catalog management. The Item Catalog web application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

## Table of Contents

1. [Introduction ](#introduction)
1. [Setup ](#setup)
    - [Prerequisites ](#prerequisites)
    - [Creating The Database ](#creating-the-database)   
    - [Testing ](#testing)
1. [Assumptions](#assumptions)
1. [Extra Credit Features](#extra-credit-features)
1. [Code Documentation ](#code-documentation)
1. [Database Structure ](#database-structure)
    - [Tables](#tables)
    - [Functions ](#functions)
    - [Views ](#views)

---

## Setup
### Prerequisites

