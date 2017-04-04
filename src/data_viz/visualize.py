

def create_day_tuples(tes_list):
	#find integer of first day and last day
	#partition into bins
	#if TextEquivalent is between the bins add to count
	#similar approach can be used for response time trending
	#checkout numpy and cumsum()
	"""
	http://stackoverflow.com/questions/3034162/plotting-a-cumulative-graph-of-python-datetimes
	http://stackoverflow.com/questions/37293014/draw-a-cumulative-chart-from-a-pandas-dataframe
	https://docs.scipy.org/doc/numpy/reference/generated/numpy.cumsum.html
	"""
	daily_text_eqs = {}
	for te in tes_list:
		k =  str(te.date_month) +'-'+ str(te.date_day) +'-'+ str(te.date_year)
		if(k in daily_text_eqs.keys()):
			daily_text_eqs[k].append(te)
		else:
			daily_text_eqs[k] = [te]

