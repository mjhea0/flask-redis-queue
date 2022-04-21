import dataclasses
from typing import List

import pandas as pd
from pydantic.dataclasses import dataclass


@dataclasses.dataclass
class DataFrames:
    dataframe: pd.DataFrame = None


@dataclass
class OutputObject:
    delay: int = None
    time: float = (None,)
    texts: List[str] = (None,)
    file_names: List[str] = (None,)
    byte_data_lengths: List[int] = (None,)
    webhook_endpoint: str = None
    tic: float = None
