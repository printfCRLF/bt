def create_moving_averages(df, column_name, ma_func, periods):
    df1 = df.copy()
    for period in periods:
        df1[f"SMA{period}"] = ma_func(df1[column_name], timeperiod=period)

    return df1

