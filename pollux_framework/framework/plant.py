class Plant:
    """A Plant is a class that consists of several assets."""

    def __init__(self):
        self.project_path = None
        self.name = None
        self.parameters = dict()
        self.units = []
        self.databases = []
        self.diagram = None

    def update_parameters(self, parameters):
        for key, value in parameters.items():
            self.parameters[key] = value

    def add_unit(self, unit):
        """function to add asset instance to the plant."""
        self.units.append(unit)

    def remove_unit(self, unit_id):
        """function to remove asset instance based on unit id.

        :param str unit_id: the unique identifier of an asset.
        """
        for ii in range(0, len(self.units)):
            if self.units[ii].id == unit_id:
                del self.units[ii]

    def get_unit(self, unit_id):
        """function to get asset instance based on unit id.

        :param str unit_id: the unique identifier of an asset.
        """
        unit = None
        for ii in range(0, len(self.units)):
            if self.units[ii].id == unit_id:
                unit = self.units[ii]
                break
        return unit

    def connect_unit(self):
        for cell in self.diagram['cells']:
            if cell['type'] == 'devs.Link':
                source_unit = self.get_unit(cell['source']['id'])
                target_unit = self.get_unit(cell['target']['id'])
                if not (source_unit is None) and not (target_unit is None):
                    source_unit.to_units.append(target_unit)
                    target_unit.from_units.append(source_unit)

    def add_database(self, database):
        self.databases.append(database)

    def connect_database(self):
        for database in self.databases:
            database.connect()

    def find_modules(self, category):
        modules = []
        for unit in self.units:
            modules += unit.modules[category]

        return modules
