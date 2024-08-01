from gemini_framework.framework.loop import Loop


class MainModule:
    plant = None
    modules = dict()
    loop = dict()

    def __init__(self, plant):
        self.plant = plant

        self.modules['preprocessor'] = plant.find_modules('preprocessor')
        self.modules['model'] = plant.find_modules('model')
        self.modules['postprocessor'] = plant.find_modules('postprocessor')

        self.loop['filtered'] = Loop()
        end_time = self.plant.databases[0].get_current_time_str()
        timestep = self.plant.parameters['database']['filtered']['interval']
        self.loop['filtered'].initialize(end_time, timestep)

        self.loop['calculated'] = Loop()
        end_time = self.plant.databases[0].get_current_time_str()
        timestep = self.plant.parameters['database']['calculated']['interval']
        self.loop['calculated'].initialize(end_time, timestep)

    def step(self):
        for database in self.plant.databases:
            # database.delete(self.plant.name)
            database.import_raw_data()

        for module in self.modules['preprocessor']:
            module.logger.info("Timestamps: " + self.loop['filtered'].end_time +
                               ". Running preprocessor module: " + module.__class__.__name__)
            module.step(self.loop['filtered'])

        for module in self.modules['model']:
            module.logger.info("Timestamps: " + self.loop['calculated'].end_time +
                               ". Running calculation module: " + module.__class__.__name__)
            module.step(self.loop['calculated'])

        for module in self.modules['postprocessor']:
            module.logger.info("Timestamps: " + self.loop['calculated'].end_time +
                               ". Running postprocessor module: " + module.__class__.__name__)
            module.step(self.loop['calculated'])
