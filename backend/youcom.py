import os, re
from os import getenv, path
from dotenv import load_dotenv
import backend.bs_scraping as bss
import backend.sentimentAnalysis as sent
from openai import OpenAI
import requests
import ast
app_base = path.dirname(__file__)
app_root = path.join(app_base, '../')

load_dotenv(dotenv_path=path.join(app_root, '.env.local'))

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
        news = [x["url"] for x in response["news"]["results"][:2]]
        data[company] = news
    return data

def summarizePort(ticker, text):
    """uses openAI to get dictionary of stocks to related sentences"""
    load_dotenv()

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    my_assistant = client.beta.assistants.create(
        instructions="You are a news article parser.",
        name="testing",
        model="gpt-4o",
    )
    thread = client.beta.threads.create()
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=my_assistant.id,
        model="gpt-4o",
        instructions="Give me a lists of sentences from the article which are related to {ticker} stock (don't modify the sentences). Make sure that only the sentences relating to the stock are included in the values. Keep the output in JSON format, so use only double quotes not single quotes. When doing double quotes, make sure to use \" whenever necessary: "+ text
        )
    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            run_id=run.id
        )
        text = messages.data[0].content[0].text.value
        text = re.sub(r'【.*?】', '', text) # Remove unwanted stuff from the text

        # Delete the assistant and the thread after use
        client.beta.assistants.delete(assistant_id=my_assistant.id)
        client.beta.threads.delete(thread_id=thread.id)
        return text
    

#input --> {ticker: [list of urls]}
###### RUN THIS FUNCTION TO MAKE PORTFOLIO PREDICTIONS ######
def portfolioStockPredictions(portfolio):
    allStocks = []
    for ticker, urls in portfolio.items():
        # for each ticker, create a large paragraph 
        info = []
        for url in urls:
            try:
                text = bss.extract_text_with_line_breaks_from_url(url)
                text = summarizePort(ticker, text)
                text = text[text.find("["):text.rfind("]")+1]
                
                info += ast.literal_eval(text)
            except:
                print("one failed")
        allStocks.append({ticker:info})

    predictions = sent.makePrediction(allStocks)
    return predictions
    

"""
temp = {"AAPL":["https://finance.yahoo.com/news/best-stock-buy-now-apple-101500161.html", "https://finance.yahoo.com/news/hedge-funds-crazy-apple-inc-212411753.html"],
        "DUOL":["https://finance.yahoo.com/news/too-buy-duolingo-stock-142100630.html"]}
portfolioStockPredictions(temp)
"""

