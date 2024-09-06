from pollux_framework.abstract.unit_abstract import UnitAbstract


class ElectrolyzerUnit(UnitAbstract):
    """A ElectrolyzerUnit represents Electrolyzer modules."""

    def __init__(self, unit_id, unit_name, plant):
        super().__init__(unit_id=unit_id, unit_name=unit_name, plant=plant)

        # define unit modules
        self.modules['preprocessor'] = []
        self.modules['model'] = []
        self.modules['postprocessor'] = []
