import pandas as pd
import numpy as np

# user defined variables
numeric_column_filter = ['_no', '_amt', '_rat']
numeric_column_name_filter = []		# name of column you want to specifically add to filter
numeric_column_filter += numeric_column_name_filter
date_column_filter = ['_ym', '_dtc','_dtm']
find_bad_val = ["", "none", "null", "nan", "-", "*"]

df1 = pd.DataFrame({'col_NO1':[1,2,3], 'col_ym1':['202501',nan,'202503'], 'col_str1':['a','*','c']})
df2 = pd.DataFrame({'col_no2':[1,'2',3], 'col_ym2':['20250101141414','None','2025-03-01 14:14:14'], 'col_str2':['a','-','c']})
df_list = [df1, df2]

def check_bad_value(val):

	if isinstance(val, str):
		original_val = val.strip()
		val_lower = original_val.lower()
		if val_lower in find_bad_val:
			return np.nan
	return val
			
def clean_date(val, drop_time=True):
	
	try:
		_val = pd.to_datetime(val, errors='coerce')
		if drop_time:
			return _val.dt.date
		return _val
	except (ValueError, TypeError):
		return val

def clean_value(val, date_format=False, drop_time=True):

	if pd.isna(val):
		return np.nan
	_val = check_bad_value(val)
	if date_format:
		return clean_date(_val, drop_time)
	try:
		return pd.to_numeric(_val, errors='coerce')
	except (ValueError, TypeError):
		return val

def clean_value(val):
	if pd.isna(val):
		return np.nan
	if isinstance(val, str):
		original_val = val.strip()
		val_lower = original_val.lower()
		if val_lower in find_bad_val:
			return np.nan
		try:
			return pd.to_numeric(original_val, errors='coerce')
		except (ValueError, TypeError):
			return original_val    
	return val

# 수정-----
for idx, dfi in enumerate(df_list):
	#print(f"--- for table:{idx}")
	#숫자와 날짜형 컬럼 외에는 모두 문자형 컬럼으로 간주한다.
	num_col  = [elem for elem in dfi.columns if any(n in elem.lower() for n in set(numeric_column_filter))]
	date_col = [elem for elem in dfi.columns if any(n in elem.lower() for n in set(date_column_filter))]
	str_col  = [elem for elem in dfi.columns if not any(n in elem.lower() for n in set(numeric_column_filter+date_column_filter))]
	# 컬럼명 필터링의 결과가 다른 필터와 중복될 경우 문제가 발생하게된다.
	# 즉, 이런 필터링 방법은 새로운 컬럼명을 가진 테이블을 만났을때 문제가 발생할 가능성이 있다.
	if len(num_col+date_col+str_col) != len(df1.columns):
		print('WARNING : Check your column filter')	

	for col in dfi.columns:
		if col.lower() in num_col:
			# 숫자는 숫자형으로 변경(숫자가 아니면 null)
			dfi[col] = dfi[col].apply(clean_value)
		elif col.lower() in date_col:
			# date format 컬럼의 변환
			dfi[col] = dfi[col].apply(clean_value, date_format=True)
		else:
			# 그 외 컬럼은 *, - 를 null로 변경. 0은 변경없음(as number|string)
			dfi.replace(to_replace={col:find_bad_val}, value=np.nan, inplace=True)

print(df1)
print(df2)