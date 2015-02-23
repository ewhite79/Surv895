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
    connection = sqlite3.connect( "tweet_sample.sqlite" )

    # set row_factory that returns values mapped to column names as well as list
    connection.row_factory = sqlite3.Row

    #make cursors
    cursor = connection.cursor()
    cursor2 = connection.cursor()

#############################FILL USER TABLE############################

    #declare variables
#    user_set = None
#    current_row = None
#    sql_insert_user = ""

#    user_set = cursor.execute(
#    	'''
#    	SELECT 
#            twitter_user_twitter_id,
#            twitter_user_screenname,
#            user_followers_count,
#            user_favorites_count,
#            user_location,
#            user_description,
#            user_friends_count,
#            user_statuses_count
#        FROM tweet_sample_raw
#        ''')
    
#    unique_users = []

    #loop through rows
#   for current_row in user_set:

#        if current_row[0] not in unique_users:

#           unique_users.append(current_row)

#           sql_insert_user = '''
#                INSERT INTO User (
#                    twitter_user_twitter_id,
#                    twitter_user_screenname,
#                    user_followers_count,
#                    user_favorites_count,
#                    user_created,
#                   user_location,
#                    user_description,
#                    user_friends_count,
#                    user_statuses_count
#             	    )
#                VALUES (?,?,?,?,?,?,?,?,?);
#                '''
        	#execute insert function

#            cursor2.execute(sql_insert_user,(current_row[0], current_row[1], current_row[2], 
#        	current_row[3], current_row[4],current_row[5], current_row[6], current_row[7],
#        	current_row[8]))
    	
#            # get ID of each record.
#            new_user_id = cursor2.lastrowid
    
            # output result
#            print("New record inserted with ID = " + str(new_user_id))

            #commit
#            connection.commit()

#        else:

#            pass 

        
    #end loop



    ############################FILL TWEET TABLE##########################

    #declare variables
#    tweet_set = None
#    current_row = None
#    sql_insert_tweet = ""

    #SELECT statement
#    tweet_set = cursor.execute(
#    	'''
#        SELECT 
#    	    tweet_timestamp,
#            twitter_tweet_id,
#            tweet_text,
#            tweet_language,
#            tweet_retweet_count,
#            tweet_place,
#            tweet_user_mention_count,
#            tweet_hashtag_mention_count,
#            tweet_url_count
#        FROM tweet_sample_raw
#        ''') 
#    #loop through columns
#    for current_row in tweet_set:
#    
        #INSERT statement
#        sql_insert_tweet = '''
#            INSERT INTO Tweet (tweet_timestamp,
#                twitter_tweet_id,
#                tweet_text,
#                tweet_language,
#                tweet_retweet_count,
#                tweet_place,
#                tweet_user_mention_count,
#                tweet_hashtag_mention_count,
#                tweet_url_count
#            	)
#            VALUES (?,?,?,?,?,?,?,?,?);
#            '''
#    	#execute insert function
#        cursor2.execute(sql_insert_tweet,(current_row[0], current_row[1], current_row[2], 
#        	current_row[3], current_row[4],current_row[5], current_row[6], current_row[7],
#        	current_row[8]))
    	
        # get ID of each record.
#        new_tweet_id = cursor2.lastrowid
    
        # output result
 #       print("New record inserted with ID = " + str(new_tweet_id))

#
#       print current_row[0]
#
#    	#commit
#    	connection.commit()    

   #END LOOP 

#######################################FILL IN HASHTAG TABLE###########################

    #declare variables
#    hashtag_set = None
#    current_row = None
#    sql_insert_hashtag = ""
#    hashtag_list = []
#    unique_hashtags = []

    #SELECT statement
#    hashtag_set = cursor.execute(
#        '''
#        SELECT tweet_hashtags_mentioned
#        FROM tweet_sample_raw
#        WHERE tweet_hashtags_mentioned !='';
#        ''') 
    
    #INSERT function
#    sql_insert_hashtag = '''
#        INSERT INTO Hashtag 
#        (hashtag_text)            	
#        VALUES (?);
#    '''

    #loop over rows of hashags
#    for current_row in hashtag_set:

        #split list
#        hashtag_list = current_row[0].split(",")

        #loop through split hashtags
#        for hashtag in hashtag_list:

            #check if we already have this hashtag
#            if hashtag not in unique_hashtags:

                #add to list
#                unique_hashtags.append(hashtag)

                #execute insert function
#                cursor2.execute(sql_insert_hashtag,(hashtag,))
    	
                #check whether it worked
#    	        new_hashtag_id = cursor2.lastrowid
    
                # output result
#                print("New record inserted with ID = " + str(new_hashtag_id))

                #commit
#                connection.commit()

            #if already in list do nothing
#            else:

#                pass
            #end check            
        #end loop

    #end loop   

    #test

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