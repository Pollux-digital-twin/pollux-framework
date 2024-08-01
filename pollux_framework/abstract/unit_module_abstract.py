from abc import ABC
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class UnitModuleAbstract(ABC):
    logger = logger

    def __init__(self, unit):
        self.unit = unit
        self.input_tags = dict()
        self.output_tags = dict()
        self.loop = None

    def link_input(self, category, tagname):
        self.input_tags[tagname] = {'internal_tagname': tagname + '.' + category}

    def link_output(self, category, tagname):
        self.output_tags[tagname] = {'internal_tagname': tagname + '.' + category}

    def get_output_last_data_time(self, tagname):
        database = None
        for database in self.unit.plant.databases:
            if database.category == 'measured':
                break

        time_str = database.get_internal_database_last_time_str(
            self.unit.plant.name,
            self.unit.name,
            self.output_tags[tagname]['internal_tagname'])

        return time_str

    def get_input_data(self, tagname):
        database = None
        for database in self.unit.plant.databases:
            if database.category == 'measured':
                break

        result, time = database.read_internal_database(
            self.unit.plant.name,
            self.unit.name,
            self.input_tags[tagname]['internal_tagname'],
            self.loop.start_time,
            self.loop.end_time,
            str(self.loop.timestep) + 's')

        return time, result

    def write_output_data(self, tagname, time, result):
        database = None
        for database in self.unit.plant.databases:
            if database.category == 'measured':
                break

        database.write_internal_database(
            self.unit.plant.name,
            self.unit.name,
            self.output_tags[tagname]['internal_tagname'],
            time,
            result
        )
