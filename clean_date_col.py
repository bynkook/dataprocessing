import pandas as pd

def clean_date_column(df, col_name, return_invalid=False, drop_time=True, inplace=False):
    """
    Clean and standardize a date/time column in a memory-efficient way.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        col_name (str): Name of the column to parse.
        return_invalid (bool): Return unparseable rows separately.
        drop_time (bool): If True, output date only (no time). If False, keep full timestamp.
        inplace (bool): If True, modify original DataFrame.

    Returns:
        pd.DataFrame: DataFrame with 'PARSED_DATE' column.
        Optional[pd.DataFrame]: Invalid rows if return_invalid=True.
    """
    if not inplace:
        df = df.copy(deep=False)  # 🧠 memory-light copy

    # Ensure string type for parsing
    df[col_name] = df[col_name].astype(str).replace(['nan', '', 'None'], pd.NA)

    # Universal date parsing (multi-format tolerant)
    parsed = pd.to_datetime(df[col_name], errors='coerce', dayfirst=True)

    # 👇 STEP 3: Drop time if requested
    if drop_time:
        df['PARSED_DATE'] = parsed.dt.date  # Python date object (clean, readable)
    else:
        df['PARSED_DATE'] = parsed.dt.normalize()  # datetime64[ns] but time is 00:00:00

    # Optionally return rows with failed parses
    if return_invalid:
        df_invalid = df[df['PARSED_DATE'].isna()]
        return df, df_invalid
    return df