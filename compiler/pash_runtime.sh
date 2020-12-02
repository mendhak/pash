#!/bin/bash

## Check flags
pash_output_time_flag=0
for item in $@
do
    if [ "--output_time" == "$item" ]; then
        pash_output_time_flag=1
    fi
done

pash_compiled_script_file=$(mktemp -u)
python3.8 pash_runtime.py ${pash_compiled_script_file} $@

## Count the execution time and execute the compiled script
pash_exec_time_start=$(date +"%s%N")
source ${pash_compiled_script_file}
pash_exec_time_end=$(date +"%s%N")

## TODO: Maybe remove the temp file after execution

## We want the execution time in milliseconds
if [ "$pash_output_time_flag" -eq 1 ]; then
    pash_exec_time_ms=$(echo "scale = 3; ($pash_exec_time_end-$pash_exec_time_start)/1000000" | bc)
    >&2 echo "Execution time: $pash_exec_time_ms  ms"
fi