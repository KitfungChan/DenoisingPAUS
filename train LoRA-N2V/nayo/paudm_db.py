#!/usr/bin/env python
# encoding: UTF8

# Helper function to connect to PAUdm database. I intentionally 
# avoided creating a "utils.py" where people would dump all kinds
# of code.

import os
import pandas as pd

import psycopg2
from psycopg2 import OperationalError

def connect_db(at_pic=True):
    """Connect to the PAU database."""

    # Switch to read only user!

    # Store your password in this file.
    
    #pw_path = os.path.expanduser('~/paudm_pw_readonly')
    #pw = open(pw_path).readline().strip()
    pw = 'PAUsc1ence'
    
    # Requires a tunnel!
    # e.g. ssh -v -N -L 5432:db01.pau.pic.es:5432 eriksen@ui.pic.es
    cred = {'database': 'dm', 'user': 'readonly'}
    #cred['host'] = 'db01.pau.pic.es' if at_pic else 'localhost'
    cred['host'] = 'db.pau.pic.es' if at_pic else 'localhost'
    
    try:
        conn = psycopg2.connect(password=pw, **cred)
    except OperationalError:
        url = 'https://gitlab.pic.es/pau/paus-validation#database-tunnel'
        raise OperationalError(f'See {url} for how to configure a database tunnel.')

    return conn

def query(sql, conn, config={}):
    """Read SQL query into a Pandas dataframe."""

    # A bit overkill, but useful when working in a notebook.
    sql = sql.format(**config)
    cat = pd.read_sql_query(sql, conn)

    return cat
