"""
This mod contains main func about show plot graphics
"""

import numpy as np
import matplotlib.pyplot as plt

from base import Aircraft
from message import MESSAGE


class Plot:
    """
    This class contain main info for show plots
    """

    def __init__(self) -> None:
        self._aircraft = Aircraft(MESSAGE)
        self._list_times = [second for second in range(int(self._aircraft.get_all_time_fly().seconds))]
        self._list_distances_per_signal = self.get_next_distance()
        self._list_speed_fly = [round(speed * 3.6, 2) for speed in self.get_list_fly_speed()]
        self._list_height_fly = [float(value) for value in self._aircraft._list_height[1:]] 

    
    def get_next_distance(self):
        """
        Get list with next distances per signal
        """
        list_distances = [round(distance, 2) for distance in self._aircraft.get_list_distances_per_signal()]
        list_distances_per_signal = []

        for index in range(len(list_distances)):
            if index == 0:
                list_distances_per_signal.append(round(list_distances[index], 2))
                continue

            list_distances_per_signal.append(round(list_distances[index]+list_distances_per_signal[index-1], 2))
        return list_distances_per_signal

    def get_list_fly_speed(self):
        list_fly_speed = []

        value_second_in_signal = int(self._aircraft.get_delta_in_signals())
        list_distances_per_second = self._aircraft.get_list_distances_per_signal()

        for distance in list_distances_per_second:
            list_fly_speed.append(round(distance/value_second_in_signal, 2))

        return list_fly_speed
            

class Show:
    """
    In this class we can select graphics for show
    """
    def __init__(self) -> None:
        self._plot = Plot()
        self._x_time_list = np.array(self._plot._list_times)
        self._y_speed_list = np.array(self._plot._list_speed_fly)
        self._y_height_list = np.array(self._plot._list_height_fly)
        self._y_distance_list = np.array(self._plot._list_distances_per_signal)

    def show_speed_to_time(self) -> None:
        """
        Show plot about speed to time
        """
        figure = plt.figure()
        plt.plot(self._x_time_list, self._y_speed_list, marker='*', markerfacecolor='w')
        plt.xlabel('Час')
        plt.ylabel('Швидкість польоту')
        plt.suptitle('Speed flight by time')
        plt.show()
        figure.savefig('speed_by_time.jpg')
        return None

    def show_height_to_time(self) -> None:
        """
        Show plot about height to time
        """
        figure = plt.figure()
        plt.plot(self._x_time_list, self._y_height_list, marker='*', markerfacecolor='w')
        plt.xlabel('Час')
        plt.ylabel('Висота польоту')
        plt.suptitle('Height flight by time')
        plt.show()
        figure.savefig('height_by_time.jpg')
        return None

    def show_distance_to_time(self) -> None:
        """
        Show plot about distance to time
        """
        figure = plt.figure()
        plt.plot(self._x_time_list, self._y_distance_list, marker='*', markerfacecolor='w')
        plt.xlabel('Час')
        plt.ylabel('Відстань, яку пройшов літак')
        plt.suptitle('Distance flight by time')
        plt.show()
        figure.savefig('distance_by_time.jpg')
        return None


def base():
    show = Show()

    show.show_speed_to_time()     # show plot about speed to time
    show.show_height_to_time()    # show plot about height to time
    show.show_distance_to_time()  # show plot about distance to time


def get_lists_with_data():
    plot = Plot()
    print(f"List times - {plot._list_times}")
    print(f"List distances - {plot._list_distances_per_signal}")
    print(f"List speed fly - {plot._list_speed_fly}")
    print(f"List height fly - {plot._list_height_fly}")


if __name__ == "__main__":
    base()
    get_lists_with_data()
