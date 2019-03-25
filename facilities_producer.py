import uuid
import tempfile
import json
from time import sleep
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from vr900connector.api import ApiConnector, constant

from kafka import KafkaProducer


def extract_data_from_json(json_data):
    """Helper function to extract three sensor values out of a json object"""

    # Do extraction and store in variables
    json_data = json_data['body']['devices']
    flow_temperature_sensor_value = json_data[0]['reports'][0]['value']
    water_pressure_sensor_value = json_data[1]['reports'][0]['value']
    domestic_hot_water_tank_temperature_value = json_data[2]['reports'][0]['value']

    # Put variables in a dictionary
    extracted_data = {
        "flow_temperature_sensor_value": flow_temperature_sensor_value,
        "water_pressure_sensor_value": water_pressure_sensor_value,
        "domestic_hot_water_tank_temperature_value": domestic_hot_water_tank_temperature_value
    }

    # Turn dictionary in JSON string
    extracted_data = json.dumps(extracted_data)
    return extracted_data


# If the program is run standalone use this as main loop
if __name__ == '__main__':
    # ArgumentParser is used to get the username and password from the command line
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('--username', '-u', help='Username used to connect', dest='username',
                        required=True)
    parser.add_argument('--password', '-p', help='Password used to connect', dest='password',
                        required=True)

    args = parser.parse_args()

    # Create the ApiConnector using the provided username and password and make it use a temporary directory
    connector = ApiConnector(args.username, args.password, file_dir=tempfile.gettempdir() + "/" + str(uuid.uuid4()))

    # Create a KafkaProducer for local usage
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        # Get json data from ApiConnector and then extract the data from it
        vaillant_data_json = connector.get(constant.LIVE_REPORT_URL)
    
        message = extract_data_from_json(vaillant_data_json)

        print(message)

        # Send extracted json data to the vaillant-input Kafka topic
        producer.send('vaillant-input', message.encode('utf-8'))
        sleep(60)
