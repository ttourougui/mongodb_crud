#!/usr/bin/python3

import logging
import json
from create_table import create_table, check_table_status, check_table_exists
import boto3
from botocore.exceptions import ClientError

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

# print(get_char_by_id_name('characters', '1', 'Walter White'))