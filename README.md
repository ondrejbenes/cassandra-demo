### About
- "bank" app creates Transactions and stores them in Cassandra
- "analyzer" checks for suspicious Transactions

### Prerequisites
- docker and docker-compose

### Install
```bash
# clone the repo
git clone git@github.com:ondrejbenes/cassandra-demo.git

# create docker network
docker network create cassandra

# create cassandra keyspace
docker-compose up -d cassandra
# when cassandra is ready
docker-compose exec cassandra cqlsh -f create.cql

# run producer and consumer
docker-compose up
```

### Roadmap
There is no actual analysis - the "analyzer" simply prints 5 newest Transactions
into stdout. The idea is to use ML (random forests) to analyze the Transactions,
based on sender and receiver account number, transferred amount, sender IP,
sender browser fingerprint etc.

Next, more C* nodes should be added to allow replication.

Finally, a Flask api should be created for the "analyzer", which would support
Transaction classification and ML model retrain.
