import numpy as np
import pandas as pd
from tabulate import tabulate


def process_data(data):
    """ Change labels, group by planner and format for latex."""
    data = data.replace(
        {
            "grid_run_1": "Grid",
            "prm_run_1": "PRM A",
            "prm_run_2": "PRM B",
            "prm_run_3": "PRM C",
        }
    )

    data = data.rename(
        columns={"num_samples": "samples", "cc_checks": "collision checks"}
    )

    df = data.groupby(["run"]).sum()[["samples", "jvm", "time", "collision checks"]]
    df["samples"] = np.round(df["samples"])
    df["time"] = np.round(df["time"])
    df["samples"] = np.round(df["collision checks"])

    sr = data.groupby(["run"]).sum()[["success"]]
    df["solved"] = sr.astype(int).astype(str) + "/14"

    latex = df.to_latex(
        formatters={
            "samples": "{:,.0f}".format,
            "jvm": "{:.2f}".format,
            "collision checks": "{:,.0f}".format,
            "time": "{:.0f}".format,
        }
    )

    return df, latex


filenames = ["data/case1.csv", "data/case2.csv", "data/case3.csv"]

res = [process_data(pd.read_csv(name)) for name in filenames]
data_frames, latex_strings = list(zip(*res))  # fancy python list unzipping

with open("README.md", "w") as md_file:
    for i, data_frame in enumerate(data_frames):
        md_file.write("## Case {}\n".format(i))
        md_file.write(tabulate(data_frame, headers="keys", tablefmt="github"))
        md_file.write("\n\n")

with open("tables.tex", "w") as latex_file:
    for i, latex_str in enumerate(latex_strings):
        latex_file.write("Case {}\n".format(i))
        latex_file.write(latex_str)
        latex_file.write("\n\n")

