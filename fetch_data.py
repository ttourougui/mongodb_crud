#!/usr/bin/python3

import logging
import requests
import json

base_url = 'https://breakingbadapi.com'

def beautify(data):
  return json.dumps(data, sort_keys=True, indent=4)

def fetch_chars():
  url = base_url + '/api/characters'
  data = {}
  try: 
    response = requests.get(url) 
    response.raise_for_status()
    if response.ok:
      data =  response.json()
      return data
  except requests.exceptions.Timeout:
    logging.error('Timeout')
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)


if __name__ == '__main__':
  data = fetch_chars()

