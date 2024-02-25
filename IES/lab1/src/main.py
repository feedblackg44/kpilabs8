import os
import time

from paho.mqtt import client as mqtt_client

import config
from schema import AggregatedDataSchema, AggregatedTemperatureSchema
from domain import AggregatedData, Accelerometer, Gps, AggregatedTemperature, Temperature
from file_datasource import FileDatasource
from autocreator import AutoCreator


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(*args, **kwargs):
    client, delay = args
    topics = kwargs.get('topics')
    datasources = kwargs.get('datasources')
    schemas = kwargs.get('schemas')
    for datasource in datasources:
        datasource.startReading()
    while True:
        time.sleep(delay)
        for topic, datasource, schema in zip(topics, datasources, schemas):
            data = datasource.read()
            msg = schema().dumps(data)
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                pass
                # print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


def run():
    temperature_file_name = "data/temperature.csv"
    temperature_rows_amount = 100

    if not os.path.exists(temperature_file_name):
        kwargs = {
            "data_names": ["temperature, C"],
            "data_types": [float],
            "bounds": [(-10, 30)]
        }
        autocreator = AutoCreator(**kwargs)
        autocreator.create(temperature_file_name, temperature_rows_amount)

    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource_accelerometer = FileDatasource(AggregatedData,
                                              filetypes=[Accelerometer, Gps],
                                              filenames=['data/accelerometer.csv',
                                                         'data/gps.csv'])
    datasource_temperature = FileDatasource(AggregatedTemperature,
                                            filetypes=[Temperature, Gps],
                                            filenames=[temperature_file_name,
                                                       'data/gps.csv'])
    # Infinity publish data
    publish(client, config.DELAY,
            topics=[config.MQTT_TOPIC_MAIN, config.MQTT_TOPIC_SELF],
            datasources=[datasource_accelerometer, datasource_temperature],
            schemas=[AggregatedDataSchema, AggregatedTemperatureSchema])


if __name__ == '__main__':
    run()
