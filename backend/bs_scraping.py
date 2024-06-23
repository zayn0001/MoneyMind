import requests
from bs4 import BeautifulSoup
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
app_base = os.path.dirname(__file__)
app_root = os.path.join(app_base, '../')

load_dotenv(dotenv_path=os.path.join(app_root, '.env.local'))

def scrape_yahoo_finance_news():
    """goes through yahoo's finance website and takes articles that are flagged to be related to stocks/trading"""
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select('h3 a')  # Selects all <a> tags within <h3> tags

        news = []
        for article in articles:
            title = article.get_text(strip=True)
            link = article['href']
            if not link.startswith('http'):
                link = f"https://finance.yahoo.com{link}"
            news.append({'title': title, 'link': link})

        return news
    else:
        print(f"Failed to fetch the page at {url}, Status Code: {response.status_code}")
        return []

def filter_news(news):
    """filters to figure out which articles are related to stocks"""
    stock_keywords = ['stock', 'share', 'market', 'NASDAQ', 'NYSE', 'S&P', 'Dow', 'equity', 'ticker', 'IPO', 'dividend', 'invest']
    filtered = []

    for article in news:
        title = article["title"].lower()
        if any(keyword.lower() in title for keyword in stock_keywords) and ".html" in article["link"]:
            filtered.append(article)
    return filtered

def fix_url(url):
    """Ensure the urls are in proper format"""
    url = url.strip("/")
    if not url.startswith("https://"):
        url = "https://" + url
    return url

def extract_text_with_line_breaks_from_url(url):
    """Retrieve all the text contents of the html of a page as a string"""

    # Ensure it is in the proper format
    url = fix_url(url)

    # Fetch the HTML content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text with proper line breaks and remove duplicates
    text_with_line_breaks = ' '.join(list(set(soup.stripped_strings)))
    
    return text_with_line_breaks

def summarize(text):
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
        instructions="Give me a python dictionary where the keys are stock tickers and the values are lists of sentences from the article which are related to that stock (don't modify the sentences). Make sure that only the sentences relating to the stock are included in the values. Keep the output in JSON format, so use only double quotes not single quotes. When doing double quotes, make sure to use \" whenever necessary: "+ text
        )
    #print(run)
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

def main():
    """main function which combies all helper functions to get all the information from yahoo finance"""
    news = scrape_yahoo_finance_news()
    stock_news = filter_news(news)
    allInfo = []
    for idx, article in enumerate(stock_news):
        try:
            text = extract_text_with_line_breaks_from_url(article['link'])
            text = summarize(text)
            text = text[text.find("{"):text.rfind("}")+1]
            #print(text)
            allInfo.append(text)
        except:
            pass
    return allInfo




if __name__ == "__main__":
    news = scrape_yahoo_finance_news()
    stock_news = filter_news(news)
    print("------------------------------------------------")
    print("Stock-related news articles:")
    for idx, article in enumerate(stock_news):
        print(f"{idx+1}. {article['title']}\n   {article['link']}")
        try:
            text = extract_text_with_line_breaks_from_url(article['link'])
            text = summarize(text)
            text = text[text.find("{"):text.rfind("}")+1]
            print(text)
        except:
            pass


