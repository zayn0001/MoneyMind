import re, os
import requests
import backend.bs_scraping as bss
import json
from openai import OpenAI
from dotenv import load_dotenv
import backend.transfer_to_db as ttdb

# get general stock info (separate from portfolio information)
app_base = os.path.dirname(__file__)
app_root = os.path.join(app_base, '../')

load_dotenv(dotenv_path=os.path.join(app_root, '.env.local'))
def setupGeneral():
    stockInfo = bss.main()
    stockDictList = [json.loads(item) for item in stockInfo]
    return stockDictList

def makePrediction(info):
    predictions = []
    tickers = []
    for item in info:
        for ticker,sentences in item.items():
            count = 0
            if ticker not in tickers:
                sentences = "".join(sentences)
                sentences = sentences.replace(".",";")
                job_id = createJob(sentences)
                while jobStatusCheck(job_id) == "IN_PROGRESS":
                    print(count)
                    count+=1
                score = getHighests(job_id)
                sum = summary(ticker, score, sentences)
                predictions.append({"name":ticker, "advice":sum})
                tickers.append(ticker)
                print(f"{ticker} : {score}, {sum}\n")
    return predictions

def summary(ticker, score, sentences):
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
        instructions= f"Using information gathered through various news websites, we have found that there is a {'positive' if score>0 else 'negative'} sentiment towards the {ticker} stock. Use the following summary of information to put together a 1-2 sentence investment advice and use evidence from the information given (you don't need to cite it): "+ sentences
        )
    #print(run)
    if run.status == "completed":
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            run_id=run.id
        )
        text = messages.data[0].content[0].text.value
        #text = extractJson(text)
        text = re.sub(r'【.*?】', '', text) # Remove unwanted stuff from the text

        # Delete the assistant and the thread after use
        client.beta.assistants.delete(assistant_id=my_assistant.id)
        client.beta.threads.delete(thread_id=thread.id)
        return text

def createJob(sentences):
    sentences.replace("."," ")
    response = requests.post(
    "https://api.hume.ai/v0/batch/jobs",
    headers={
        "X-Hume-Api-Key": "d43oGgPUD0mnoAgEmByIEDHQ5ubCx1388sFPFqAlPl4yGoVT",
        "Content-Type": "application/json"
    },
    json={
        "notify": False,
        "text": [
        sentences,
        ],
        "models": {
        "language": {
            "granularity": "sentence",
            "sentiment": {},
            "toxicity": {}
        }
        }
    },
    )
    data = response.json()
    return data["job_id"]

def jobStatusCheck(job_id):
    response = requests.get(
    f"https://api.hume.ai/v0/batch/jobs/{job_id}",
    headers={
        "X-Hume-Api-Key": "d43oGgPUD0mnoAgEmByIEDHQ5ubCx1388sFPFqAlPl4yGoVT"
    },
    )
    data = response.json()
    #print(data)
    return data["state"]["status"]

def getHighests(job_id):
    # Get job predictions (GET /v0/batch/jobs/:id/predictions)
    response = requests.get(
    f"https://api.hume.ai/v0/batch/jobs/{job_id}/predictions",
    headers={
        "X-Hume-Api-Key": "d43oGgPUD0mnoAgEmByIEDHQ5ubCx1388sFPFqAlPl4yGoVT"
    },
    )
    emotions = response.json()[0]['results']['predictions'][0]['models']['language']['grouped_predictions'][0]['predictions'][0]['emotions']

    return overallPosOrNeg(emotions)

def overallPosOrNeg(emotions):
    weight = [1,1,0,0,-2,-1,-1,1.5,-1,0,0,1,-1.5,0,-1.5,1,1,0,1.5,-1.5,-1,-1.5,-1.5,-2,1.5,-1.5,-1,1.5,0,0,2,-1,1,0,0,1.5,1.5,1,0,-1,1,0,0,0,-1,0,1,-1,-1,1,0,0,2]
    score = 0
    for ind in range(len(emotions)):
        score += weight[ind] * emotions[ind]["score"]
    return score


##### CALL THIS FUNCTION TO MAKE GENERAL PREDICTIONS #####
def generalStockPredictions():
    print("----------->reading from the internet...")
    stockSentences = setupGeneral()
    print("\n----------->read news...")
    print(stockSentences)
    print("\n----------->making predictions...")
    predictions = makePrediction(stockSentences)
    print("\n----------->predictions done....")

    ttdb.truncate_and_populate_table(predictions)