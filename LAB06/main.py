from statistic import Statistic

stat = Statistic('table_oxy.csv')

diff_info = stat.diff_info
date_info = stat.get_categories('DATE')

diff_info_chunks = stat.sliding_window(diff_info, 100)
date_info_chunks = stat.sliding_window(date_info, 100)
diff_info_mv_av = stat.moving_average(diff_info_chunks)
lin_reg_slope = stat.calculate_linear_regression_slope(diff_info_chunks, date_info_chunks)
print len(lin_reg_slope)
print len(diff_info_mv_av)

stat.plot_data(date_info, diff_info, 'Difference between OPEN and CLOSE (DATE)',
               'DATE', 'OPEN - CLOSE', '../plots/open_close_diff.png')

# stat.plot_data(lin_reg_slope, diff_info_mv_av, 'Linear regression slope (moving average)', 'Linear regression slope', 'Moving average', '../plots/lin_reg_mv_av.png')

