from distutils.command.config import config
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from graphqlclient import GraphQLClient
from request_secureworks import config

import os
import json
import csv


def refresh_investigation():
    print('Requesting to investigation API...')
    client_id = config.THIRD_CLIENT_ID
    client_secret = config.THIRD_CLIENT_SECRET
    client = BackendApplicationClient(client_id=client_id)
    oauth_client = OAuth2Session(client=client)
    token = oauth_client.fetch_token(token_url='https://api.ctpx.secureworks.com/auth/api/v2/auth/token', client_id=client_id,
                                     client_secret=client_secret)

    gql_client = GraphQLClient('https://api.ctpx.secureworks.com/graphql')
    gql_client.inject_token("Bearer " + token['access_token'], "Authorization")
    result = gql_client.execute('''
  {
    allInvestigations {
      id
      description
      status
    }
  }
  ''')
    data = json.loads(result)
    data = data['data']['allInvestigations']
    with open("investigation_api.csv", 'w', newline='', encoding='utf-8') as pt_data1:
        csvwriter = csv.writer(pt_data1)
        csvwriter.writerow(["id", "description", "status"])
        for num in data:
            id = num["id"]
            description = num["description"]
            status = num["status"]
            csvwriter.writerow(
                [id, description, status])
