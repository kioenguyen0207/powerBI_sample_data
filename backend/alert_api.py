from tabnanny import check
from request_secureworks import *

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
import json
import csv


def check_label_name(filename='original_alert.csv'):
    with open(filename, 'r', encoding='utf8') as inp, open('alert_api.csv', 'w', encoding='utf8', newline='') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            if row[9] != "suppressed":
                writer.writerow(row)


def refresh_alert(before, after):
    print(f"Requesting from {after} to {before}...\n")
    client_id = config.THIRD_CLIENT_ID
    client_secret = config.THIRD_CLIENT_SECRET
    client = BackendApplicationClient(client_id=client_id)
    oauth_client = OAuth2Session(client=client)
    token = oauth_client.fetch_token(token_url='https://api.ctpx.secureworks.com/auth/api/v2/auth/token', client_id=client_id,
                                     client_secret=client_secret)

    query = """query alerts($before: Time!, $after: Time!) {
        alertsByDate(after:$after, before:$before, orderByField: severity, orderDirection: desc, page_size: 1000) {
            cursor
            edges {
                id
                alert_type
                group_key
                confidence
                severity
                creator
                creator_version
                tenant_id
                message
                attack_categories
                related_entities
                description
                data {
                    domain
                    message
                    timestamp{
                        seconds
                        nanos
                    }
                    domain_registration_date{
                        seconds
                        nanos
                    }
                    attack_categories
                    raw_event
                    username
                    password
                    source_ip
                    destination_ip
                    source_port
                    destination_port
                    alert_extra_data_url
                    alert_extra_data_link_text
                    blacklist_name
                    attack_categories_info{
                        platform
                        system_requirements
                        data_sources
                        defence_bypassed
                        contributors
                        tactics
                        technique_id
                        technique
                        type
                        description
                        url
                        version
                    }
                }
                source {
                    uuid
                    origin
                    source_event
                    event_snippet
                }
                references {
                    description
                    url
                }
                investigations
                investigation_info {
                    investigations {
                        id
                        tenant
                        alerts
                        genesis_alerts
                    }
                }
                insert_timestamp{
                    seconds
                    nanos
                }
                timestamp{
                    seconds
                    nanos
                }
                ranking_data {
                    rank_score
                    ranker
                    ranker_version
                    ranker_model_version
                }
                labels_data{
                    source_id
                    data_id
                    labels
                }
            }
        }
    }"""

    # r = oauth_client.post('https://api.ctpx.secureworks.com/graphql', json={"query": query, "variables": {
    #                       "after": "2020-01-22T20:04:02Z", "before": "2022-02-28T14:13:51-06:00"}}, headers={"X-Tenant-Context": "136279",
    #                       "Authorization": config.AUTHORIZATION})
    # r = oauth_client.post('https://api.ctpx.secureworks.com/graphql', json={"query": query, "variables": {
    #     "after": "2020-03-01T00:00:00Z", "before": "2022-03-18T00:00:00Z"}})
    r = oauth_client.post('https://api.ctpx.secureworks.com/graphql', json={"query": query, "variables": {
        "after": after, "before": before}})

    data = json.loads(r.content)
    edges_data = data['data']['alertsByDate']['edges']
    with open("original_alert.csv", 'w', newline='', encoding='utf-8') as pt_data1:
        csvwriter = csv.writer(pt_data1)
        csvwriter.writerow(["id", "tenant_id", "message", "severity",
                            "timestamp_nanos", "timestamp_seconds", "investigation_id", "investigation_alert", "data_domain", "label_name"])
        for num in edges_data:
            id = num["id"]
            tenant_id = num["tenant_id"]
            message = num["message"]
            severity = num["severity"]
            timestamp_nanos = num['timestamp']['nanos']
            timestamp_seconds = num['timestamp']['seconds']
            investigation_id = ""
            investigation_alert = ""
            data_domains = ""
            label_name = ""
            try:
                investigation_id = num['investigation_info']['investigations'][0]['id']
                investigation_alert = num['investigation_info']['investigations'][0]['alert']
            except:
                pass
            try:
                data_domain = num['data'][0]['domain']
            except:
                pass
            try:
                label_name = num['labels_data']['labels']['suppressionRule']['label_name']
            except:
                pass
            csvwriter.writerow(
                [id, tenant_id, message, severity, timestamp_nanos, timestamp_seconds, investigation_id, investigation_alert, data_domain, label_name])
    check_label_name()


if __name__ == "__main__":
    refresh_alert("2022-03-18T00:00:00Z", "2020-03-01T00:00:00Z")
