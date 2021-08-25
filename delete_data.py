#!/usr/bin/python3

import logging
import json
from create_table import create_table, check_table_status, check_table_exists
from read_data import get_char_by_id_name
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

import sys

logging.basicConfig(level = logging.INFO)

def delete_character(table_name, char_id, name, dynamodb=None):
  if not dynamodb:
      dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

  table = dynamodb.Table(table_name)

  if not get_char_by_id_name(table_name, char_id, name, dynamodb): #Check if character already exist in the table
    logging.warning(name+' Character does not exists!')
    return None

  try:
    response = table.delete_item(
      Key={
        'char_id': int(char_id),
        'name': name
      },
    )
    logging.info('Character has been deleted.')
    print(response)
    return response
  except ClientError as e:
    if e.response['Error']['Code'] == "ConditionalCheckFailedException":
      print(e.response['Error']['Message'])
    else:
      raise
  else:
    return response

if __name__ == '__main__':

  table_name = 'characters'
  char_id = input('Enter character ID: ')
  name = input('Enter character name: ')

  delete_character(table_name, char_id, name)