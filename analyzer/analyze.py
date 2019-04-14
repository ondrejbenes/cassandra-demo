""" Analyzes transactions, searching for possible fraud. """

import os
import time
import logging

from cassandra.cluster import Cluster


def connection_factory():
    contact_point = os.environ['CASSANDRA_CONTACT_POINT']
    cluster = Cluster([contact_point])
    return cluster.connect(keyspace=os.environ['CASSANDRA_KEYSPACE'])


def analyze_transactions(connection):
    while True:
        rows = connection.execute('SELECT * FROM transaction LIMIT 5')
        for row in rows:
            logging.info(row)

        time.sleep(5)


def main():
    logging.basicConfig(level=logging.DEBUG)

    connection = connection_factory()
    analyze_transactions(connection)


if __name__ == "__main__":
    main()
