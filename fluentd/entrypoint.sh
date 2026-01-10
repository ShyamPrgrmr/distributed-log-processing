#!/bin/sh
set -e

sed \
  -e "s|__KAFKA_BROKERS__|${KAFKA_BROKERS}|g" \
  -e "s|__KAFKA_TOPIC__|${KAFKA_TOPIC}|g" \
  /etc/fluent/output.conf.template \
  > /etc/fluent/output.conf

exec fluentd -c /etc/fluent/fluent.conf