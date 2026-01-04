import pandas as pd
from constants import CSV_FILE_PATH


def load_csv(component):
    df = pd.read_csv(
        f"./{CSV_FILE_PATH}/{component}.csv",
        header=None,
        names=["component", "log", "level"]
    )
    return df
