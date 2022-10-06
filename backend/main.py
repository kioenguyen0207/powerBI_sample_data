from calendar import week
from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource, reqparse
from collections import Counter

import numpy as np
from alert_api import refresh_alert
from investigation_api import refresh_investigation
from helper import get_csv_column, week_time, year_time, last_two_weeks_time
import json

DATA = ('alert_api.csv')
THIS_YEAR = '2022'
app = Flask(__name__)
api = Api(app)


def statisting(data, date, sorter):
    formated_data = {
        'date': date,
        'sorter': sorter,
        'low': 0,
        'medium': 0,
        'high': 0,
        'critical': 0,
        'line': 0
    }
    for value in data:
        if value < 0.5:
            formated_data['low'] += 1
        if value == 0.5:
            formated_data['medium'] += 1
        if value == 0.75:
            formated_data['high'] += 1
        if value > 0.75:
            formated_data['critical'] += 1
    formated_data['line'] = formated_data['medium'] + \
        formated_data['high']  # critical removed

    return formated_data


class column_chart(Resource):
    def get(self):
        date_data = last_two_weeks_time()
        ret_count = []
        for date in date_data:
            try:
                # refresh_alert(date['before'], date['after'])
                # 1st graph
                data = get_csv_column(DATA, 'severity')
                statisted_data = statisting(
                    data, date['date'], date['date_sorter'])
                ret_count.append(statisted_data)
            except:
                sample_data = {
                    'date': date['date'],
                    'sorter': date['date_sorter'],
                    'low': 0,
                    'medium': 0,
                    'high': 0,
                    'critical': 0,
                    'line': 0
                }
                ret_count.append(sample_data)

        return {'data': ret_count}, 200


class horizontal_chart(Resource):
    def get(self):
        # 2nd graph
        ret = []
        # refresh_alert(year_time(THIS_YEAR)[
        #     'before'], year_time(THIS_YEAR)['after'])
        domain_data = get_csv_column(DATA, "data_domain")
        formated_domain_data = list(map(str, domain_data))
        counter = Counter(formated_domain_data).most_common(11)
        for value in counter:
            if str(value[0]) == "nan":
                continue
            ret.append({
                'domain': str(value[0]),
                'amount': int(value[1])
            })
        return {
            'domain_data': ret
        }, 200


class grid_chart(Resource):
    def get(self):
        ret = {}
        ret_dict = []
        # default values RMS, Emily, IT Infra
        ret_dict.append({
            'domain': 'RMS',
            'severity': 0,
            'size': 1
        })
        ret_dict.append({
            'domain': 'Emily',
            'severity': 0,
            'size': 1
        })
        ret_dict.append({
            'domain': 'IT Infra',
            'severity': 0,
            'size': 1
        })

        # refresh_alert(year_time(THIS_YEAR)[
        #     'before'], year_time(THIS_YEAR)['after'])
        domain = get_csv_column(DATA, "data_domain")
        severity = get_csv_column(DATA, "severity")
        domain_data = list(map(str, domain))
        severity_data = list(map(float, severity))
        domain_count = Counter(domain_data).keys()
        for i in range(len(domain_data)):
            if domain_data[i] == "nan":
                continue
            if domain_data[i] not in ret:
                ret[domain_data[i]] = severity_data[i]
            elif severity_data[i] > ret[domain_data[i]]:
                ret[domain_data[i]] = severity_data[i]
            else:
                pass
        for key in ret:
            ret_dict.append({
                'domain': key,
                'severity': ret[key],
                'size': 1/len(domain_count)
            })
        return {
            'grid': ret_dict
        }


class map_chart(Resource):
    def get(self):
        ret = []
        ret.append({
            'location': 'USA',
            'color_value': 0
        })
        ret.append({
            'location': 'Singapore',
            'color_value': 1
        })
        ret.append({
            'location': 'China',
            'color_value': 2
        })
        return {
            'map': ret
        }


class investigation_count(Resource):
    def get(self):
        # refresh_investigation()
        status_data = get_csv_column('investigation_api.csv', 'status')
        counter = 0
        for value in status_data:
            if value == 'Open':
                counter += 1
        return {
            'investigation_open': counter
        }

# for quick loading time


class json1(Resource):
    def get(self):
        f = open('refresh1.json', 'r')
        data = json.load(f)
        f.close()
        return data


class json2(Resource):
    def get(self):
        f = open('refresh2.json', 'r')
        data = json.load(f)
        f.close()
        return data


# api.add_resource(column_chart, "/daily")
api.add_resource(json1, "/daily")
api.add_resource(horizontal_chart, "/domains")
api.add_resource(grid_chart, "/grid")
api.add_resource(map_chart, "/map")
api.add_resource(investigation_count, "/open_count")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
