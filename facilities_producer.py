import uuid
import traceback
import os
import tempfile
import json
import shutil
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from vr900connector.api import ApiConnector, ApiError, constant


def print_responses(user, password, result_dir):
    connector = ApiConnector(user, password, file_dir=tempfile.gettempdir() + "/" + str(uuid.uuid4()))

    shutil.rmtree(result_dir, ignore_errors=True)
    os.mkdir(result_dir)

    #with open(result_dir + '/facilities', 'w+') as file:
    #    secure_call(connector, constant.FACILITIES_URL, file)

    #with open(result_dir + '/system_status', 'w+') as file:
    #    secure_call(connector, constant.SYSTEM_STATUS_URL, file)

    # Belangrijkste
    #with open(result_dir + '/live_report', 'w+') as file:
    #    secure_call(connector, constant.LIVE_REPORT_URL, file)

    #with open(result_dir + '/system_control', 'w+') as file:
    #    secure_call(connector, constant.SYSTEM_CONTROL_URL, file)

    #with open(result_dir + '/hvac_state', 'w+') as file:
    #    secure_call(connector, constant.HVAC_STATE_URL, file)

    try:
        live_report_data = connector.get(constant.LIVE_REPORT_URL)
        extract_data_from_json(live_report_data)
        #print(json.dumps(live_report_data, indent=1))
    except Exception as e:
        print(e)

    connector.logout()


def secure_call(connector, url, file):
    try:
        file.write(json.dumps(connector.get(url), indent=4))
    except ApiError as e:
        if e.response is not None:
            file.write(e.response.text)
        else:
            file.write(e.message + '\n')
            traceback.print_exc(file=file)
    except Exception as e:
        traceback.print_exc(file=file)


def extract_data_from_json(json_data):
    flow_temperature_sensor_value = json_data['body']['devices'][0]['reports'][0]['value']
    water_pressure_sensor_value = json_data['body']['devices'][1]['reports'][0]['value']
    domestic_hot_water_tank_temperature_value = json_data['body']['devices'][2]['reports'][0]['value']
    print(flow_temperature_sensor_value)
    print(water_pressure_sensor_value)
    print(domestic_hot_water_tank_temperature_value)



if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('--username', '-u', help='Username used to connect', dest='username',
                        required=True)
    parser.add_argument('--password', '-p', help='Password used to connect', dest='password',
                        required=True)
    parser.add_argument('--dir', '-d', help='Where to store files', dest='dir',
                        required=True)

    args = parser.parse_args()
    print_responses(args.username, args.password, args.dir)
