from airflow.decorators import dag, task
from datetime import datetime

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table

@dag(start_date=datetime(2025, 1, 1), schedule_interval='@daily', catchup=False, tags=['movie'])

def movie():

    load_movie_to_snowflake=aql.load_file(
        task_id='load_movie_to_snowflake',
        input_file=File(path='https://raw.githubusercontent.com/astronomer/astro-sdk/main/tests/data/imdb.csv'),
        output_table=Table(name='movie', conn_id='snowflake')
    )

movie()
