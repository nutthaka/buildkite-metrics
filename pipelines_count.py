#!/usr/bin/env python3

import json
import requests
from future.utils import iteritems
from string import Template
from date_range import get_date_tuples
from datetime import datetime
import os

BK_ACCESS_TOKEN = os.environ['BK_ACCESS_TOKEN']
BK_GRAPHQL_URL = 'https://graphql.buildkite.com/v1'
BK_HEADERS = {'Authorization': 'Bearer ' + BK_ACCESS_TOKEN}
BK_ORGANIZATION = os.environ['BK_ORGANIZATION']

date_tuples = get_date_tuples(1)

query_template = Template('''{ 
    organization(slug: "$BK_ORGANIZATION") { 
        pipelines(first: 500) { 
            edges { 
                node { 
                    name, 
                    builds(createdAtFrom: "$createdFrom", createdAtTo:"$createdTo") { 
                        count 
                    } 
                } 
            } 
        } 
    } 
}''')

print('DateTime,Total builds')
for item in date_tuples:    
    request_body = {'query': query_template.substitute(BK_ORGANIZATION=BK_ORGANIZATION, createdFrom=item[0], createdTo=item[1])}     
    response = requests.post(BK_GRAPHQL_URL, headers = BK_HEADERS, data = json.dumps(request_body))
    pipelines = response.json()['data']['organization']['pipelines']['edges']
    total_builds = 0
    build_dict = {}

    for pipeline in pipelines:
        build_dict[pipeline['node']['name']] = pipeline['node']['builds']['count']
        total_builds += pipeline['node']['builds']['count']

    output_template = Template('$datetime,$count')
    print(output_template.substitute(datetime=datetime.strptime(item[0], '%Y-%m-%dT%H:%M:%S%z').date(), count=str(total_builds)))

# sort_key = lambda t: (t[1], t[0])
# sorted_pipelines = sorted(iteritems(build_dict), key=sort_key)

# for key, value in sorted_pipelines:
#     print("%s: %s" % (key, value))    
