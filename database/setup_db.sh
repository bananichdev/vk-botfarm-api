#!/bin/bash

psql -U admin <<-EOSQL
    CREATE DATABASE "botfarm";
    CREATE DATABASE "botfarm-test";
EOSQL
