#!/usr/bin/python3

import logging
import json
from create_table import create_table, check_table_status, check_table_exists
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import sys

logging.basicConfig(level = logging.INFO)

def get_char_by_id_name(table_name, char_id, char_name, dynamodb=None):
  response = []
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name="eu-central-1")
  table = dynamodb.Table(table_name)
  try:
    response = table.get_item(Key={'char_id': int(char_id), 'name': char_name})
    if 'Item' in response:
      return True
  except ClientError as e:
    logging.error(e.response['Error']['Message'])
  else: return False

def query_char(table_name, char_name,dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name="eu-central-1")
  if not check_table_exists(table_name):
    logging.error('Table does not exist')
    return
  table = dynamodb.Table(table_name)
  response = table.query(
    IndexName='NameIndex',
    KeyConditionExpression=Key('name').eq(char_name)
    )
  return response['Items']

if __name__ == '__main__':

  char_name = input("Enter character's name: ")
  characters = query_char('characters', char_name)
  if characters:
    for char in characters:
      print(char)
  else:
    print('no character goes by that name')
