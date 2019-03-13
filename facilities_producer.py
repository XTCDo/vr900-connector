import uuid
import tempfile
import json
from time import sleep
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from vr900connector.api import ApiConnector, constant

from kafka import KafkaProducer


def print_responses(connector):
    try:
        live_report_data = connector.get(constant.LIVE_REPORT_URL)
        print(extract_data_from_json(live_report_data))
    except Exception as e:
        print(e)

    connector.logout()


def extract_data_from_json(json_data):
    json_data = json_data['body']['devices']
    flow_temperature_sensor_value = json_data[0]['reports'][0]['value']
    water_pressure_sensor_value = json_data[1]['reports'][0]['value']
    domestic_hot_water_tank_temperature_value = json_data[2]['reports'][0]['value']

    extracted_data = {
        "flow_temperature_sensor_value": flow_temperature_sensor_value,
        "water_pressure_sensor_value": water_pressure_sensor_value,
        "domestic_hot_water_tank_temperature_value": domestic_hot_water_tank_temperature_value
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

    connector = ApiConnector(args.username, args.password, file_dir=tempfile.gettempdir() + "/" + str(uuid.uuid4()))

    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        message = extract_data_from_json(connector.get(constant.LIVE_REPORT_URL))
        print(message)
        producer.send('vaillant-input', message.encode('utf-8'))
        sleep(60)
