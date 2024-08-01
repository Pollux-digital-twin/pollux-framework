import math
import datetime


class Loop:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.timestep = None
        self.n_step = None

    def initialize(self, end_time, timestep):

        self.end_time = end_time
        self.timestep = timestep

    def compute_n_simulation(self):
        starttime_datetime = datetime.datetime.fromisoformat(self.start_time)
        endtime_datetime = datetime.datetime.fromisoformat(self.end_time)

        self.n_step = math.ceil(
            (endtime_datetime - starttime_datetime).total_seconds() / self.timestep)
