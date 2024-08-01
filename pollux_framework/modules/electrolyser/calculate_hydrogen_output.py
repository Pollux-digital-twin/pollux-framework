from pollux_framework.abstract.unit_module_abstract import UnitModuleAbstract
from pollux_model.electrolyser.pem_electrolyser import PEMElectrolyser
import numpy as np

class CalculateHydrogenOutput(UnitModuleAbstract):
    def __init__(self, unit):
        super().__init__(unit)

        self.model = PEMElectrolyser()

        self.link_input('measured', 'temperature')
        self.link_input('measured', 'pressure')
        self.link_input('measured', 'power')
        self.link_output('calculated', 'hydrogen_flow')
        self.link_output('calculated', 'oxygen_output')

    def step(self, loop):
        self.loop = loop
        self.loop.start_time = self.get_output_last_data_time('hydrogen_flow')
        self.loop.compute_n_simulation()

        parameters = dict()

        self.model.update_parameters(parameters)

        time, temperature = self.get_input_data('temperature')
        time, pressure = self.get_input_data('pressure')
        time, power = self.get_input_data('power')

        u = dict()

        for ii in range(1, self.loop.n_step):
            try:
                u['temperature'] = 1
                u['pressure'] = 2
                u['power'] = 3

                x = []
                self.model.calculate_output(u, x)

                y = self.model.get_output()

                esp_pump_head.append(y['pump_head'] / 1e5)  # convert to bar
            except Exception as e:
                self.logger.warn("ERROR:" + repr(e))
                esp_pump_head.append(None)

        if esp_pump_head:
            self.write_output_data('esp_pump_head', time, esp_pump_head)