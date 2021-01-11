import time
from func.Singleton import SingletonMeta
from func.threading import threaded
from logic.CapacityController import get_current_occupation

class Ventilation(metaclass=SingletonMeta):
    main_thread = None
    elevator = None

    def __init__(self, elevator):
        self.main_thread = thread_main()
        self.elevator = elevator

    @property
    def status(self):
        if self.main_thread:
            return self.main_thread.is_alive()
        return False

    @threaded
    def thread_main(self):
        while True:
            sleep(5)
            isInactive = (time.time() - self.elevator.last_ride_time) > 10
            isUnocuppied = (get_current_occupation() - 1) <= 0
            print(f"VENTIL: Ventilating {isInactive}, {isUnoccupied}")
            if not self.elevator.riding and isInactive and isUnoccupied:
                print("VENTIL: Ventilating")