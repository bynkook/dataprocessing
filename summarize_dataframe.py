def summarize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    summary = []
    total_rows = len(df)
    total_columns = len(df.columns)

    for col in df.columns:
        col_data = df[col]
        data_type = col_data.dtype
        non_null_count = col_data.notna().sum()
        null_count = col_data.isna().sum()
        percent_null = (null_count / total_rows) * 100 if total_rows > 0 else np.nan
        unique_count = col_data.nunique(dropna=True)

        # Default values
        min_val = max_val = sample_value = np.nan

        if pd.api.types.is_numeric_dtype(col_data) or pd.api.types.is_datetime64_any_dtype(col_data):
            min_val = col_data.min(skipna=True)
            max_val = col_data.max(skipna=True)

        # Grab a sample non-null value for general types
        non_nulls = col_data.dropna()
        if not non_nulls.empty:
            sample_value = non_nulls.iloc[0]

        summary.append({
            "Column": col,
            "Data Type": str(data_type),
            "Non-Null Count": non_null_count,
            "Null Count": null_count,
            "% Null": round(percent_null, 2),
            "Unique Count": unique_count,
            "Min": min_val,
            "Max": max_val,
            "Sample Value": sample_value,
        })

    summary_df = pd.DataFrame(summary)
    summary_df.index.name = "Column Index"

    # Add meta info at the top
    summary_df.attrs["Total Columns"] = total_columns
    summary_df.attrs["Total Rows"] = total_rows

    return summary_df