# FILL TABLES THAT ALREADY CREATED IN SQL

# setup 
from __future__ import unicode_literals
import sqlite3
import csv

connection = None
cursor = None
cursor2 = None
tab_delimited_file = None
tweet_reader = None
tweet_counter = -1
field_count = -1
current_tweet_row = None

# variables to hold fields
tweet_timestamp = ""
twitter_tweet_id = ""
tweet_text = ""
tweet_language = ""
twitter_user_twitter_id = ""
twitter_user_screenname = ""
user_followers_count = ""
user_favorites_count = ""
user_created = ""
user_location = ""
tweet_retweet_count = ""
tweet_place = ""
tweet_user_mention_count = ""
tweet_users_mentioned_screennames = ""
tweet_users_mentioned_ids = ""
tweet_hashtag_mention_count = ""
tweet_hashtags_mentioned = ""
tweet_url_count = ""
tweet_shortened_urls_mentioned = ""
tweet_full_urls_mentioned = ""
user_description = ""
user_friends_count = ""
user_statuses_count = ""
tweet_display_urls_mentioned = ""

# build INSERT statement
sql_insert_string = ""

#start try-except-finally
try:
    
    #connect to database 
    connection = sqlite3.connect( "tweet_sample.sqlite" )

    # set row_factory that returns values mapped to column names as well as list
    connection.row_factory = sqlite3.Row

    #make cursors
    cursor = connection.cursor()
    cursor2 = connection.cursor()

