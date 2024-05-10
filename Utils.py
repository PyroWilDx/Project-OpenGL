from time import time


class Utils:
    last_time = time()
    dt = 0

    @staticmethod
    def update_dt():
        curr_time = time()
        Utils.dt = curr_time - Utils.last_time
        Utils.last_time = curr_time
