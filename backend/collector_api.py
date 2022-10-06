from request_secureworks import *


from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from graphqlclient import GraphQLClient


import json
import pprint

# We need to first set up our client token and GraphQL client instance
pp = pprint.PrettyPrinter(depth=6)
client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
client = BackendApplicationClient(client_id=client_id)
oauth_client = OAuth2Session(client=client)
token = oauth_client.fetch_token(
    token_url='https://api.ctpx.secureworks.com/auth/api/v2/auth/token', client_id=client_id, client_secret=client_secret)

gql_client = GraphQLClient('https://api.ctpx.secureworks.com/graphql')
gql_client.inject_token('Bearer ' + token['access_token'], 'Authorization')

# Let's start off by creating a new collector
createCollectorQuery = gql_client.execute(
    '''
mutation {
  createCluster(
    clusterInput: {
      name: "sample-collector"
      description: "a collector created from a script!"
      network: { dhcp: true, hostname: "sample-collector-host" }
    }
  ) {
    createdAt
    id
    name
    description
    network {
      dhcp
      hostname
    }
  }
}
'''
)

# We can now decode the response and print it out
result = json.loads(createCollectorQuery)
# Barring any errors, we should the our new created 'sample-collector' information printed out
pp.pprint(result)

# Now let's try to list all of our created collectors
getAllClustersQuery = gql_client.execute(
    '''
query {
  getAllClusters(role: "collector") {
    createdAt
    updatedAt
    id
    name
    description
    health
    network {
      dhcp
      hostname
      dns
      ntp
      proxy
    }
    deployments {
      name
      id
      config
    }
    status {
      id
      createdAt
    }
  }
}
''')

# We can now decode the response and print it out
result = json.loads(getAllClustersQuery)
# Barring any errors, we should see our newly created 'sample-collector' listed
pp.pprint(result)
