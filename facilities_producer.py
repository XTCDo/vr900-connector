import uuid
import traceback
import os
import tempfile
import json
import shutil
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from vr900connector.api import ApiConnector, ApiError, constant


def print_responses(user, password):
    connector = ApiConnector(user, password, file_dir=tempfile.gettempdir() + "/" + str(uuid.uuid4()))

    try:
        live_report_data = connector.get(constant.LIVE_REPORT_URL)
        print(extract_data_from_json(live_report_data))
    except Exception as e:
        print(e)

    connector.logout()


def extract_data_from_json(json_data):
    flow_temperature_sensor_value = json_data['body']['devices'][0]['reports'][0]['value']
    water_pressure_sensor_value = json_data['body']['devices'][1]['reports'][0]['value']
    domestic_hot_water_tank_temperature_value = json_data['body']['devices'][2]['reports'][0]['value']
    extracted_data = {
        "flow_temperature_sensor_value" : flow_temperature_sensor_value,
        "water_pressure_sensor_value" : water_pressure_sensor_value,
        "domestic_hot_water_tank_temperature_value" : domestic_hot_water_tank_temperature_value
    }
    extracted_data = json.dumps(extracted_data)
    return extracted_data


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('--username', '-u', help='Username used to connect', dest='username',
                        required=True)
    parser.add_argument('--password', '-p', help='Password used to connect', dest='password',
                        required=True)

    args = parser.parse_args()
    print_responses(args.username, args.password)
