from pollux_framework.abstract.unit_abstract import UnitAbstract
from pollux_framework.modules.electrolyser.calculate_hydrogen_output \
    import CalculateHydrogenOutput


class ESPUnit(UnitAbstract):
    """A ESPUnit represents ESP modules."""

    def __init__(self, unit_id, unit_name, plant):
        super().__init__(unit_id=unit_id, unit_name=unit_name, plant=plant)

        # define unit modules
        self.modules['preprocessor'] = []
        self.modules['model'].append(CalculateHydrogenOutput(self))
        self.modules['postprocessor'] = []