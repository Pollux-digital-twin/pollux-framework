from abc import ABC


class UnitAbstract(ABC):
    """Abstract class for Unit."""

    def __init__(self, unit_id, unit_name, plant):
        """Basic constructor for unit objects.

        :param str unit_id: The unique identifier of the unit.
        :param str unit_name: The name of the unit.
        :param str plant: The plant.
        """

        self.id = unit_id
        self.name = unit_name
        self.plant = plant
        self.parameters = dict()
        self.tagnames = {'measured': {}, 'calculated': {}}
        self.modules = {'preprocessor': [], 'model': [], 'postprocessor': []}
        self.from_units = []
        self.to_units = []

    def update_parameters(self, param):
        """function to update unit parameters.

        :param dict param: parameters that need to be updated.
        """
        for key, value in param.items():
            self.parameters[key] = value

    def update_tagnames(self, category, param):
        """function to update unit parameters.

        :param str category: tagnames category (measured, filtered, calculated).
        :param dict param: tagnames that need to be updated.
        """
        for key, value in param.items():
            self.tagnames[category][key] = value
