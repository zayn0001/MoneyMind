import json
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from os import getenv, path
from dotenv import load_dotenv

app_base = path.dirname(__file__)
app_root = path.join(app_base, '../')

load_dotenv(dotenv_path=path.join(app_root, '.env.local'))

cred = credentials.Certificate(json.loads(getenv("FIREBASE_SERVICE_ACCOUNT")))
firebase_admin.initialize_app(cred)

app = FastAPI()

# Define your domain
allowed_domains = ["localhost:3000", "127.0.0.1:8000", "next-starter-swart.vercel.app"]  # Replace with your actual domain
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_domains,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")







@app.get("/backend/python")
def hello_world(request: Request, current_user: dict = Depends(get_current_user)):
    mystr = f"Hello, {current_user['name']}. This is a random sentence"
    return {"message":mystr}


@app.get("/backend/getprediction")
def hello(request):
    news_article_links = get_news(request["links"])
    listofarticledata = getlist(news_article_links)
    articledict = {}
    for article in listofarticledata:
        articledict[article.title] = getprediction(article.content)
    return articledict

