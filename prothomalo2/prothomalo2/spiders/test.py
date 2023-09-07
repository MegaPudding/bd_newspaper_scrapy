import requests
import json
req = requests.get("https://www.banglatribune.com/api/theme_engine/get_ajax_contents?widget=10950&start=20&count=20&page_id=0&author=0&tags=&archive_time=")
response = req.json()
print(response)