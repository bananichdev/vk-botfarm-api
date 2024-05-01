#!/bin/bash

psql -U postgres <<-EOSQL
    CREATE DATABASE "botfarm";
    CREATE DATABASE "botfarm-test";
EOSQL
