import json
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import boto3
from os import getenv, path
from dotenv import load_dotenv
from pydantic import BaseModel
import backend.youcom as yc
app_base = path.dirname(__file__)
app_root = path.join(app_base, '../')

load_dotenv(dotenv_path=path.join(app_root, '.env.local'))

cred = credentials.Certificate(json.loads(getenv("FIREBASE_SERVICE_ACCOUNT")))
firebase_admin.initialize_app(cred)
session = boto3.Session(
    aws_access_key_id=getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=getenv("AWS_SECRET"),
    region_name='us-west-1'  # e.g., 'us-east-1'
)

# Create a DynamoDB client
dynamodb = session.client('dynamodb')
# Example: Inserting an item into DynamoDB table
table_name = 'money-mind'

def update_user(username, company_names):
    table_name = 'money-mind'
    
    # Check if the user exists in DynamoDB
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'username': {'S': username}
        }
    )
    
    if 'Item' in response:
        # User exists, update company names
        existing_companies = response['Item'].get('companies', {'SS': []})['SS']
        updated_companies = list(set(existing_companies + company_names))  # Merge and deduplicate
        
        # Update item in DynamoDB
        dynamodb.update_item(
            TableName=table_name,
            Key={
                'username': {'S': username}
            },
            UpdateExpression='SET companies = :c',
            ExpressionAttributeValues={
                ':c': {'SS': updated_companies}
            }
        )
        
        print(f"User '{username}' updated with new company names.")
        
    else:
        # User does not exist, create new item
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'username': {'S': username},
                'companies': {'SS': company_names}
            }
        )
        
        print(f"New user '{username}' created with company names.")

def truncate_and_populate_table(data):
    table_name = 'money-mind-general'

    # Scan the table to get all items (used for deletion)
    response = dynamodb.scan(
        TableName=table_name,
        ProjectionExpression='name'
    )

    items = response.get('Items', [])
    
    # Delete each item
    for item in items:
        dynamodb.delete_item(
            TableName=table_name,
            Key={
                'name': item['name']
            }
        )

    # Add each new object to the table
    for obj in data:
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'name': {'S': obj['name']},
                'advice': {'S': obj['advice']}
            }
        )

    print("Table truncated and populated successfully.")


def get_company_names(username):
    table_name = 'money-mind'
    
    # Check if the user exists in DynamoDB
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'username': {'S': username}
        }
    )
    
    if 'Item' in response:
        # User exists, return company names
        return response['Item'].get('companies', {'SS': []})['SS']
    else:
        # User does not exist, return None
        return None
    

def add_company(username, company_name):
    table_name = 'money-mind'
    
    # Check if the user exists in DynamoDB
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'username': {'S': username}
        }
    )
    
    if 'Item' in response:
        # User exists, update company names
        existing_companies = response['Item'].get('companies', {'SS': []})['SS']
        
        if company_name not in existing_companies:
            updated_companies = existing_companies + [company_name]  # Add new company name
            
            # Update item in DynamoDB
            dynamodb.update_item(
                TableName=table_name,
                Key={
                    'username': {'S': username}
                },
                UpdateExpression='SET companies = :c',
                ExpressionAttributeValues={
                    ':c': {'SS': updated_companies}
                }
            )
            
            print(f"Company '{company_name}' added to user '{username}'.")
        else:
            print(f"Company '{company_name}' is already associated with user '{username}'.")
        
    else:
        # User does not exist, create new item
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'username': {'S': username},
                'companies': {'SS': [company_name]}
            }
        )
        
        print(f"New user '{username}' created with company '{company_name}'.")

def remove_company(username, company_name):
    table_name = 'money-mind'
    
    # Check if the user exists in DynamoDB
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'username': {'S': username}
        }
    )
    
    if 'Item' in response:
        # User exists, update company names
        existing_companies = response['Item'].get('companies', {'SS': []})['SS']
        
        if company_name in existing_companies:
            updated_companies = [company for company in existing_companies if company != company_name]  # Remove the company name
            
            # Update item in DynamoDB
            dynamodb.update_item(
                TableName=table_name,
                Key={
                    'username': {'S': username}
                },
                UpdateExpression='SET companies = :c',
                ExpressionAttributeValues={
                    ':c': {'SS': updated_companies}
                }
            )
            
            print(f"Company '{company_name}' removed from user '{username}'.")
        else:
            print(f"Company '{company_name}' is not associated with user '{username}'.")
        
    else:
        # User does not exist
        print(f"User '{username}' does not exist.")

def get_all_data():
    table_name = 'money-mind-general'
    scan_kwargs = {}
    items = []

    # Scan the table to get all items
    done = False
    start_key = None

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        response = dynamodb.scan(TableName=table_name, **scan_kwargs)
        items.extend(response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    # Convert DynamoDB attribute values to strings
    for item in items:
        for key, value in item.items():
            item[key] = value.get('S') if 'S' in value else str(value)

    return items


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


@app.get("/backend/getcompany")
async def hello(request: Request, current_user: dict = Depends(get_current_user)):
    company_names = get_company_names(current_user['email'])
    comdict = []
    for com in company_names:
        comdict.append({"name":com})
    return {"message":comdict}

@app.get("/backend/getportfolio")
def hello(request: Request, current_user: dict = Depends(get_current_user)):
    company_names = get_company_names(current_user['email'])
    newslinks = yc.get_news_links(company_names)
    portfolio = yc.portfolioStockPredictions(newslinks)
    return {"message":portfolio, 'Cross-Origin-Opener-Policy':'same-origin'}

class UserRequest(BaseModel):
    company: str
    
    
@app.post("/backend/addcompany")
def add(user_request: UserRequest, current_user: dict = Depends(get_current_user)):
    add_company(current_user["email"], user_request.company)
    return {"message":"done"}

    
@app.post("/backend/removecompany")
async def add(user_request: UserRequest, current_user: dict = Depends(get_current_user)):
    remove_company(current_user["email"], user_request.company)
    return {"message":"done"}

@app.get("/backend/getgeneral")
def add(current_user: dict = Depends(get_current_user)):
    data = get_all_data()
    print(data)
    return {"message":data, 'Cross-Origin-Opener-Policy':'same-origin'}
