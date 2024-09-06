from pollux_framework.database.influxdb_driver import InfluxdbDriver
from pollux_framework.database.csv_driver import CsvDriver
from datetime import datetime, timedelta, timezone
import logging
import pytz
import os

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

tzobject = pytz.timezone('Europe/Amsterdam')


class InfluxdbCsvConnector:

    def __init__(self, category):
        self.category = category
        self.internal_db_driver = InfluxdbDriver()
        self.external_db_driver = CsvDriver()

        self.tags = []
        self.parameters = dict()
        self.delta_t = 600

    def update_parameters(self, parameters):
        for key, value in parameters.items():
            self.parameters[key] = value

        self.delta_t = self.parameters[self.category]['interval']

        self.external_db_driver.update_parameters({})

        influxdb_param = {
            "url": os.getenv('INFLUXDB_URL', 'http://localhost:8086'),
            "org": os.getenv('INFLUXDB_ORG', 'TNO'),
            "username": os.getenv('INFLUXDB_USERNAME', 'pollux-user'),
            "password": os.getenv('INFLUXDB_PASSWORD', 'pollux-password'),
            "bucket": os.getenv('INFLUXDB_BUCKET', 'pollux-project'),
        }

        self.internal_db_driver.update_parameters(influxdb_param)

    def connect(self):
        self.internal_db_driver.connect()
        self.external_db_driver.connect()

    def disconnect(self):
        self.internal_db_driver.disconnect()
        self.external_db_driver.disconnect()

    def register_tags(self, units):
        for unit in units:
            for key, value in unit.tagnames[self.category].items():
                tag = {'plant_name': unit.plant.name,
                       'asset_name': unit.name,
                       'internal_tagname': key + '.' + self.category,
                       'external_tagname': value}

                self.tags.append(tag)

    def delete(self, plant_name):
        self.internal_db_driver.delete_database_all(plant_name)

    def import_raw_data(self):
        endtime_str = self.get_current_time_str()

        for tag in self.tags:
            if tag['external_tagname'] == '':
                continue

            starttime_str = self.get_internal_database_last_time_str(tag['plant_name'],
                                                                     tag['asset_name'],
                                                                     tag['internal_tagname'])

            if not (starttime_str == endtime_str):
                try:
                    logger.info('Reading ' + tag[
                        'external_tagname'] + ' from ' + starttime_str + ' to ' + endtime_str)

                    result, time = self.read_external_database(tag['external_tagname'],
                                                               starttime_str, endtime_str)

                    logger.info('Writing : ' + tag['internal_tagname'] + ' of ' + tag[
                        'asset_name'] + ' from ' + starttime_str + ' to ' + endtime_str)

                    self.write_internal_database(tag['plant_name'], tag['asset_name'],
                                                 tag['internal_tagname'], time, result)
                except Exception as err:
                    logger.error(err)

    def get_current_time_str(self):
        endtime_datetime = self.round_minutes(datetime.utcnow(), 'down', self.delta_t / 60)
        endtime_str = endtime_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

        return endtime_str

    def get_internal_database_last_time_str(self, plant_name, asset_name, tagname):
        _, timestamps = self.internal_db_driver.get_last_data(plant_name, asset_name, tagname)

        if timestamps:
            starttime_str = timestamps[0]
        else:
            starttime_datetime = datetime.strptime(self.parameters['start_time'],
                                                   '%Y-%m-%d %H:%M:%S')
            starttime_datetime = tzobject.localize(starttime_datetime)
            starttime_str = starttime_datetime.astimezone(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ")

        return starttime_str

    def read_external_database(self, external_tagname, starttime_str, endtime_str):
        result, time = self.external_db_driver.read_data(external_tagname,
                                                         starttime_str, endtime_str)

        return result, time

    def write_internal_database(self, plant_name, asset_name, internal_tagname, time, result):
        self.internal_db_driver.write_data(plant_name, asset_name,
                                           internal_tagname, time, result)

    def read_internal_database(self, plant_name, asset_name, internal_tagname, starttime_str,
                               endtime_str, timestep):

        result, time = self.internal_db_driver.read_data(plant_name, asset_name,
                                                         internal_tagname, starttime_str,
                                                         endtime_str, timestep)

        return result, time

    @staticmethod
    def round_minutes(dt, direction, resolution):
        new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution

        return dt + timedelta(minutes=new_minute - dt.minute, seconds=-dt.second,
                              microseconds=-dt.microsecond)
