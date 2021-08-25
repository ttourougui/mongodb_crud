#!/usr/bin/python3

import logging
import json
from create_table import create_table, check_table_status, check_table_exists
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import sys

from create_table import table_name

logging.basicConfig(level = logging.INFO)

def update_char_nickname(table_name, char_id, name, nickname, dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name="eu-central-1")

  table = dynamodb.Table(table_name)
  try:
    response = table.update_item(
      Key={
          'char_id': int(char_id),
          'name': name,
      },
      UpdateExpression="set nickname = :nickname",
      ExpressionAttributeValues={
          ':nickname': nickname,
      },
      ReturnValues="UPDATED_NEW"
    )
    print(response)
    return response
  except ClientError as e:
    logging.error(e.response['Error']['Message'])

    return 

def add_char_occupation(table_name, char_id, name, occupation, dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name="eu-central-1")

  table = dynamodb.Table(table_name)
  try:
    response = table.update_item(
      Key={
          'char_id': int(char_id),
          'name': name,
      },
      UpdateExpression="SET #attrName = list_append(#attrName, :attrValue)",
      ExpressionAttributeNames={"#attrName": "occupation"},
      ExpressionAttributeValues={":attrValue": [occupation]},
      ReturnValues="UPDATED_NEW"
    )
    print(response)
    return response
  except ClientError as e:
    logging.error(e.response['Error']['Message'])

    return 




if __name__ == '__main__':

  char_id = input('Enter character ID: ')
  name = input('Enter character name: ')
  # nickname = input('Enter the new nickname: ')
  occupation = input('Enter additional character occupation: ')

  # update_char_nickname(table_name, char_id, name, nickname)
  add_char_occupation(table_name, char_id, name, occupation)

