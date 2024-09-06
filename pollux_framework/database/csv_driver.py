from pollux_framework.abstract.databasedriver_abstract import DatabaseDriverAbstract


class CsvDriver(DatabaseDriverAbstract):
    """ Timeseries database based on Influxdb"""

    def __init__(self):
        super().__init__()

    def connect(self):
        return

    def disconnect(self):
        return

    def read_data(self, tagname, start_time, end_time):
        return

    def write_data(self):
        return
