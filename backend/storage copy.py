import boto3
from os import getenv
from dotenv import load_dotenv
load_dotenv()

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


#print(get_company_names("mishal0404"))

update_user("mishal0404@gmail.com", ["microsoft", "apple", "google"])
