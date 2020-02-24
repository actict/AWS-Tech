Cloudwatch Logs Metric Filter for `wallet-svr_logs` log group
================================================================

# Summary
- Last Updated: 2018.10.02
- Updated by: scott.hwang@peertec.com

# Filter pattern

```
[result=ERROR, wallet, app, timestamp, msg]
```

## Sample filter pattern and matches

### boto3 script

```
./get_cloudwatch_logs.py prod wallet-svr_logs \
  "[result=DEBUG, wallet, app, timestamp, msg]" \
  '2018-10-01 00:00:00' '2018-10-01 00:00:30' \
  wallet-svr.txt

[DEBUG] wallet [ethereum_api_processor.py:582] 2018-10-01T00:00:04.511Z ========================>>>>>> findTransactionByAddresse startBlock= 6430268, endBlock = 6430271

[DEBUG] wallet [ethereum_api_processor.py:584] 2018-10-01T00:00:04.511Z ========================>>>>>> findTransactionByAddresse find startBlock= 6430261, endBlock = 6430272

[DEBUG] wallet [thread_find_block.py:149] 2018-10-01T00:00:04.810Z {'ver': '1.0', 't_id': '0001538352004810539', 'crypto': 'ETH', 'api': 'check_last_block_number', 'params': {'last_block_number': '6430272'}}
...
```

### AWS Web GUI

> The results look better when rendered as an HTML table in a
> web browser...

```
[result=DEBUG, wallet, app, timestamp, msg]

Line Number
$result
$wallet
$app
$timestamp
$msg
4
DEBUG
wallet
ethereum_api_processor.py:104
2018-09-12T01:40:02.549Z
eth_processor Nice to meet U^^ : I am Ethereum API
5
DEBUG
wallet
boscoin_api_processor.py:48
2018-09-12T01:40:02.549Z
bos_processor Nice to meet U^^ : I am Boscoin API
6
DEBUG
wallet
stellar_api_processor.py:49
2018-09-12T01:40:02.549Z
xlm_processor Nice to meet U^^ : I am Stellar API
7
DEBUG
wallet
erc20_api_processor.py:104
2018-09-12T01:40:02.551Z
erc20_processor Nice to meet U^^ : I am ERC20 API
```
