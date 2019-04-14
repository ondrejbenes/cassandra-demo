""" Generates transactions and stores them in Cassandra. """

import os
import time
import random
import logging
from uuid import uuid1

from cassandra.cluster import Cluster
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.connection import register_connection, set_default_connection


class Transaction(Model):
    __keyspace__ = os.environ['CASSANDRA_KEYSPACE']

    id = columns.TimeUUID(primary_key=True, default=uuid1)
    sender_account_number = columns.Text()
    receiver_account_number = columns.Text()


def connection_factory():
    contact_point = os.environ['CASSANDRA_CONTACT_POINT']
    cluster = Cluster([contact_point])
    connection = cluster.connect(keyspace=os.environ['CASSANDRA_KEYSPACE'])

    register_connection(str(connection), session=connection)
    set_default_connection(str(connection))

    return connection


def generate_transactions():
    while True:
        transaction = Transaction(
            sender_account_number=str(random.randint(1000, 10000)),
            receiver_account_number=str(random.randint(1000, 10000)))
        transaction.save()
        logging.info('Transaction generated.')
        time.sleep(random.randint(1, 3))


def main():
    logging.basicConfig(level=logging.DEBUG)
    connection_factory()  # creates and registers default connection
    sync_table(Transaction)
    generate_transactions()


if __name__ == "__main__":
    main()
