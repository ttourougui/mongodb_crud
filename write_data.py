#!/usr/bin/python3

import logging
import requests
import json
from fetch_data import fetch_chars
from create_table import create_table, check_table_status, check_table_exists
from read_data import get_char_by_id_name
import boto3
import time
from botocore.exceptions import ClientError

from create_table import table_name


logging.basicConfig(level = logging.INFO)


def write_char(data, table_name, dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

  table = dynamodb.Table(table_name)
  if get_char_by_id_name(table_name, data['char_id'], data['name'], dynamodb): #Check if character already exist in the table
    logging.warning(data['name']+' Character already exists!')
    return None
  try:
    logging.info("Writing "+data['name'])
    
    response = table.put_item(
      Item={
        'char_id': data['char_id'],
        'name': data['name'],
        'birthday': data['birthday'],
        'occupation': data['occupation'],
        'img': data['img'],
        'status': data['status'],
        'nickname': data['nickname'],
        'appearance': data['appearance'],
        'portrayed': data['portrayed'],
        'category': data['category'],
      }
    )
  except ClientError as e:
    logging.error(e.response['Error']['Message'])

    return response

if __name__ == '__main__':

  new_table = None
  if not check_table_exists(table_name): #ensure table exist and avoid table already exists error
    new_table = create_table(table_name)

  if new_table != None:
    while check_table_status(table_name) != 'ACTIVE': #ensure that the table is ready for writing
      logging.info('Waiting for table creation ...')
      time.sleep(1)
    data = fetch_chars()

    for item in data: #writing data
      write_char(item, table_name)