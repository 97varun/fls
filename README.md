# Running the code

Place input files in the `data/input` directory and run the following command:

```
python src/summarize_flow_logs.py --flow-log-file sample-flow-logs.log --tag-lookup-file sample-flow-log-lookup-table.csv
```

Output will be generated in the `data/output` directory.

# Notes

- Only protocols present in the lookup table are considered to create a mapping from the protocol number to the protocol name. If we expect protocols not present in the lookup table to be present in the flow logs, we need to take another approach to handle this.