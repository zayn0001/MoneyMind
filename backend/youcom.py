import json
import boto3
from os import getenv, path
from dotenv import load_dotenv
app_base = path.dirname(__file__)
app_root = path.join(app_base, '../')

load_dotenv(dotenv_path=path.join(app_root, '.env.local'))

import requests

def get_news_links(company_names):
    headers = {"X-API-Key": getenv("YOUCOM_API_KEY")}
    data = {}
    for company in company_names:
        params = {"query": company}
        
        response = requests.get(
            f"https://api.ydc-index.io/news?q={company}",
            params=params,
            headers=headers,
        ).json()
        news = [x["url"] for x in response["news"]["results"]]
        data[company] = news
    return data
results = get_news_links(["microsoft", "apple", "google"])
print(json.dumps(results))

