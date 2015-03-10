from __future__ import unicode_literals

# import six package
import six

# import twitter
import twitter

# variables to hold tweet info
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

# variables for processing tweets
my_oauth = None
twitter_stream = None
tweet_iterator = None
tweet_counter = -1
current_tweet = None

# hashtag processing
tweet_hashtag_json_list = None
hashtag_count = -1
tweet_hashtag_json = None
current_hashtag_text = ""
tweet_hashtag_list = []

# url processing
tweet_url_json_list = None
url_count = -1
tweet_url_json = None
current_url_text = ""
current_dislpay_url_text = ""
current_short_url_text = ""
tweet_url_list = []
tweet_display_url_list = []
tweet_short_url_list = []

# user mention processing
tweet_user_mentions_json_list = None
user_mention_count = -1
tweet_user_mention_json = None
current_user_id = ""
current_user_screenname = ""
tweet_user_id_list = []
tweet_user_screenname_list = []

# set up OAuth stuff.
CONSUMER_KEY = '7nBeY5FeuBVcHycx7BltvUadt'
CONSUMER_SECRET = 'vAD1UOIWd24oq52R8suGCCggy1kU6pBd1JPwYve5BT5qz0FDyl'
ACCESS_KEY = '349050542-h2OJB8XEg2NicZEpIYcX5Yj1RdXGYNqtr6XPbLwo'
ACCESS_SECRET = '7MOMc8VtwnlbM0ENGsucHcaP1BxGxBYj972AQtWZQKVv0'

# Make an OAuth object.
my_oauth = twitter.OAuth( ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET )

