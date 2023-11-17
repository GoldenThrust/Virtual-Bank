#!/usr/bin/env bash

APPS=("users" "accounts" "credit_cards" "merchants" "notifications" "payments" "transactions" "transfers" "admin")

for app in "${APPS[@]}"
do
    python3 backend/manage.py migrate $app zero
done
