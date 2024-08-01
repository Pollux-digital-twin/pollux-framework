import logging
import os
import json

from pollux_framework.framework.plant import Plant
from pollux_framework.database.influxdb_aveva_reader_db import InfluxdbAvevaReaderDB
from pollux_framework.modules.electrolyser.unit import Electrolyser
# from pollux_framework.modules.esp.unit import ESPUnit
# from pollux_framework.modules.productionwell.unit import ProductionWellUnit
# from pollux_framework.modules.injectionwell.unit import InjectionWellUnit
# from pollux_framework.modules.injectionpump.unit import InjectionPumpUnit
# from pollux_framework.modules.degasser.unit import DegasserUnit
# from pollux_framework.modules.filter.unit import FilterUnit
# from pollux_framework.modules.heatexchanger.unit import HeatExchangerUnit
# from pollux_framework.modules.reservoir.unit import ReservoirUnit
# from pollux_framework.modules.boosterpump.unit import BoosterPumpUnit
# from pollux_framework.modules.gasboiler.unit import GasBoilerUnit

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def setup(project_path, plant_name):
    """function to setup the plant.

    :param str project_path: location of the project folder.
    :param str plant_name: the plant name or location name.
    """
    logger.info('Boot application ' + plant_name)

    plant = Plant()
    plant.project_path = project_path
    plant.name = plant_name

    project_folder = os.path.join(plant.project_path, plant.name)
    with open(os.path.join(project_folder, 'plant.conf'), 'r') as jsonfile:
        cfg = json.load(jsonfile)
        plant.update_parameters(cfg)

    with open(os.path.join(project_folder, 'diagram.json'), 'r') as jsonfile:
        plant.diagram = json.load(jsonfile)

    plant = boot_unit(plant)
    plant = boot_database(plant)

    return plant


def boot_unit(plant):
    """function to boot unit in the plant."""
    logger.info('Boot Unit Plant')

    project_folder = os.path.join(plant.project_path, plant.name)
    for file in os.listdir(project_folder):
        if file.endswith('.param'):
            with open(os.path.join(project_folder, file), 'r') as jsonfile:
                unitfile = json.load(jsonfile)
                unit = []
                if unitfile['parameters']['type'] == 'electrolyser':
                    unit = Electrolyser(unitfile['id'], unitfile['name'], plant)
                else:
                    logger.error(
                        'UNIT ' + unitfile['parameters']['type'] + ' not yet implemented')

                unit.update_parameters(unitfile['parameters'])
                unit.update_tagnames('measured', unitfile['tagnames']['measured'])
                unit.update_tagnames('calculated', unitfile['tagnames']['calculated'])

                plant.add_unit(unit)

    plant.connect_unit()

    return plant


def boot_database(plant):
    """function to starting up the boot_database."""
    logger.info('Boot Database')
    # add measured database
    meas_database = InfluxdbAvevaReaderDB('measured')
    plant.add_database(meas_database)
    for database in plant.databases:
        database.register_tags(plant.units)
        database.update_parameters(plant.parameters['database'])

    for database in plant.databases:
        database.connect()

    return plant
