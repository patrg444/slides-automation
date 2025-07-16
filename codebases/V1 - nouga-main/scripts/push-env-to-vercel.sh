#!/bin/bash

if [ ! -f .env ]; then
  echo ".env file not found in the project root."
  exit 1
fi

DEFAULT_ENV="production"

while IFS= read -r line || [ -n "$line" ]; do
  [[ -z "$line" || "$line" =~ ^\s*# ]] && continue

  line=$(echo "$line" | sed -E 's/^\s*export\s+//' | sed -E 's/^\s+|\s+$//g')
  [[ "$line" != *"="* ]] && continue

  key=$(echo "$line" | cut -d '=' -f 1 | sed 's/ *$//')
  value=$(echo "$line" | cut -d '=' -f 2- | sed 's/^ *//')
  value=$(echo "$value" | sed 's/^["'\'']//; s/["'\'']$//')

  echo "Updating $key..."
  vercel env rm "$key" "$DEFAULT_ENV" --yes >/dev/null 2>&1
  printf %s "$value" | vercel env add "$key" "$DEFAULT_ENV"
done < .env

echo "All variables from .env have been processed."
