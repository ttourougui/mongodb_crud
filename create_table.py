#!/usr/bin/python3

import boto3
from botocore.exceptions import ClientError
import logging

table_name = 'characters'


def create_table(table_name, dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
  try:
    response = dynamodb.create_table(
      TableName=table_name,
      KeySchema=[
          {
            'AttributeName': 'char_id',
            'KeyType': 'HASH'  
          },
          {
            'AttributeName': 'name',
            'KeyType': 'RANGE' 
          },
          

      ],
      AttributeDefinitions=[
          {
            'AttributeName': 'char_id',
            'AttributeType': 'N'
          },
          {
            'AttributeName': 'name',
            'AttributeType': 'S'
          },
          {
            'AttributeName': 'nickname',
            'AttributeType': 'S'
          },
      ],
      GlobalSecondaryIndexes= [ 
      { 
         'IndexName': 'NameIndex',
         'KeySchema': [ 
            {
              'AttributeName': 'name',
              'KeyType': 'HASH'  
            },
            {
              'AttributeName': 'nickname',
              'KeyType': 'RANGE'  
            },

         ],
         'Projection': { 
            'ProjectionType': 'ALL'
         },
         'ProvisionedThroughput': { 
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
         }
      }
   ],
      ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
      }
    )
    return response
  except ClientError as e:
    logging.error(e.response['Error']['Message'])
    return


def check_table_status(table_name, dynamodb=None):
  status = False
  if not dynamodb:
    dynamodb = boto3.client('dynamodb', region_name='eu-central-1')
  try:
    response = dynamodb.describe_table(TableName=table_name)
    status = response['Table']['TableStatus']
  except ClientError as e: 
    logging.error(e.response['Error']['Message'])
  else: 
    return status

def check_table_exists(table_name, dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
  table_names = [table.name for table in dynamodb.tables.all()]
  if table_name in table_names:
    return True


if __name__ == '__main__':
  table = create_table(table_name)
  logging.info('Table status: '+table.table_status)
