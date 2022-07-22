import matplotlib.pyplot as plt

class DynamicPloter:
    def __init__(self, color='r'):
        self._t = []
        self._t_now = 0
        self._y_list = []
        self.color = color

    def init(self):
        plt.ion()
        plt.figure(1)

    def plot(self, new_data):
        self._t_now += 0.1
        self._t.append(self._t_now)
        self._y_list.append(new_data)
        plt.plot(self._t, self._y_list, '-' + self.color)
        plt.draw()