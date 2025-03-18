#!/usr/bin/env bash
# wait.sh

# Wait for a service to be ready before continuing.
# Usage: ./wait.sh <host> <port> -- <command>

host="$1"
shift
port="$1"
shift
cmd="$@"

until nc -z -v -w30 "$host" "$port"
do
  echo "Waiting for $host:$port..."
  sleep 2
done

echo "$host:$port is ready"
exec $cmd