def mapFromTo(x_input, in_range_start, in_range_start_end, out_range_start, out_range_end):
   y=(x_input - in_range_start) / (in_range_start_end-in_range_start) * (out_range_end-out_range_start) + out_range_start
   return y