import pandas as pd
import numpy as np
import os
import pytest
import tempfile
import sqlalchemy as sa


df = pd.DataFrame({
    'a': np.random.rand(100),
    'b': np.random.randint(100),
    'c': np.random.choice(['a', 'b', 'c', 'd'], size=100)
})
df.index.name = 'p'


@pytest.fixture(scope='module')
def temp_db():
    f = tempfile.mkstemp(suffix='.db')[1]
    uri = 'sqlite:///' + f
    engine = sa.create_engine(uri)
    con = engine.connect()
    con.execute(
        """CREATE TABLE temp (
        p BIGINT PRIMARY KEY,
        a REAL NOT NULL,
        b BIGINT NOT NULL,
        c TEXT NOT NULL);""")
    df.to_sql('temp', uri, if_exists='append')
    try:
        yield 'temp', uri
    finally:
        if os.path.isfile(f):
            os.remove(f)
