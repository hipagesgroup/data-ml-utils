# data-ml-utils
A utility python package that covers the common libraries we use.

## Installation
Since this is hosted privately on git, you will need to be under VPN, then run
```
pip install git+ssh://git@github.com/hipagesgroup/data-ml-utils@v0.2.1
```

## Feature
### Pyathena client initialisation
Almost one liner
```python
import os
from data_ml_utils.pyathena_client.client import PyAthenaClient

os.environ["AWS_ACCESS_KEY_ID"] = "xxx"
os.environ["AWS_SECRET_ACCESS_KEY"] = "xxx"

pyathena_client = PyAthenaClient()
```
![Pyathena client initialisation](docs/_static/initialise_pyathena_client.png)

### Pyathena query
Almost one liner
```python
query = """
    SELECT
        *
    FROM
        dev.test_tutorial_table
    LIMIT 10
"""

df_raw = pyathena_client.query_as_pandas(final_query=query)
```
![Pyathena query](docs/_static/query_pyathena_client.png)
