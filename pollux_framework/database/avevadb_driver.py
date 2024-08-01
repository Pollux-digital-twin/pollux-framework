import adh_sample_library_preview as dbconn
from datetime import datetime
import pandas as pd
import math
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class AvevaDriver:
    """ database driver based on AVEVA"""

    def __init__(self):
        """ Establish connection to AVEVA database

        """
        self.conn = None
        self.parameters = dict()

    def update_parameters(self, parameters):
        for key, value in parameters.items():
            self.parameters[key] = value

    def connect(self):
        self.conn = dbconn.ADHClient(api_version=self.parameters["api_version"],
                                     url=self.parameters["url"],
                                     tenant=self.parameters["tenant"],
                                     client_id=self.parameters["client_id"],
                                     client_secret=self.parameters["client_secret"])

    def disconnect(self):
        self.conn = []

    def check_query(self):
        self.conn.Streams.getStreams(self.parameters["namespace_id"],
                                     skip=0,
                                     count=200,
                                     query='HAL_2.Channel2.Device1*')

    def read_data(self, stream_id, start_time, end_time):
        """ function to read data from AVEVA database

        """

        url = '/'.join(
            [
                self.parameters["url"],
                'api', self.parameters["api_version"],
                'Tenants', self.parameters["tenant"],
                'Namespaces', self.parameters["namespace_id"],
                'Streams', ''
            ]
        )

        Nsize = 10000

        start_time_datetime = datetime.fromisoformat(start_time)
        end_time_datetime = datetime.fromisoformat(end_time)

        start_time_unix = int(start_time_datetime.timestamp())
        end_time_unix = int(end_time_datetime.timestamp())

        length_intervals = round(
            (end_time_unix - start_time_unix) / self.parameters["interval"]) + 1

        stream_data_dfs = None
        remaining = length_intervals
        for ii in range(math.ceil(length_intervals / Nsize)):
            start_index_unix = start_time_unix + ii * Nsize * self.parameters["interval"]

            start_index = datetime.utcfromtimestamp(start_index_unix).strftime("%Y-%m-%dT%H:%M:%SZ")
            if remaining > Nsize:
                end_index_unix = start_time_unix + ((ii + 1) * Nsize - 1) * self.parameters[
                    "interval"]
                end_index = datetime.utcfromtimestamp(end_index_unix).strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                end_index_unix = end_time_unix
                end_index = datetime.utcfromtimestamp(end_index_unix).strftime("%Y-%m-%dT%H:%M:%SZ")

            logger.info('Blocksize: ' + start_index + ' to ' + end_index)

            interval = round((end_index_unix - start_index_unix) / self.parameters["interval"]) + 1

            stream_data = self.conn.Streams.getRangeValuesInterpolatedUrl(
                url=url + stream_id,
                start=start_index,
                end=end_index,
                count=interval,
                value_class=None
            )

            stream_data_df = pd.DataFrame(stream_data)
            stream_data_df['Timestamp'] = pd.to_datetime(stream_data_df['Timestamp'], utc=True,
                                                         format='mixed').round('min').dt.strftime(
                '%Y-%m-%dT%H:%M:%SZ')
            stream_data_df = stream_data_df.set_index('Timestamp')

            if stream_data_df.columns.to_list().__contains__('Value'):
                stream_data_df = stream_data_df.loc[:, ['Value']]
                stream_data_df.columns = [stream_id]
                stream_data_df[stream_id] = stream_data_df[stream_id].astype(float)
            else:
                stream_data_df[stream_id] = None

            stream_data_dfs = pd.concat([stream_data_dfs, stream_data_df])

            remaining = remaining - Nsize

        results = stream_data_dfs[stream_id].to_list()
        timestamps = stream_data_dfs.index.values.tolist()

        return results, timestamps

    def get_tagnames(self, tagname_keyword):
        """ function to get tagnames from a keyword"""
        streams = self.conn.Streams.getStreams(self.parameters["namespace_id"],
                                               skip=0,
                                               count=200,
                                               query=tagname_keyword + '*')

        streams_records = [s.toDictionary() for s in streams]

        tagnames = []
        for tag in streams_records:
            tagnames.append(tag['Id'] + ' - ' + tag['Description'])

        return tagnames
