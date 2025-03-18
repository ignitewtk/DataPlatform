#!/bin/bash

# Initiate topic
kafka-topics --create --topic user-events \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1

echo "Kafka topic 'user-events' created."