try: 

    #connect to database 
    connection = sqlite3.connect( "tweet_sample.sqlite" )

    # set row_factory that returns values mapped to column names as well as list
    connection.row_factory = sqlite3.Row

    #make cursors
    cursor = connection.cursor()
    cursor2 = connection.cursor()

    # Create a tweetstream
    twitter_stream = twitter.TwitterStream( auth = my_oauth )

    # get an iterator over tweets - basic sample
    tweet_iterator = twitter_stream.statuses.sample() 

    # or, filtered sample
    # from https://dev.twitter.com/streaming/reference/post/statuses/filter
    # "track" = list of string keywords
    # "locations" = list of string lat. long. locations ( "<lat>,<long>" )
    # "follow" = list of users whose statuses we want returned.
    #tweet_iterator = twitter_stream.statuses.filter( track = [ "nytimes", ] )

    # loop over tweets
    tweet_counter = 0
    for current_tweet in tweet_iterator:

        tweet_counter += 1
    
        # check for delete request.
        try:
    
            # if delete request, will have a delete element at the root.
            # If not, this will throw an exception, and you'll process the tweet.
            delete_info = current_tweet[ 'delete' ]
            print( "--> Deletion request - moving on." )
    
        except:

            # print out the tweet.
            print( "====> Tweet JSON:" )
            print( current_tweet_JSON_string )

            #------------------------------------------------------------------------
            # tweet data
            #------------------------------------------------------------------------

            # get tweet data
            twitter_tweet_id = current_tweet[ 'id' ]
            tweet_text = current_tweet[ 'text' ]
            tweet_timestamp = current_tweet[ 'created_at' ]
            tweet_language = current_tweet[ 'lang' ]
            tweet_place = current_tweet[ 'place' ]
            tweet_retweet_count = current_tweet[ 'retweet_count' ]
        
            # !tweet hashtags?
            tweet_hashtag_json_list = current_tweet[ 'entities' ][ 'hashtags' ]
            hashtag_count = len( tweet_hashtag_json_list )
            if hashtag_count > 0:
        
                # got at least one hashtag. loop and build list.
                tweet_hashtag_list = []
                for tweet_hashtag_json in tweet_hashtag_json_list:
            
                    # get hash tag value
                    current_hashtag_text = tweet_hashtag_json[ 'text' ]
                
                    # append to list
                    tweet_hashtag_list.append( current_hashtag_text )
            
                #-- END loop over hash tags --#
        
                # store count
                tweet_hashtag_mention_count = len( tweet_hashtag_list )

                # convert to comma-delimited list for storage.
                tweet_hashtags_mentioned = ",".join( tweet_hashtag_list )

            #-- END check to see if one or more hash tags --#
        
            # !tweet urls?
            tweet_url_json_list = current_tweet[ 'entities' ][ 'urls' ]
            url_count = len( tweet_url_json_list )
            if url_count > 0:
        
                # got at least one url. loop and build lists.
                tweet_url_list = []
                tweet_display_url_list = []
                tweet_short_url_list = []

                for tweet_url_json in tweet_url_json_list:
            
                    # get URL, display URL, and short URL
                    current_url_text = tweet_url_json[ 'expanded_url' ]
                    current_display_url_text = tweet_url_json[ 'display_url' ]
                    current_short_url_text = tweet_url_json[ 'url' ]

                    # append to lists
                    encoded_value = current_url_text.encode( 'utf-8' )
                    tweet_url_list.append( six.moves.urllib.parse.quote_plus( encoded_value ) )
                    encoded_value = current_display_url_text.encode( 'utf-8' )
                    tweet_display_url_list.append( six.moves.urllib.parse.quote_plus( encoded_value ) )
                    encoded_value = current_short_url_text.encode( 'utf-8' )
                    tweet_short_url_list.append( six.moves.urllib.parse.quote_plus( encoded_value ) )
            
                #-- END loop over URLs --#
        
                # store count
                tweet_url_count = len( tweet_url_list )

                # convert to comma-delimited lists for storage.
                tweet_shortened_urls_mentioned = ",".join( tweet_short_url_list )
                tweet_display_urls_mentioned = ",".join( tweet_display_url_list )
                tweet_full_urls_mentioned = ",".join( tweet_url_list )

            #-- END check to see if one or more urls --#
        
            # !tweet user mentions?
            tweet_user_mentions_json_list = current_tweet[ 'entities' ][ 'user_mentions' ]
            user_mention_count = len( tweet_user_mentions_json_list )
            if user_mention_count > 0:
        
                # got at least one user mention. loop and build lists.
                tweet_user_id_list = []
                tweet_user_screenname_list = []
                for tweet_user_mention_json in tweet_user_mentions_json_list:
            
                    # get user mention values
                    current_user_id = tweet_user_mention_json[ 'id_str' ]
                    current_user_screenname = tweet_user_mention_json[ 'screen_name' ]
                
                    # append to lists
                    tweet_user_id_list.append( current_user_id )
                    tweet_user_screenname_list.append( current_user_screenname )
            
                #-- END loop over hash tags --#
        
                # store count
                tweet_user_mention_count = len( tweet_user_id_list )

                # convert to comma-delimited lists for storage.
                tweet_users_mentioned_ids = ",".join( tweet_user_id_list )
                tweet_users_mentioned_screennames = ",".join( tweet_user_screenname_list )

            #-- END check to see if one or more user mentions --#
        
            #------------------------------------------------------------------------
            # user data
            #------------------------------------------------------------------------

            twitter_user_twitter_id = current_tweet[ 'user' ][ 'id' ]
            twitter_user_screenname = current_tweet[ 'user' ][ 'screen_name' ]
            user_followers_count = current_tweet[ 'user' ][ 'followers_count' ]
            user_favorites_count = current_tweet[ 'user' ][ 'favourites_count' ]
            user_friends_count = current_tweet[ 'user' ][ 'friends_count' ]
            user_created = current_tweet[ 'user' ][ 'created_at' ]
            user_location = current_tweet[ 'user' ][ 'location' ]
            user_description = current_tweet[ 'user' ][ 'description' ]
            user_statuses_count = current_tweet[ 'user' ][ 'statuses_count' ]

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

            #print something

            print ("new record inserted", twitter_tweet_id)
        
        #-- END try-except to see if deleted tweet. --#
    
        if ( tweet_counter % 100 ) == 0:
    
            # yes - print a brief message
            print( "====> tweet count = " + str( tweet_counter ) )
    
    #-- END check to see if we've done another hundred --#
    #-- END loop over tweet stream --#

except Exception as e:
    
    print( "exception: " + str( e ) )
    
finally:

    # close cursor
    cursor.close()
    cursor2.close()

    # close connection
    connection.close()

#-- END try-->except-->finally around database access. --#
