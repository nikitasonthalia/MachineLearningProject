#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
  week=`echo $line | sed 's/,.*$//'`
  echo "$line">>train_week$week.csv
done < "$1"
