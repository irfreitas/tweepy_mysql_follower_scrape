from __future__ import unicode_literals

import logging
import time

import pymysql
import tweepy

logging.basicConfig(
    filename="follow.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, retry_delay=60, retry_count=5)

conn = pymysql.connect(host="", user='', password='', db='', charset='', connect_timeout=30)
c = conn.cursor()

c.execute('SET NAMES utf8;')
c.execute('SET character set utf8;')
c.execute('SET character_set_connection=utf8;')

def create_table():
    """
    table_users: stores user objects in table with the relevant rows (see user_entry function below)
    table_ids: stores paired followed and follower ids

    """
    c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft}, {nf1} {ft1})'.format(
        tn="table_ids", nf="from_id", ft="TEXT", nf1="to_id", ft1="TEXT"))
    logging.info("created table %s" % "table_ids")
    print("created table_ids")

    c.execute("""CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft} PRIMARY KEY,
    {nf1} {ft1},
    {nf2} {ft2},
    {nf3} {ft3},
    {nf4} {ft4},
    {nf5} {ft5},
    {nf6} {ft6},
    {nf7} {ft7},
    {nf8} {ft8},
    {nf9} {ft9},
    {nf10} {ft10},
    {nf11} {ft11},
    {nf12} {ft12},
    {nf13} {ft13},
    {nf14} {ft14},
    {nf15} {ft15})""".format(tn='table_users',
                             nf='id_str', ft='VARCHAR(30)',
                             nf1='name', ft1='VARCHAR(191) CHARACTER SET utf8mb4',
                             nf2='location', ft2='VARCHAR(191) CHARACTER SET utf8mb4',
                             nf3='created_at', ft3='VARCHAR(40)',
                             nf4='favourites_count', ft4='VARCHAR(10)',
                             nf5='url', ft5='VARCHAR(255)',
                             nf6='followers_count', ft6='VARCHAR(10)',
                             nf7='verified', ft7='VARCHAR(10)',
                             nf8='time_zone', ft8='VARCHAR(40)',
                             nf9='utc_offset', ft9='VARCHAR(40)',
                             nf10='friends_count', ft10='VARCHAR(10)',
                             nf11='screen_name', ft11='VARCHAR(255)',
                             nf12='default_profile', ft12='VARCHAR(10)',
                             nf13='default_profile_image', ft13='VARCHAR(10)',
                             nf14='listed_count', ft14='VARCHAR(10)',
                             nf15='description', ft15='VARCHAR(255) CHARACTER SET utf8mb4'))
    conn.commit()
    logging.info("created table %s" % "table_users")
    print("created table_users")


create_table()


def follow_entry(followed_id, follower_id):
    """
    make entry of ids for who follows whom
    """
    pair = (str(followed_id), str(follower_id))
    c.execute("INSERT INTO table_ids (from_id, to_id) VALUES ('%s','%s')" % pair)
    # conn.commit()


def user_entry(user_object):
    """
    make tuple of user information to input to database
    """
    user_tuple = (str(user_object.id_str), str(user_object.name), str(user_object.location), str(user_object.created_at), str(user_object.favourites_count), str(user_object.url), str(user_object.followers_count), str(user_object.verified), str(user_object.time_zone), str(user_object.utc_offset), str(user_object.friends_count), str(user_object.screen_name), str(user_object.default_profile), str(user_object.default_profile_image), str(user_object.listed_count), str(user_object.description.encode('utf8')))

    sql = "INSERT IGNORE INTO table_users (id_str, name, location, created_at, favourites_count, url, followers_count, verified, time_zone, utc_offset, friends_count, screen_name, default_profile, default_profile_image, listed_count, description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    c.execute(sql, user_tuple)
    # conn.commit()


def iterate_users(user_id):
    pages = tweepy.Cursor(api.followers, user_id=int(user_id), count=200, skip_status=True, wait_on_rate_limit=True, wait_on_rate_limit_notify = True).pages()
    while True:
        try:
            page = next(pages)
            time.sleep(4)
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
            page = next(pages)
        except StopIteration:
            break
        except tweepy.TweepError:
            time.sleep(30)
            page = next(pages)
        for user in page:
            user_entry(user)
            follow_entry(user_id, user.id_str)
            conn.commit()

Voad_list_accounts = [ Fill, with, twitter, user, ids]

def main(lst):
    """
    For each account in lst, get all followers
    """
    for account in lst:
        iterate_users(account)
        logging.info("logging accomplished for account  %s" % account)
    conn.close()

    
if __name__ == "__main__":
    main(Voad_list_accounts)
