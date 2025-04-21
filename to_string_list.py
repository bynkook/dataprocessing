import numpy as np
import pandas as pd
from typing import Any, List

def to_string_list(x: Any, flatten: bool = False, keep_none: bool = True) -> List[str] | List[List[str]]:
    """
    Convert any input (scalar, iterable, numpy, pandas) into a list of strings,
    preserving the nested structure by default. Optionally, flatten and filter nulls.
    Compatible with Python 3.10 or above.

    Parameters:
    -----------
    x : Any
        Input data. Can be scalar, list, tuple, NumPy array, Pandas Series or DataFrame.
    flatten : bool, default=False
        If True, flattens the output to a single list of strings.
    keep_none : bool, default=True
        If False, filters out None, NaN, and null-like values.

    Returns:
    --------
    List[str] or List[List[str]]
        List of string-converted data, preserving structure unless flattened.

    Examples:
    ---------
    >>> to_string_list(42)
    [['42']]

    >>> to_string_list([1, None, 3], keep_none=False)
    [['1', '3']]

    >>> to_string_list([[1, 2], [3, None]], flatten=True, keep_none=False)
    ['1', '2', '3']

    >>> import numpy as np
    >>> to_string_list(np.array([[1, 2], [3, np.nan]]), flatten=False, keep_none=False)
    [['1', '2', '3']]

    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, None], 'B': ['x', 'y']})
    >>> to_string_list(df, keep_none=True)
    [['1.0', 'x'], ['nan', 'y']]
    """

    def is_null(val: Any) -> bool:
        return val is None or (isinstance(val, float) and np.isnan(val)) or pd.isna(val)

    def convert(val: Any) -> Any:
        if isinstance(val, pd.DataFrame):
            val = val.astype(str) if keep_none else val.dropna().astype(str)
            return val.values.tolist()
        elif isinstance(val, pd.Series):
            val = val.astype(str) if keep_none else val.dropna().astype(str)
            return val.tolist()
        elif isinstance(val, np.ndarray):
            if keep_none:
                return val.astype(str).tolist()
            else:
                return [str(i) for i in val.flatten() if not is_null(i)]
        elif isinstance(val, (list, tuple)):
            return [convert(i) for i in val if keep_none or not is_null(i)]
        else:
            return [str(val)] if (keep_none or not is_null(val)) else []

    def flatten_list(nested: Any) -> List[str]:
        if isinstance(nested, list):
            result = []
            for item in nested:
                result.extend(flatten_list(item))
            return result
        else:
            return [nested]

    structured = convert(x)
    return flatten_list(structured) if flatten else structured
