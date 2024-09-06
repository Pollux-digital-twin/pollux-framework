import os
from pathlib import Path
from pollux_framework.framework.boot_plant import setup
from pollux_framework.framework.mainmodule import MainModule

pollux_root_dir = Path(__file__).parents[2]


class App:
    def __init__(self, project_path, plant_name):
        self.project_path = project_path
        self.plant_name = plant_name

    def boot(self):
        self.plant = setup(self.project_path, self.plant_name)

        self.mainmodule = MainModule(self.plant)

    def step(self):
        self.mainmodule.step()


if __name__ == "__main__":

    projectpath = os.getenv('POLLUX_PROJECT_FOLDER',
                            os.path.join(pollux_root_dir, 'pollux-project'))
    plantname = os.getenv('POLLUX_PLANT', '')

    if not plantname == '':
        app = App(projectpath, plantname)
        app.boot()
        app.step()
