from mastodon import Mastodon
import dropbox
from datetime import date
import schedule
import time
import json
import os

with open('config.json') as config_file:
    data = json.load(config_file)
    accessToken = data['access_token']
    apiBaseUrl = data['api_base_url']
    dropbox_access_token = data['dropbox_access_token']

def GetFollowersList():
    print("Getting Followers List")
    dateTime = str(date.today())
    dateTime = dateTime.replace('-', "_")
    fileName = "following_" + dateTime + ".txt"

    mastodon = Mastodon(
        access_token = accessToken,
        api_base_url = apiBaseUrl,
        ratelimit_method='pace',
    )
    id = mastodon.account_verify_credentials()["id"]
    start = mastodon.account_following(id)

    following = mastodon.fetch_remaining(start)

    f = open(fileName, "w")

    for d in following:
            line = d['acct'] + "\n"
            #print(line)
            f.write(line)
            
    f.close()

    dropbox_path = "/" + fileName
    computer_path = "/home/pi/mastodon/" + fileName

    #with dropbox.Dropbox(dropbox_access_token) as dbx:
    client = dropbox.Dropbox(dropbox_access_token)
    print("[SUCCESS] dropbox account linked")
    client.files_upload(open(computer_path, "rb").read(), dropbox_path)
    print("[UPLOADED] {}".format(computer_path))
    
    if os.path.isfile(fileName):
        os.remove(fileName)


schedule.every().day.at("20:20").do(GetFollowersList)

while True:
    schedule.run_pending()
    time.sleep(60) 


    
