"""This file created for working with navigation data"""

from datetime import timedelta

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


class Aircraft:

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
    def local_append(local_attr: list, value_to_append: str) -> None:
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


aircraft = Aircraft(message=MESSAGE)

# print(aircraft.get_max_hight_value())
# print(aircraft.get_min_hight_value())
aircraft.get_all_time_fly()
