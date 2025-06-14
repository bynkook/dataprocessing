import pandas as pd
import numpy as np

# -------------------------------------------------
# Settings for filtering values and inferring column types

filter_bad_value = ["", "none", "null", "nan", "-", "*"]
# Fallback date formats (None is used to fall back to pandas’ default parser)
filter_date_formats = ['%Y%m%d%H%M%S', '%Y%m%d', '%Y%m', None]
filter_column_name = {
    'numeric': ['_no', '_amt', '_rat'],
    'date': ['_ym', '_dtc', '_dtm']
}

def type_of_column(col):
    """
    Returns the intended data type of the column (date, numeric, or string)
    based on keywords in its name.
    """
    lname = col.lower()
    for dtype in ['date', 'numeric']:
        if any(k in lname for k in filter_column_name[dtype]):
            return dtype
    return 'string'

# -------------------------------------------------
# Numeric cleaning: if the series is a string, we strip whitespace,
# mask bad values (case-insensitive), and convert to numeric.
def vectorized_clean_value_numeric(series):
    if pd.api.types.is_string_dtype(series):
        cleaned = series.str.strip()
        mask_bad = cleaned.str.lower().isin([v.lower() for v in filter_bad_value])
        cleaned = cleaned.mask(mask_bad)
    else:
        cleaned = series.copy()
    return pd.to_numeric(cleaned, errors='coerce')

# -------------------------------------------------
# Date cleaning using element-wise mapping.
# pandas 는 기본적으로 컬럼에 첫번째 변환 성공한 date format 을 계속 적용한다(속도 향상)

def vectorized_clean_value_date(series):
    def clean_value(x):
        # 1. If x is missing, return pd.NaT
        if pd.isna(x):
            return pd.NaT
        # 2. Ensure the value is a string and strip whitespace.
        s_val = x if isinstance(x, str) else str(x)
        s_val = s_val.strip()
        # 3. If the value is a known "bad" value, return pd.NaT.
        if s_val.lower() in [v.lower() for v in filter_bad_value]:
            return pd.NaT
        # 4. Try using the default pandas parser.
        default_parsed = pd.to_datetime(s_val, errors="coerce")
        if pd.notna(default_parsed):
            return default_parsed.normalize()
        # 5. Apply fallback formats one by one if needed.
        for fmt in filter_date_formats:
                parsed = pd.to_datetime(s_val, format=fmt, errors="coerce")
                if pd.notna(parsed):
                    return parsed.normalize()
        # 6. If all parsing attempts fail, return pd.NaT.
        return pd.NaT

    # Use element-wise mapping using .map(lambda …)
    return series.map(lambda x: clean_value(x))

# -------------------------------------------------
# String cleaning: strip whitespace and mask bad values.
def vectorized_clean_value_string(series):
    if pd.api.types.is_string_dtype(series):
        cleaned = series.str.strip()
        mask_bad = cleaned.str.lower().isin([v.lower() for v in filter_bad_value])
        return cleaned.mask(mask_bad)
    return series

# -------------------------------------------------
# Main processing: create two DataFrames and apply column-type detection,
# then clean the columns based on their intended type.
if __name__ == "__main__":

    df1 = pd.DataFrame({
        'col_NO1': [1, 2, 3, '4-', 5],
        'col_ym1': [202501, '202502', '20250301', '2025-03-02', '*'],
        'col_str1': ['a', '*', 'c', 1, '#8#']
    })

    df2 = pd.DataFrame({
        'col_no2': [1, '2', 3, '4*', 5],
        'col_ym2': [20250101121212, '20250201141414', '2025-03-01 14:14:14', '2025010216', None],
        'col_str2': ['a', '-', 'c', 2, '&&7']
    })

    df_list = [df1, df2]

    for idx, dfi in enumerate(df_list):
        # Map column names to their determined data type.
        col_type_map = {col: type_of_column(col) for col in dfi.columns}
        for col, dtype in col_type_map.items():
            if dtype == 'numeric':
                dfi[col] = vectorized_clean_value_numeric(dfi[col])
            elif dtype == 'date':
                dfi[col] = vectorized_clean_value_date(dfi[col])
            else:
                dfi[col] = vectorized_clean_value_string(dfi[col])

    print(df1)
    print(df2)