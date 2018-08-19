#!/usr/bin/env python3

import json
import requests
from future.utils import iteritems
from string import Template
from date_range import get_date_tuples

BK_ACCESS_TOKEN = ""
BK_GRAPHQL_URL = "https://graphql.buildkite.com/v1"
BK_HEADERS = {'Authorization': 'Bearer ' + BK_ACCESS_TOKEN}

query_template = Template('{ organization(slug: "") { pipelines(first: 500) { edges { node { name, builds(createdAtFrom: "$createdFrom", createdAtTo:"$createdTo") { count } } } } } }')

GRAPHQL_DATA_1 = {"query": query_template.substitute(createdFrom="2018-08-16T08:00+10", createdTo="2018-08-17T08:00+10")}
GRAPHQL_DATA_2 = {"query": query_template.substitute(createdFrom="2018-08-19T08:00+10", createdTo="2018-08-20T08:00+10")}

list_of_request_body = [GRAPHQL_DATA_1, GRAPHQL_DATA_2]

print("Day,Total builds")
for (i, request_body) in enumerate(list_of_request_body):
    response = requests.post(BK_GRAPHQL_URL, headers = BK_HEADERS, data = json.dumps(request_body))
    build_pipelines = response.json()['data']['organization']['pipelines']['edges']
    total_builds = 0
    build_dict = {}

    for pipeline in build_pipelines:
        build_dict[pipeline['node']['name']] = pipeline['node']['builds']['count']
        total_builds += pipeline['node']['builds']['count']

    output_template = Template('$day,$count')
    print(output_template.substitute(day=str(i+1), count=str(total_builds)))

    
