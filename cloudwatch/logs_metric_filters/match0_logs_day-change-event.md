Cloudwatch Logs Metric Filter for `match0_logs` log group
================================================================

# Summary
- Last Updated: 2018.10.02
- Updated by: scott.hwang@peertec.com

# Filter pattern

```
[result=STATUS, ID, app, timestamp, fs1, fs2, msg="day change event processed"]
```

## Sample matches

```
[STATUS] match_trade [trade_receiver_v2.py:351] 2018-10-02T00:00:00.218Z > '-' day change event processed
```
