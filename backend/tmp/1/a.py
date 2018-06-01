from statistics import mean, median, mode, median_low, median_high, median_grouped, pstdev, pvariance

lst = [22, 33, 21, 28, 22, 31, 44, 50, 19]


def print_stats(lst):
    print('List: ', lst)
    lst = sorted(lst)
    print('Sorted list: ', lst)
    print('Mean: ',   mean(lst))
    print('Mode: ',   mode(lst))
    print('Median: ', median(lst))
    print('Median low: ',     median_low(lst))
    print('Median high: ',    median_high(lst))
    print('Median grouped: ', median_grouped(lst))
    print('Range: ', max(lst)- min(lst))
    print('Standart deviation: ', pstdev(lst))
    print('Variance: ', pvariance(lst))



print_stats(lst)
print_stats([i - 2 for i in lst])