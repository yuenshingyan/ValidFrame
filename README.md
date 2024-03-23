# ValidFrame

ValidFrame is a Python library designed to efficiently parse and validate all columns in a pandas DataFrame. It leverages the vectorized operations of pandas to significantly speed up the validation process, making it a powerful tool for data validation in data science and machine learning projects.

## Features

- **Vectorized Validation**: Utilizes pandas' vectorized operations for fast and efficient data validation.
- **Similar Syntax to Pydantic**: Offers a familiar API for those who have used Pydantic, making it easy to adopt.
- **Custom Validators**: Allows for the definition of custom validation rules to meet specific data requirements.

## Installation

To install ValidFrame, use pip:

    pip install validframe


## Usage

First, define a schema for your DataFrame using ValidFrame's syntax, which is similar to Pydantic's:
    
    import pandas as pd
    import numpy as np
    from models import Model
    import time
    import matplotlib.pyplot as plt
    from src.vframe.basemodel import BaseModel
    from src.vframe.column_types import (
        Integer,
        Float,
        Boolean,
        Datetime,
        String,
        List,
        Tuple,
        Dictionary,
        Set,
        Object
    )
    
    
    class Model(BaseModel):
        integer = Integer(lower=-1, upper=6, nullable=True)
        float = Float(lower=-1.0, upper=6.0, nullable=True)
        bool = Boolean(nullable=True)
        datetime = Datetime(lower="2024-03-20", upper="2024-03-21", nullable=True)
        list = List(nullable=True, min_items=1, max_items=3)
        tuple = Tuple(nullable=True, min_items=1, max_items=3)
        dictionary = Dictionary(nullable=True, min_items=1, max_items=3)
        set = Set(nullable=True, min_items=1, max_items=3)
        string = String(min_length=0, max_length=5, nullable=True)
        object = Object(nullable=True)
    
    
    if __name__ == "__main__":
        df = pd.DataFrame(
            {
                'integer': [1, "2", 3, 4, np.nan],
                'float': [1.0, "2.0", 3, "4", "5"],
                'bool': [True, "False", "True", False, False],
                'datetime': [
                    "2024-03-20",
                    "2024-03-21",
                    "2024-03-21",
                    "2024-03-21",
                    "2024-03-21"
                ],
                'list': [[1, 2], "[3, 4]", [5, 6], [7, 8], [9, 10]],
                'tuple': [(1, 2), "(3, 4)", (5, 6), (7, 8), (9, 10)],
                'dictionary': [
                    {'a': 1, 'b': 2.1},
                    "{'e': 3, 'f': 4.0}",
                    {'a': 1, 'b': 2.1},
                    {'a': 1, 'b': 2.1},
                    {'a': 1, 'b': 2.1}
                ],
                'set': [{1, 2}, "{1, 2}", {1, 2}, {1, 2}, {1, 2}],
                'string': ["str1", "str2", "", "12345", "I"],
                'object': [1, 2.0, False, np.nan, None]
            }
        )

        m = Model(df)
        df = m.validate()
