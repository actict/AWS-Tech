RDS slow_query log in Cloudwatch
=================================

# Summary
- Last Updated: 2018.11.16
- Updated by: scott.hwang@peertec.com

> AuroraDB mysql 호환 인스턴스인 경우 각종 mysql 로그를 Cloudwatch
> Logs (또는 DB 내부 테이블)에 저장할 수 있다. Cloudwatch Logs에
> 저장하면 로그를 parsing 하고 특별 조건에 따라 alarm이 발동되겠끔
> 할 수 있다.

# Cloudwatch Log DSL로 slow query query_time 추출하기

> 원본 데이터

```
# Time: 181017 12:53:16 # User@Host: peer_user[peer_user] @  [10.0.48.128]  Id:    79 # Query_time: 2.573717  Lock_time: 0.000147 Rows_sent: 100  Rows_examined: 565692 use whalex; SET timestamp=1539780796; SELECT CAST(TB_ORDER.order_id AS CHAR) AS order_id,  CAST(TB_TRADE.trade_id AS CHAR) AS trade_id,  DATE_FORMAT(TB_TRADE.trade_dtime, "%Y-%m-%dT%H:%i:%sZ") AS trade_dtime,  TB_ORDER.pair, TB_ORDER.order_side,  CAST(TB_TRADE.trade_price AS CHAR) AS trade_price,  CAST(TB_TRADE.trade_quantity AS CHAR) AS trade_quantity,  CAST(TB_TRADE.trade_amount AS CHAR) AS trade_amount,  CAST(TB_TRADE.open_quantity AS CHAR) AS open_quantity,  CAST(TB_TRADE.fee AS CHAR) AS fee,  CAST(TB_TRADE.amount_fee AS CHAR) AS amount_fee,  DATE_FORMAT(TB_ORDER.reg_dtime, "%Y-%m-%dT%H:%i:%sZ") AS order_dtime  FROM TB_ORDER  INNER JOIN TB_TRADE  ON TB_ORDER.order_id = TB_TRADE.order_id WHERE TB_ORDER.order_id BETWEEN DATE_FORMAT(DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH), "%y%m%d0000000000000") AND DATE_FORMAT(CURRENT_DATE, "%y%m320000000000000") AND TB_ORDER.user_id = 10010851 AND TB_TRADE.trade_id < 6288463 ORDER BY TB_TRADE.trade_id DESC  LIMIT 100;
```

> Cloudwatch Logs filter pattern

```
[f1, timeHdr, yymmdd, hhmmss, f4, f5, dbuser, f7, IP, IdHdr, Id, f11, queryt, querytval, lockt, locktval, query]
```
