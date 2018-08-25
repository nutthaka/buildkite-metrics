#!/usr/bin/env python3

import requests
import json
from string import Template
import os

BK_ACCESS_TOKEN = os.environ['BK_ACCESS_TOKEN']
BK_GRAPHQL_URL = "https://graphql.buildkite.com/v1"
BK_HEADERS = {'Authorization': 'Bearer ' + BK_ACCESS_TOKEN}
BK_ORGANIZATION = os.environ['BK_ORGANIZATION']

query_template = Template('''{ 
    organization(slug: "$BK_ORGANIZATION") { 
        pipelines(first: 500) { 
            count 
            edges {
                node {
                    name 
                }
            }
        }
    }
}''')

request_body = {"query": query_template.substitute(BK_ORGANIZATION=BK_ORGANIZATION)}     
response = requests.post(BK_GRAPHQL_URL, headers = BK_HEADERS, data = json.dumps(request_body))
pipelines = response.json()['data']['organization']['pipelines']['edges']

for pipeline in pipelines:
    print(pipeline['node']['name'])
