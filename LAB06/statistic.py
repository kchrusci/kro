import csv
import math
import numpy as np
from scipy import stats
import pylab


class Statistic:
    def __init__(self, path):
        self.data_path = path
        self.tagged_data = []
        self.open_info = []
        self.close_info = []
        self.diff_info = []

        with open(self.data_path, 'r') as csv_file:
            self.csv_file = csv.reader(csv_file, delimiter=',')
            for row in self.csv_file:
                self.tagged_data.append(self.tag_data(row))
                self.diff_info.append(self.load_data(row))

    @staticmethod
    def tag_data(raw_data):
        tagged_data = dict()
        tagged_data["DATE"] = raw_data[0]
        tagged_data["TIME"] = raw_data[1]
        tagged_data["OPEN"] = raw_data[2]
        tagged_data["HIGH"] = raw_data[3]
        tagged_data["LOW"] = raw_data[4]
        tagged_data["CLOSE"] = raw_data[5]
        tagged_data["EARNINGS"] = raw_data[6]
        return tagged_data

    @staticmethod
    def load_data(raw_data):
        open_info = raw_data[2]
        close_info = raw_data[5]
        diff_info = float(open_info) - float(close_info)
        return diff_info

    def get_categories(self, category):
        category_list = []
        for row in self.tagged_data:
            category_list.append(row[category])

        category_list = map(float, category_list)
        return category_list

    @staticmethod
    def sliding_window(input_data, window_size):
        number_of_windows = math.ceil(float(len(input_data)) / float(window_size))
        aggregated_data = []
        for window_num in range(int(number_of_windows)):
            window = input_data[window_num*window_size:window_num*window_size+window_size]
            aggregated_data.append(window)

        return aggregated_data

    @staticmethod
    def moving_average(data_chunks):
        mv_av = []
        for chunk in data_chunks:
            window_size = len(chunk)
            result = np.convolve(chunk, np.ones(window_size,) / window_size, mode='valid')
            mv_av.append(result[0])

        return mv_av

    @staticmethod
    def linear_regression_slope(x, y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        return slope

    def calculate_linear_regression_slope(self, x, y):
        x.pop(-1)
        y.pop(-1)
        lin_reg_slope = []
        for i in x:
            for a in y:
                result = self.linear_regression_slope(i, a)
                lin_reg_slope.append(result)

        return lin_reg_slope

    @staticmethod
    def plot_data(x_data, y_data, title, x_label, y_label, file_path):

        f1 = pylab.figure(1)
        s1 = f1.add_subplot(1, 1, 1)
        s1.plot(x_data, y_data, "g-o", linewidth=2)
        s1.set_title(title)
        s1.set_xlabel(x_label)
        s1.set_ylabel(y_label)
        handles, labels = s1.get_legend_handles_labels()
        s1.legend(handles, labels, loc='lower left', fontsize='11', bbox_to_anchor=(0.60, 0.02))
        s1.grid(True)
        pylab.savefig(file_path)
