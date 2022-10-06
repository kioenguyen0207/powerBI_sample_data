from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
import json
import csv

from request_secureworks import config

client_id = config.THIRD_CLIENT_ID
client_secret = config.THIRD_CLIENT_SECRET
client = BackendApplicationClient(client_id=client_id)
oauth_client = OAuth2Session(client=client)
token = oauth_client.fetch_token(token_url='https://api.ctpx.secureworks.com/auth/api/v2/auth/token', client_id=client_id,
                                 client_secret=client_secret)


# Show me the first 100 assets (All) - options are All | Active | Deleted
allAssetsQuery = '''
{
  allAssets(
    offset: 0,
    order_by: hostname,
    filter_asset_state: All
  )
  {
    totalResults
    assets {
      id
      hostId
      sensorTenant
      sensorId
      sensorVersion
      endpointType
      hostnames {
        hostname
      }
    }
  }
}
'''

result = oauth_client.post('https://api.ctpx.secureworks.com/graphql',
                           json={"query": allAssetsQuery})
data = json.loads(result.content)
data = data['data']['allAssets']['assets']

with open("assets_api.csv", 'w', newline='', encoding='utf-8') as pt_data1:
    csvwriter = csv.writer(pt_data1)
    csvwriter.writerow(["id", "hostId", "sensorTenant",
                       "sensorId", "sensorVersion", "endpointType", "hostname"])
    for num in data:
        id = num["id"]
        hostId = num["hostId"]
        sensorTenant = num["sensorTenant"]
        sensorId = num["sensorId"]
        sensorVersion = num["sensorVersion"]
        endpointType = num["endpointType"]
        hostname = num["hostnames"][0]['hostname']
        csvwriter.writerow(
            [id, hostId, sensorTenant, sensorId, sensorVersion, endpointType, hostname])
