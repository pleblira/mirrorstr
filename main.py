from apscheduler.schedulers.background import BackgroundScheduler
import time
import random
import subprocess
import sys
import json
import datetime
from post_note import *
from nostr.key import PrivateKey
   
TWITTER_HANDLE = "jusabitcoiner"
NOSTR_PRIVATE_KEY = ""

# print(type(result.stdout))
# repr shows escape characters - searching for \n
# print(repr(result.stdout))

def scrape_and_post():
    print('running run_snscrape')
    scrape = subprocess.run(['snscrape','--jsonl','-n','5','twitter-user', TWITTER_HANDLE], capture_output=True, text=True)
    json_from_scraper_output = json.loads("["+scrape.stdout.strip().replace("\n",",")+"]")
    # print(json_from_scraper_output)
    with open('tweets.json','r+') as f:
        stored_json = json.load(f)
        for scraped_tweet in json_from_scraper_output:
            print("")
            if scraped_tweet["inReplyToTweetId"] == None:
                new_tweet = True
                while new_tweet == True:
                    for stored_tweet in stored_json:
                        if scraped_tweet["id"] == stored_tweet["id"]:
                            print('tweet already scraped')
                            new_tweet = False
                    if new_tweet == True:
                        print("new tweet found")
                        if scraped_tweet["media"] != None:
                            print("has image")
                            for image in scraped_tweet["media"]:
                                scraped_tweet["rawContent"] = scraped_tweet["rawContent"]+" "+image["fullUrl"]
                        stored_json.append(scraped_tweet)
                        f.seek(0)
                        f.write(json.dumps(stored_json, indent=2))
                        post_note(NOSTR_PRIVATE_KEY, scraped_tweet["rawContent"])
                        new_tweet = False
                print('exited while loop')
            else:
                print('tweet is a reply')

if __name__ == "__main__":
    # NOSTR_PRIVATE_KEY = input("Please type your Nostr private key: ")
    NOSTR_PRIVATE_KEY = PrivateKey.from_nsec("nsec16pejvh2hdkf4rzrpejk93tmvuhaf8pv7eqenevk576492zqy6pfqguu985")

    with open('tweets.json','w') as f:
        f.write("[]")

    scrape = subprocess.run(['snscrape','--jsonl','-n','5','twitter-user',TWITTER_HANDLE], capture_output=True, text=True)
    json_from_output = json.loads("["+scrape.stdout.strip().replace("\n",",")+"]")
    json_from_output.reverse()
    with open('tweets.json','r+') as f:
        f.seek(0)
        f.write(json.dumps(json_from_output, indent=2))
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_and_post, 'interval', seconds=6)
    print('\nstarting scheduler')
    scheduler.start()

while True:
#     with open('tweets.json', 'r') as f:
#         tweets = json.load(f)
#         last_queried_event_datetime = int(datetime.fromisoformat(tweets[len(tweets)-1]['date']).timestamp())
#     # print(f"last queried event datetime {last_queried_event_datetime}")
#     # quit()
#     time.sleep(600)
#     print('closing connections to relays')
#     close_connections(relay_manager)
#     time.sleep(5)
#     print('restarting connection on relay manager')
#     relay_manager = main(public_key.hex(), since=last_queried_event_datetime)
#     print('resuming')

    print('\nhello world')
    time.sleep(7)