##############################READ IN BIG FILE############################################

    # open the data file for reading.
    with open( 'tweet_sample.txt', 'rb' ) as tab_delimited_file:

        # feed the file to csv.reader to parse.
        tweet_reader = csv.reader( tab_delimited_file, dialect = "excel-tab" )
            delimiter = '\t', quotechar = '\"', strict = True, lineterminator = "\n" )

        # loop over logical rows in the file.
        tweet_counter = 0
        for current_tweet_row in tweet_reader:

            tweet_counter = tweet_counter + 1
            field_count = len( current_tweet_row )

            # print some info
            print( "====> line " + str( tweet_counter ) + " - " + str( field_count ) + " fields - text: " + '|||'.join( current_tweet_row ) )

            # only do stuff after first row
            if ( tweet_counter > 1 ):

                # get fields
                tweet_timestamp = unicode( current_tweet_row[ 0 ], "UTF-8" )
                twitter_tweet_id = unicode( current_tweet_row[ 1 ], "UTF-8" )
                tweet_text = unicode( current_tweet_row[ 2 ], "UTF-8" )
                tweet_language = unicode( current_tweet_row[ 3 ], "UTF-8" )
                twitter_user_twitter_id = int( current_tweet_row[ 4 ] )
                twitter_user_screenname = unicode( current_tweet_row[ 5 ], "UTF-8" )
                user_followers_count = int( current_tweet_row[ 6 ] )
                user_favorites_count = int ( current_tweet_row[ 7 ] )
                user_created = unicode( current_tweet_row[ 8 ], "UTF-8" )
                user_location = unicode( current_tweet_row[ 9 ], "UTF-8" )
                tweet_retweet_count = int( current_tweet_row[ 10 ] )
                tweet_place = unicode( current_tweet_row[ 11 ], "UTF-8" )
                tweet_user_mention_count = unicode( current_tweet_row[ 12 ], "UTF-8" )
                tweet_users_mentioned_screennames = unicode( current_tweet_row[ 13 ], "UTF-8" )
                tweet_users_mentioned_ids = unicode( current_tweet_row[ 14 ], "UTF-8" )
                tweet_hashtag_mention_count = unicode( current_tweet_row[ 15 ], "UTF-8" )
                tweet_hashtags_mentioned = unicode( current_tweet_row[ 16 ], "UTF-8" )
                tweet_url_count = unicode( current_tweet_row[ 17 ], "UTF-8" )
                tweet_shortened_urls_mentioned = unicode( current_tweet_row[ 18 ], "UTF-8" )
                tweet_full_urls_mentioned = unicode( current_tweet_row[ 19 ], "UTF-8" )
                user_description = unicode( current_tweet_row[ 20 ], "UTF-8" )
                user_friends_count = int( current_tweet_row[ 21 ] )
                user_statuses_count = int( current_tweet_row[ 22 ] )
                tweet_display_urls_mentioned = unicode( current_tweet_row[ 23 ], "UTF-8" )

                # print tweet ID
                print ( "====> line " + str( tweet_counter ) + " - " + str( field_count ) +# " Twitter Tweet ID = " + twitter_tweet_id )

                # build INSERT statement
                sql_insert_string = '''
                    INSERT INTO tweet_sample_raw
                    (
                        tweet_timestamp,
                        twitter_tweet_id,
                        tweet_text,
                        tweet_language,
                        twitter_user_twitter_id,
                        twitter_user_screenname,
                        user_followers_count,
                        user_favorites_count,
                        user_created,
                        user_location,
                        tweet_retweet_count,
                        tweet_place,
                        tweet_user_mention_count,
                        tweet_users_mentioned_screennames,
                        tweet_users_mentioned_ids,
                        tweet_hashtag_mention_count,
                        tweet_hashtags_mentioned,
                        tweet_url_count,
                        tweet_shortened_urls_mentioned,
                        tweet_full_urls_mentioned,
                        user_description,
                        user_friends_count,
                        user_statuses_count,
                        tweet_display_urls_mentioned
                    )
                    VALUES
                    (
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?
                    )
                '''

                # execute the command.
                cursor.execute( sql_insert_string, ( tweet_timestamp, twitter_tweet_id, tweet_text, tweet_language, twitter_user_twitter_id, twitter_user_screenname, user_followers_count, user_favorites_count, user_created, user_location, tweet_retweet_count, tweet_place, tweet_user_mention_count, tweet_users_mentioned_screennames, tweet_users_mentioned_ids, tweet_hashtag_mention_count, tweet_hashtags_mentioned, tweet_url_count, tweet_shortened_urls_mentioned, tweet_full_urls_mentioned, user_description, user_friends_count, user_statuses_count, tweet_display_urls_mentioned ) )

               # commit.
                connection.commit()

            #-- END check to make sure we aren't the first row. --#

        #-- END loop over rows in file --#

    #-- END use of tab_delimited_file --#
    
#############################FILL USER TABLE############################

    #declare variables
    user_set = None
    current_row = None
    sql_insert_user = ""
    user_set = cursor.execute(
    	'''
    	SELECT 
            twitter_user_twitter_id,
            twitter_user_screenname,
            user_followers_count,
            user_favorites_count,
            user_created,
            user_location,
            user_description,
            user_friends_count,
            user_statuses_count
        FROM tweet_sample_raw
        ''')
    
    unique_users = []

    #loop through rows
    for current_row in user_set:

        if current_row[0] not in unique_users:

            unique_users.append(current_row[0])

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

            cursor2.execute(sql_insert_user,(current_row[0], current_row[1], current_row[2], 
        	    current_row[3], current_row[4],current_row[5], current_row[6], current_row[7],
        	    current_row[8]))
    	
            # get ID of each record.
            new_user_id = cursor2.lastrowid
    
            # output result
            print("New record inserted with ID = " + str(new_user_id))

            #commit
            connection.commit()

        else:

            pass 
        
    #end loop


    ############################FILL TWEET TABLE##########################

    #declare variables
    tweet_set = None
    current_row = None
    sql_insert_tweet = ""

    #SELECT statement
    tweet_set = cursor.execute(
    	'''
        SELECT 
    	    twitter_user_twitter_id,
    	    tweet_timestamp,
            twitter_tweet_id,
            tweet_text,
            tweet_language,
            tweet_retweet_count,
            tweet_place,
            tweet_user_mention_count,
            tweet_hashtag_mention_count,
            tweet_url_count
        FROM tweet_sample_raw
        ''') 

    #loop through columns
    for current_row in tweet_set:
    
        #INSERT statement
        sql_insert_tweet = '''
            INSERT INTO Tweet (twitter_user_twitter_id,
                tweet_timestamp,
                twitter_tweet_id,
                tweet_text,
                tweet_language,
                tweet_retweet_count,
                tweet_place,
                tweet_user_mention_count,
                tweet_hashtag_mention_count,
                tweet_url_count
            	)
            VALUES (?,?,?,?,?,?,?,?,?,?);
            '''
	   	#execute insert function
        cursor2.execute(sql_insert_tweet,(current_row[0], current_row[1], current_row[2],
            current_row[3], current_row[4], current_row[5], current_row[6], current_row[7],
            current_row[8], current_row[9]))
    	
       # get ID of each record.
        new_tweet_id = cursor2.lastrowid
   
        # output result
        print("New record inserted with ID = " + str(new_tweet_id))

        print current_row[0]

    	#commit
        connection.commit()    

   #END LOOP 

#######################################FILL IN HASHTAG TABLE###########################

    #declare variables
    hashtag_set = None
    current_row = None
    sql_insert_hashtag = ""
    hashtag_list = []
    unique_hashtags = []

    #SELECT statement
    hashtag_set = cursor.execute(
        '''
        SELECT tweet_hashtags_mentioned
        FROM tweet_sample_raw
        WHERE tweet_hashtags_mentioned !='';
        ''') 
    
    #INSERT function
    sql_insert_hashtag = '''
        INSERT INTO Hashtag 
        (hashtag_text)            	
        VALUES (?);
    '''

    #loop over rows of hashags
    for current_row in hashtag_set:

        #split list
        hashtag_list = current_row[0].split(",")

        #loop through split hashtags
        for hashtag in hashtag_list:

            #check if we already have this hashtag
            if hashtag not in unique_hashtags:

                #add to list
                unique_hashtags.append(hashtag)

                #execute insert function
                cursor2.execute(sql_insert_hashtag,(hashtag,))
    	
                #check whether it worked
    	        new_hashtag_id = cursor2.lastrowid
    
                # output result
                print("New record inserted with ID = " + str(new_hashtag_id))

                #commit
                connection.commit()

            #if already in list tell me it's there
            else:

                print("got this one already")

            #end check            
        #end loop

    #end loop   

#######################################FILL IN URL TABLE###########################

    #declare variables
    full_url_set = None
    current_row = None
    sql_insert_full_url = ""
    full_url_list = []
    unique_full_urls = []
 
    #SELECT statement
    full_url_set = cursor.execute(
        '''
        SELECT tweet_full_urls_mentioned
        FROM tweet_sample_raw
        WHERE tweet_full_urls_mentioned !='';
        ''') 
    
    #INSERT function
    sql_insert_full_url = '''
       INSERT INTO URL 
       (full_url)            	
        VALUES (?);
    '''

    #loop over rows of urls
    for current_row in full_url_set:

        #split list
        full_url_list = current_row[0].split(",")

        #loop through split urls
        for url in full_url_list:

            #check if we already have this url
            if url not in unique_full_urls:

                #add to list
                unique_full_urls.append(url)

                #execute insert function
                cursor2.execute(sql_insert_full_url,(url,))
    	
                #check whether it worked
    	        new_url_id = cursor2.lastrowid
    
                # output result
                print("New record inserted with ID = " + str(new_url_id))

                #commit
                connection.commit()

            #if already in list print message
            else:

                print ("got this one already")

            #end check            
        #end loop

    #end loop   

except Exception as e:
    
    print( "exception: " + str( e ) )
    
finally:

	#check it finished
    print( "Done" )

    # close cursor
    cursor.close()
    cursor2.close()

    # close connection
    connection.close()

#-- END try-->except-->finally around database access. --#