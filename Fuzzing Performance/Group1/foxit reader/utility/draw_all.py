import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import math
import os

LIMIT=100
y_limit_low = 160000
y_limit_high = 365000

def read_data(filename):
    f = open(filename, "r")
    line = f.readline().strip()
    x_points = [0]
    y_points = [y_limit_low]
    base_x = int(line.split(',')[0])
    base_y = int(line.split(',')[1])
    line = f.readline().strip()
    read_num = 1
    while read_num < LIMIT:
        read_num += 1
        x_points.append(int(line.split(',')[0]))
        y_points.append(int(line.split(',')[1])-base_y)
        line = f.readline().strip()
    f.close()
    x_max = len(x_points)
    for i in range(x_max):
        x_points[i] = x_points[i] / x_max * 48
    return x_points, y_points

def parse_folder(folder_name):
    x_ordinates = []
    y_ordinates = []
    prefix = os.path.join('../', 'data')
    folder_name = os.path.join(prefix, folder_name)
    for i in os.listdir(folder_name):
        fname = os.path.join(folder_name, i)
        tmp_x, tmp_y = read_data(fname)
        x_ordinates = tmp_x
        y_ordinates.append(tmp_y)
    return x_ordinates, y_ordinates

def combine_array(arrs):
    length = len(arrs[0])
    min = [0xffffffff for i in range(length)]
    max = [0 for i in range(length)]
    sum = [0 for i in range(length)]
    test_len = len(arrs)
    for i in range(length):
        for arr in arrs:
            num = arr[i]
            sum[i] += num
            if num < min[i]:
                min[i] = num
            if num > max[i]:
                max[i] = num
    avg = [sum[i]/test_len for i in range(length)]
    return min, max, avg

def main():
    plt.rcParams['figure.figsize'] = (7.2, 4.05)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    hour_array, document_y_arr = parse_folder('adobe_manual')
    hour_array, random_y_arr = parse_folder('random')
    # hour_array, shallow_y_arr = parse_folder('shallow')
    hour_array, error_message_y_arr = parse_folder('error_message')
    hour_array, path_len_y_arr = parse_folder('path_len')
    # hour_array, typeoracle_adobe_y_arr = parse_folder('typeoracle_adobe')
    hour_array, typeoracle_foxit_y_arr = parse_folder('typeoracle_foxit')
    document_min, document_max, document_avg = combine_array(document_y_arr)
    random_min, random_max, random_avg = combine_array(random_y_arr)
    # shallow_min, shallow_max, shallow_avg = combine_array(shallow_y_arr)
    error_message_min, error_message_max, error_message_avg = combine_array(error_message_y_arr)
    path_len_min, path_len_max, path_len_avg = combine_array(path_len_y_arr)
    # typeoracle_adobe_min, typeoracle_adobe_max, typeoracle_adobe_avg = combine_array(typeoracle_adobe_y_arr)
    typeoracle_foxit_min, typeoracle_foxit_max, typeoracle_foxit_avg = combine_array(typeoracle_foxit_y_arr)
    plt.plot(hour_array, random_avg, alpha = 0.9, color = "#808080", linestyle = "--", label =  "randomly fuzzing")
    # plt.fill_between(hour_array, random_min, random_max, alpha = 0.4, color = "g", linestyle = "-")
    plt.plot(hour_array, document_avg, alpha = 1, color = "#000000", linestyle = "-.", label =  "using Adobe manual")
    # plt.fill_between(hour_array, document_min, document_max, alpha = 0.3, color = "m", linestyle = "-")
    # plt.plot(hour_array, typeoracle_adobe_avg, alpha = 0.9, color = "b", linestyle = "-.", label =  "using TypeOracle on Adobe")
    # plt.fill_between(hour_array, typeoracle_adobe_min, typeoracle_adobe_max, alpha = 0.4, color = "b", linestyle = "-")
    # plt.plot(hour_array, shallow_avg, alpha = 0.9, color = "b", linestyle = "-", label =  "all binding calls + shallow feature")
    # plt.fill_between(hour_array, shallow_min, shallow_max, alpha = 0.4, color = "b", linestyle = "-")
    plt.plot(hour_array, error_message_avg, alpha = 1, color = "#000000", linestyle = "--", label =  "all binding calls + error message")
    # plt.fill_between(hour_array, error_message_min, error_message_max, alpha = 0.4, color = "b", linestyle = "-")
    plt.plot(hour_array, path_len_avg, alpha = 1, color = "#000000", linestyle = ":", label =  "all binding calls + path length")
    # plt.fill_between(hour_array, path_len_min, path_len_max, alpha = 0.4, color = "y", linestyle = "-")
    plt.plot(hour_array, typeoracle_foxit_avg, alpha = 1, color = "#000000", linestyle = "-", label =  "using TypeOracle on Foxit")
    # plt.fill_between(hour_array, typeoracle_foxit_min, typeoracle_foxit_max, alpha = 0.4, color = "r", linestyle = "-")
    # plt.legend(loc="best")
    x_major_locator = MultipleLocator(8)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim(0, 49)
    plt.ylim(y_limit_low, y_limit_high)
    plt.xlabel("Hours (h)")
    plt.ylabel("Coverage (# of instructions)")
    # plt.ylabel("# of insns")
    plt.savefig("foxit_type.pdf", bbox_inches = 'tight')
    typeoracle_incre_random = (typeoracle_foxit_avg[99] - random_avg[99]) / random_avg[99]
    typeoracle_incre_manual = (typeoracle_foxit_avg[99] - document_avg[99]) / document_avg[99]
    print("random avg: {}".format(random_avg[99]))
    print("argument info increment than random: {}".format(typeoracle_incre_random))
    print("argument info increment than manual: {}".format(typeoracle_incre_manual))
    plt.show()

if __name__ == "__main__":
    main()
