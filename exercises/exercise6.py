# FILL TABLES THAT ALREADY CREATED IN SQL

# setup 
from __future__ import unicode_literals
import sqlite3
import csv

connection = None
cursor = None
cursor2 = None

#start try-except-finally
try:
    
    #connect to database 
    connection = sqlite3.connect("tweet_sample.sqlite")

    # set row_factory that returns values mapped to column names as well as list
    connection.row_factory = sqlite3.Row

    #make cursors
    cursor = connection.cursor()
    cursor2 = connection.cursor()

    #USERS TABLE 

    #create variables
    sql_create_user = ""
    sql_select_user = ""
    sql_insert_user = ""

    #create user table
    sql_create_user = '''
        CREATE TABLE "User" (
            "user_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "twitter_user_twitter_id" INTEGER,
            "twitter_user_screenname" TEXT(255,0),
            "user_followers_count" INTEGER,
            "user_favorites_count" INTEGER,
            "user_created" TEXT(255,0),
            "user_location" TEXT(255,0),
            "user_description" TEXT(255,0),
            "user_friends_count" INTEGER,
            "user_statuses_count" INTEGER
            )
        '''
    cursor.execute(sql_create_user)

    #SELECT statement
    sql_select_user = '''
        SELECT twitter_user_twitter_id,
            twitter_user_screenname,
            user_followers_count,
            user_favorites_count,
            user_created,
            user_location,
            user_description,
            user_friends_count,
            user_statuses_count 
        FROM tweet_sample_raw
        '''

    #execute the SELECT statement to pull the data
    user_rows = cursor.execute(sql_select_user)

    #loop row by row through the data
    for current_row in user_rows: 

        #INSERT statement
        sql_insert_user = '''
            INSERT INTO User (
                twitter_user_twitter_id,
                twitter_user_screenname,
                user_followers_count,
                user_favorites_count,
                user_created,
                user_location, 
                user_description, 
                user_friends_count, 
                user_statuses_count
                )
            VALUES (?,?,?,?,?,?,?,?,?);
            '''
    	#execute insert function
        cursor.execute(sql_insert_user,(current_row[0], current_row[1], current_row[2], 
        	current_row[3], current_row[4],current_row[5], current_row[6], current_row[7],
        	current_row[8]))
    
        # get ID of each record.
        new_record_id = cursor.lastrowid
    
        # output result
        print( "New record inserted with ID = " + str( new_record_id ) )

    	#commit
    	connection.commit
    
    #END LOOP 

except Exception as e:
    
    print("exception: " + str( e ))
    
finally:

	#check it finished
    print("Done")

    # close cursor
    cursor.close()

    # close connection
    connection.close()

#-- END try-->except-->finally around database access. --#