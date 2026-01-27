#!/bin/sh
set -e

echo "⏳ Waiting for Elasticsearch at $ES_HOST..."

until curl -s "$ES_HOST/_cluster/health" > /dev/null; do
  sleep 2
done

echo "✅ Elasticsearch is reachable"

create_template_payload() {
  INDEX_PATTERN="$1"

  cat <<EOF
{
  "index_patterns": ["$INDEX_PATTERN"],
  "priority": 100,
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1,
      "refresh_interval": "5s"
    },
    "mappings": {
      "dynamic": false,
      "properties": {
        "@timestamp": { "type": "date" },
        "log": { "properties": { "level": { "type": "keyword" } } },
        "host": { "properties": { "name": { "type": "keyword" } } },
        "service": { "properties": { "name": { "type": "keyword" } } },
        "trace": { "properties": { "id": { "type": "keyword" } } },
        "span": { "properties": { "id": { "type": "keyword" } } },
        "labels": { "properties": { "payment_id": { "type": "keyword" } } },
        "message": {
          "type": "text",
          "fields": {
            "raw": { "type": "keyword", "ignore_above": 1024 }
          }
        },
        "event": {
          "properties": {
            "original": { "type": "keyword", "ignore_above": 4096 }
          }
        }
      }
    }
  }
}
EOF
}

TEMPLATES="
payment_processor-template payment_processor*
api_gateway-template api_gateway*
authentication_service-template authentication_service*
fraud_detection-template fraud_detection*
ledger_service-template ledger_service*
notification_service-template notification_service*
reporting_service-template reporting_service*
risk_engine-template risk_engine*
settlement-template settlement*
"

echo "$TEMPLATES" | while read TEMPLATE_NAME INDEX_PATTERN; do
  [ -z "$TEMPLATE_NAME" ] && continue

  echo "🔍 Checking template [$TEMPLATE_NAME]..."

  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X GET "$ES_HOST/_index_template/$TEMPLATE_NAME")

  if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Template [$TEMPLATE_NAME] already exists. Skipping."
    continue
  fi

  if [ "$HTTP_STATUS" != "404" ]; then
    echo "❌ Unexpected response for [$TEMPLATE_NAME]: HTTP $HTTP_STATUS"
    exit 1
  fi

  echo "🚀 Creating template [$TEMPLATE_NAME] with pattern [$INDEX_PATTERN]..."

  curl -s -X PUT "$ES_HOST/_index_template/$TEMPLATE_NAME" \
    -H "Content-Type: application/json" \
    -d "$(create_template_payload "$INDEX_PATTERN")"

  echo "✅ Template [$TEMPLATE_NAME] created."
done

echo "🎉 All templates checked."
