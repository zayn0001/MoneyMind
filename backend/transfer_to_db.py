import boto3
from dotenv import load_dotenv
from os import getenv, path

app_base = path.dirname(__file__)
app_root = path.join(app_base, '../')

load_dotenv(dotenv_path=path.join(app_root, '.env.local'))
session = boto3.Session(
    aws_access_key_id=getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=getenv("AWS_SECRET"),
    region_name='us-west-1'  # e.g., 'us-east-1'
)

# Create a DynamoDB client
dynamodb = session.client('dynamodb')


def truncate_and_populate_table(data):
    table_name = 'money-mind-general'

    # Scan the table to get all items (used for deletion)
    response = dynamodb.scan(
        TableName=table_name,
        ProjectionExpression='ticker'
    )

    items = response.get('Items', [])
    print(items)
    # Delete each item
    for item in items:
        dynamodb.delete_item(
            TableName=table_name,
            Key={
                'ticker': {"S":item['ticker']["S"]}
            }
        )

    # Add each new object to the table
    for obj in data:
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'ticker': {'S': obj['name']},
                'advice': {'S': obj['advice']}
            }
        )

    print("Table truncated and populated successfully.")
