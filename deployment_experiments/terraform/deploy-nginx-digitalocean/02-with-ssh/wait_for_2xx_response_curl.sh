#!/bin/bash
# AI Generated, would be more responsible if meant for production.
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: $0 <url> [timeout_seconds=300]"
    exit 1
fi

url=$1
timeout=120
elapsed=0

echo "Waiting for $url to return HTTP 2xx response (timeout: ${timeout}s)..."
while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [[ "$response" =~ ^2[0-9]{2}$ ]]; then
        echo "Success! $url returned HTTP $response"
        break
    fi
    if [ $elapsed -ge $timeout ]; then
        echo "Timeout after ${timeout} seconds waiting for $url"
        exit 1
    fi
    sleep 2
    elapsed=$((elapsed + 2))
done
