"""
This module is used to connect to Trello Client
"""
import os
import logging
from trello import TrelloClient
from dotenv import load_dotenv

def get_client():
    #load environment variables
    load_dotenv(override=True)
    api_key = os.getenv('TRELLO_API_KEY')
    api_secret = os.getenv('TRELLO_API_SECRET')
    token = os.getenv('TRELLO_API_TOKEN')

    logging.info('Connecting with: api_key={}, api_secret={}, token={}'.format(api_key, api_secret, token))

    #connect to trello client
    client = TrelloClient(
        api_key=api_key,
        api_secret=api_secret,
        token=token
    )

    return client
