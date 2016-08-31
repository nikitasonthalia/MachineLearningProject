#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
  week=`echo $line | awk -F "," '{print $2}'`
  echo "$line">>MLprojectOutput/test_week$week.csv
done < "$1"
