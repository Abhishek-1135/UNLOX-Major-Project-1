import pandas as pd
from scipy import stats

def compare_groups(df, column, metric="engagement_rate"):
    groups = [g[metric].dropna().values for _, g in df.groupby(column)]
    labels = list(df[column].unique())
    if len(groups) < 2:
        return None
    t_stat, p_value = stats.ttest_ind(groups[0], groups[1], equal_var=False)
    return {
        "variable": column,
        "group_1": labels[0],
        "group_2": labels[1],
        "mean_1": groups[0].mean(),
        "mean_2": groups[1].mean(),
        "t_stat": t_stat,
        "p_value": p_value,
        "significant_at_0_05": p_value < 0.05
    }
