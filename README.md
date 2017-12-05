# tweepy_mysql_follower_scrape
Uses tweepy to scrape the followers of a list of twitter users and insert them into a mysql database.  To use the script, you will need to add in your Twitter API credentials into the sript.  It also requires adding in necessary information for the mysql database which you intend to connect with.

The script uses pymysql to connect to your mysql server, create the table_ids and table_users, and insert information. Tweepy is used to gather the numeric ids of Twitter users that follow accounts which are in the list "list_accounts".  The script has been used to scrape information from Twitter users with very few followers up to those with several million followers.  The speed of the script is limited by the rate limiting which Twitter places on their API. 
