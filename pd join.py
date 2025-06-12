import pandas as pd

"""
	# --- Use them in pipe() ---
	.pipe() always passes the DataFrame as the first argument
	
	Example 1: FULL OUTER JOIN
	
	df_full = df1.pipe(lambda df: full_outer_join(df, df2, on='DATE'))
	or
	df_full = df1.pipe(full_outer_join, df2, on='DATE'))
"""

# --- Define JOIN Functions ---

def full_outer_join(df1, df2, on):
	return pd.merge(df1, df2, how='outer', on=on)

def left_join(df1, df2, on):
	return pd.merge(df1, df2, how='left', on=on)

def right_join(df1, df2, on):
	return pd.merge(df1, df2, how='right', on=on)

if __name__ == '__main__':

	# Sample data
	df1 = pd.DataFrame({
		'DATE': ['2024-01-01', '2024-01-02', '2024-01-04'],
		'A': [10, 20, 30]
	})

	df2 = pd.DataFrame({
		'DATE': ['2024-01-02', '2024-01-03', '2024-01-04'],
		'B': [100, 200, 300]
	})
	
	df_result = (
	df1
	.drop_duplicates()
	.pipe(full_outer_join, df2, on='DATE')
	)

	# --- Show results ---
	print("FULL OUTER JOIN:\n", df_full, "\n")