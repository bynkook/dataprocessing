import pandas as pd
import numpy as np

"""
Last updated: 2025-06-13 22:00:00
1. when column name match any of filter_number_column, all data in the column will be converted to numeric, if not convertable, will be np.nan.
2. when column name match any of filter_date_column, all data in the column will be converted to pandas date format, if not convertable, will be pd.NaT.  
3. when column name name match any of filter_bad_, all data in the column will be converted to NaN.
4. when column name not have any match, all data in the column will remain as original data.
5. any filter application it shall be case-insensitive.
"""

# user-defined filters
filter_bad_value = ["", "none", "null", "nan", "-", "*"]
column_name_map = {
    'numeric': ['_no', '_amt', '_rat'],
    'date': ['_ym', '_dtc', '_dtm'],
}

def clean_value(val, date_format=False):
    """
    Clean value to numeric or datetime format, handling known invalid entries.
    Dates are normalized to YYYY-MM-DD.
    """
    if pd.isna(val):
        return pd.NaT if date_format else np.nan
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in [v.lower() for v in filter_bad_value]:
            return pd.NaT if date_format else np.nan
    if date_format:
        date_formats = ['%Y%m%d%H%M%S', '%Y%m%d', '%Y%m', None]     # None for fallback
        for fmt in date_formats:
            try:
                dt = pd.to_datetime(val, format=fmt, errors='coerce')
                if not pd.isna(dt):
                    return dt.normalize()  # keep as datetime64[ns], remove time
            except Exception:
                continue
        return pd.NaT   # Return NaT if conversion fails
    try:
        return pd.to_numeric(val, errors='coerce')
    except Exception:
        return val

def type_of_column(col):
    lname = col.lower()
    for dtype in ['date', 'numeric']:
        if any(k in lname for k in column_name_map[dtype]):
            return dtype
    return 'string'

if __name__ == "__main__":
    
    df1 = pd.DataFrame({
        'col_NO1': [1, 2, 3,'4-'],
        'col_ym1': ['202501', '20250301','2025-03-02', np.nan],
        'col_str1': ['a', '*', 'c', 1]
    })
    df2 = pd.DataFrame({
        'col_no2': [1, '2', 3,'4*'],
        'col_ym2': ['20250101141414', '2025-03-01 14:14:14', '2025010216', None],
        'col_str2': ['a', '-', 'c', 2]
    })
    df_list = [df1, df2]
    for idx, dfi in enumerate(df_list):
        col_type_map = {col: type_of_column(col) for col in dfi.columns}
        if len(set(dfi.columns)) != len(set(col_type_map)):
            print(f"WARNING: Column classification issue in df{idx}")
        for col, dtype in col_type_map.items():
            if dtype == 'numeric':
                dfi[col] = dfi[col].apply(clean_value)
            elif dtype == 'date':
                dfi[col] = dfi[col].apply(lambda x: clean_value(x, date_format=True))
            else:
                dfi[col] = dfi[col].replace(filter_bad_value, np.nan)
    print(df1)
    print(df2)