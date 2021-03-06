import os
from datetime import datetime

import falcon
import pytz
import ujson
import pandas as pd
from logbook import Logger
from google.cloud import bigquery

from ...core.resource import BaseResource
from ...conf import settings
from ...conf.clients import get_credentials


logger = Logger(__name__)


class TopPostView(BaseResource):
    def __init__(self):
        super().__init__()
        self.dataset = 'hive_zurich'
        self.table = settings.TABLES
        self.first_block = settings.FIRST_BLOCK
        self.end_block = settings.END_BLOCK

    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'GET')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def on_get(self, req, resp):
        # init client
        size = req.get_param('size')
        if size is None:
            size = 10000
        credentials = get_credentials()
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        query_template = """
                SELECT count(operations.value.author) as amount, operations.value.author
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN {first_block} AND {end_block}
                    AND operations.value.title != ""
                GROUP BY operations.value.author
                ORDER BY amount desc
                LIMIT @limit
            """.format(dataset=self.dataset, table=self.table, first_block=self.first_block, end_block=self.end_block)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('limit', 'INT64', size),
            ]
        )
        query_job = client.query(query_template, job_config=job_config)
        df_results = query_job.to_dataframe()
        json_results = ujson.loads(df_results.to_json(orient='records'))
        self.ok(resp, json_results)


class TopCommentView(BaseResource):
    def __init__(self):
        super().__init__()
        self.dataset = 'hive_zurich'
        self.table = settings.TABLES
        self.first_block = settings.FIRST_BLOCK
        self.end_block = settings.END_BLOCK

    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'GET')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def on_get(self, req, resp):
        # init client
        size = req.get_param('size')
        if size is None:
            size = 10000
        credentials = get_credentials()
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        query_template = """
                SELECT count(operations.value.author) as amount, operations.value.author
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN {first_block} AND {end_block}
                    AND operations.value.title = ""
                GROUP BY operations.value.author
                ORDER BY amount desc
                LIMIT @limit
            """.format(dataset=self.dataset, table=self.table, first_block=self.first_block, end_block=self.end_block)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('limit', 'INT64', size),
            ]
        )
        query_job = client.query(query_template, job_config=job_config)
        df_results = query_job.to_dataframe()
        json_results = ujson.loads(df_results.to_json(orient='records'))
        self.ok(resp, json_results)


class TopWordView(BaseResource):
    def __init__(self):
        super().__init__()
        self.dataset = 'hive_zurich'
        self.table = settings.TABLES
        self.first_block = settings.FIRST_BLOCK
        self.end_block = settings.END_BLOCK

    def on_options(self, req, res):
        res.status = falcon.HTTP_200
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', 'GET')
        res.set_header('Access-Control-Allow-Headers', 'Content-Type')

    def on_get(self, req, resp):
        # init client
        size = req.get_param('size')
        if size is None:
            size = 10000
        credentials = get_credentials()
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        query_template = """
                SELECT operations.value.body
                FROM `steemit-307308.{dataset}.{table}`,
                    UNNEST (transactions) AS transactions,
                    UNNEST (transactions.operations) AS operations
                WHERE 
                    _TABLE_SUFFIX BETWEEN {first_block} AND {end_block}
                    AND operations.value.title != ""
                LIMIT @limit
            """.format(dataset=self.dataset, table=self.table, first_block=self.first_block, end_block=self.end_block)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('limit', 'INT64', size),
            ]
        )
        query_job = client.query(query_template, job_config=job_config)
        df_results = query_job.to_dataframe()
        json_results = ujson.loads(df_results.to_json(orient='records'))
        self.ok(resp, json_results)
