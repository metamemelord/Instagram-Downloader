import json
import requests
import re
import sys
import os
from datetime import datetime

if len(sys.argv) < 2:
    print("Please provide a username")
    quit(0)

username = sys.argv[1]

url = 'https://www.instagram.com/{}/'.format(username)
url_retrival = 'https://i.instagram.com/api/v1/users/{}/info'

try:
    r = requests.get(url, timeout=10.0)
    if r.status_code == 200:
        instagram_html = str(r.content)
        id = re.search("\"id\":\"[0-9]*\"", instagram_html).group(0).split(":")[1].strip("\"")
        if not len(id):
            raise Exception("Something went wrong")
        user_info = url_retrival.format(id)
        r = requests.get(user_info)
        response_json = json.loads(r.content)
        if response_json['user']['hd_profile_pic_url_info']['url']:
            print(response_json['user']['hd_profile_pic_url_info']['url'])
            r = requests.get(response_json['user']['hd_profile_pic_url_info']['url'])
            if os.path.isdir("./Instagram Downloads"):
                pass
            else:
                os.mkdir('./Instagram Downloads')
            with open("./Instagram Downloads/%s-%s.jpg"%(username, str(datetime.now()).replace(":", "-")), 'wb') as f:
                f.write(r.content)
            print("Saved to Instagram Downloads")
        else:
            print(response_json['user'])
    else:
        print("User '%s' not found!"%username)
except Exception as e:
        print(e)
