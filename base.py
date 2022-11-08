"""This file created for working with navigation data"""

from datetime import timedelta
from math import sin, cos, atan, sqrt

# For example
# 0GPGGA,060355.00,4950.4828,N,03638.5901,E,1,05,4.3,144.5,M,16.2,M,,*67
# Where next elements

# 0GPGGA     - command about write current message
# 060355.00  - 06 hours 03 minutes 55.00 seconds

# 4950.4828  - latitude: 49 degrees 50.4828 minutes
# N          - Nord
# 03638.5901 - longitude: 036 degrees 38.5901 minutes
# E          - East

# 1    - trash
# 05   - trash
# 4.3  - trash
# 144.5      - height
# M          - meters
# 16.2 - trash
# *67        - control summ message in 0x16 by module 16

from message import MESSAGE


EARTH_RADIUS_IN_KM = 6372.795
EARTH_RADIUS_IN_M = 6372795


class Aircraft:
    """
    Main class aircraft with data on fly
    """

    def __init__(self, message) -> None:
        self._message = message
        self._list_commands: list = []
        self._list_time: list = []
        self._list_latitude: list = []
        self._latitude: str = ""
        self._list_longtitude: list = []
        self._longtitude: str = ""
        self._list_height: list = []

        self.search_data_for_lists()

    def search_data_for_lists(self) -> None:
        """
        Get all elements for data flight
        """
        for element in self._message:
            info = element.split(',')

            self.local_append(self._list_commands, info[0])
            self.local_append(self._list_time, info[1])
            self.local_append(self._list_latitude, info[2])
            self._latitude = info[3]
            self.local_append(self._list_longtitude, info[4])
            self._longtitude = info[5]
            self.local_append(self._list_height, info[9])
        return None


    @staticmethod
    def local_append(local_attr: list, value_to_append) -> None:
        """
        Append value to current list
        """
        local_attr.append(value_to_append)
        return None

    @staticmethod
    def get_list_with_float(list_with_str: list) -> list:
        """
        Get list with float elements from list with str's
        """
        return [float(element) for element in list_with_str]

    def get_max_hight_value(self) -> float:
        """
        Get max value of height fly by list of message heights
        """
        return max(self.get_list_with_float(self._list_height))

    def get_min_hight_value(self) -> float:
        """
        Get min value of height fly by list of message heights
        """
        return min(self.get_list_with_float(self._list_height))

    @staticmethod
    def parser_time(str_with_time: str) -> tuple:
        """
        Get time info from string
        """
        hours = int(str_with_time[:2])
        minutes = int(str_with_time[2:4])
        seconds = float(str_with_time[4:])
        return hours, minutes, seconds
    
    def get_all_time_fly(self):
        """
        Get summ of time in fly
        """
        time_start = self._list_time[0]
        time_finish = self._list_time[-1]

        tuple_start = self.parser_time(time_start)
        tuple_finish = self.parser_time(time_finish)

        start = timedelta(hours=tuple_start[0], minutes=tuple_start[1], seconds=tuple_start[2])
        finish = timedelta(hours=tuple_finish[0], minutes=tuple_finish[1], seconds=tuple_finish[2])

        time_in_fly = finish - start

        return time_in_fly

    def get_sum_flight_distance(self):
        """
        Get current summa all flight distance
        """
        sum_flight_distance = 0

        for distance in self.get_list_distances_per_signal():
            sum_flight_distance += distance

        return sum_flight_distance

    def get_list_distances_per_signal(self):
        """
        Get list with elements, where on one signal -> one distance
        """
        list_of_distances = []

        fo_1_rad = 0
        la_1_rad = 0

        fo_2_rad = 0
        la_2_rad = 0

        for index in range(len(self._list_latitude)):
            if index >= 19:
                break

            fo_1_rad = self.get_radians(self._list_latitude[index])
            la_1_rad = self.get_radians(self._list_longtitude[index][1:])
            
            fo_2_rad = self.get_radians(self._list_latitude[index + 1])
            la_2_rad = self.get_radians(self._list_longtitude[index+ 1][1:])

            list_of_distances.append(self.get_distance_in_meters(fo_1_rad, la_1_rad, fo_2_rad, la_2_rad))
        return list_of_distances


    @staticmethod
    def get_radians(value):
        """
        Get radians value from degrees and minutes
        """
        degrees: float = float(value[:2])
        minutes: float = float(value[2:])
        radians = degrees + (minutes / 60)
        return radians

    @staticmethod
    def get_distance_in_meters(rad_fo_1, rad_la_1, rad_fo_2, rad_la_2):
        """
        Get value of distance by formula
        """
        delta_fo = rad_fo_2 - rad_fo_1
        delta_la = rad_la_2 - rad_la_1

        delta_ce_de = atan(sqrt((cos(rad_fo_2)*sin(delta_la))**2 + (cos(rad_fo_1)*sin(rad_fo_2) - sin(rad_fo_1)*cos(rad_fo_2)*cos(delta_la))**2)/((sin(rad_fo_1)*sin(rad_fo_2) + cos(rad_fo_1)*cos(rad_fo_2)*cos(delta_la))))

        distance = EARTH_RADIUS_IN_KM * delta_ce_de
        return distance * 1000

    def get_middle_speed(self):
        """
        Get flight middle speed by all time in fly
        """
        all_distance = int(self.get_sum_flight_distance())
        time_in_second = int(self.get_all_time_fly().seconds)

        return all_distance / time_in_second

    def get_delta_in_signals(self):
        """
        Get delta in seconds by all distans for seconds
        """
        all_time_in_sec = int(self.get_all_time_fly().seconds)
        count_signals = int(len(self._list_commands))
        return count_signals / all_time_in_sec

    def get_min_max_speed_fly(self):
        """
        Get dict with minimal and maximum speed on fly
        """
        delta_signal_in_second = self.get_delta_in_signals()

        speed_info = {
            "min": 1000.0,
            "max": 0.0,
        }
        for distance in self.get_list_distances_per_signal():
            current_speed = distance / delta_signal_in_second
            if current_speed > speed_info["max"]:
                speed_info["max"] = current_speed
            
            if current_speed < speed_info["min"]:
                speed_info["min"] = current_speed
        
        return speed_info
        

def base():
    """
    Base method for show all data info
    """

    aircraft = Aircraft(message=MESSAGE)

    print(f"Сумарна довжина маршруту польоту: {round(aircraft.get_sum_flight_distance(), 2)} метрів.")

    print(f"Середня швидкість польоту: {round(aircraft.get_middle_speed() * 3.6, 2)} км/год.")

    print(f"Мінімальна швидкість польоту: {round(aircraft.get_min_max_speed_fly()['min'] * 3.6, 2)} км/год.")

    print(f"Максимальна швидкість польоту: {round(aircraft.get_min_max_speed_fly()['max'] * 3.6 , 2)} км/год.")

    print(f"Мінімальна висота польоту: {round(aircraft.get_min_hight_value(), 2)} метрів.")

    print(f"Максимальна висота польоту: {round(aircraft.get_max_hight_value(), 2)} метрів.")
    
    print(f"Загальний час усього польоту: {aircraft.get_all_time_fly()}.")
    

if __name__ == "__main__":
    base()
