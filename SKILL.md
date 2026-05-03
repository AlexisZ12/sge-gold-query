# SGE Gold Query Skill

A command-line tool for querying daily quotation data from the Shanghai Gold Exchange (SGE).

## Purpose

Retrieve historical trading data for gold, silver, and platinum contracts from the Shanghai Gold Exchange. Useful for financial analysis, price tracking, and historical data collection.

## Dependencies

```bash
pip install requests beautifulsoup4 python-dateutil baostock pandas
```

## Command Reference

### Basic Syntax

```bash
python scripts/sge_gold_query.py <mode> [--contract <contract_code>]
```

### Modes (mutually exclusive)

| Argument | Shorthand | Description |
|----------|-----------|-------------|
| `--recent` | `-r` | Query all trading days from the past month |
| `--ago N` | `-a N` | Query the nearest trading day N months ago |

### Options

| Argument | Shorthand | Default | Description |
|----------|-----------|---------|-------------|
| `--contract` | `-c` | `Au(T+D)` | Contract symbol to query |

## Available Contracts

| Contract Code | Description |
|---------------|-------------|
| `Au99.95` | Gold 99.95% |
| `Au99.99` | Gold 99.99% |
| `Au99.5` | Gold 99.5% |
| `Au100g` | Gold 100g |
| `iAu100g` | International Gold 100g |
| `iAu99.5` | International Gold 99.5% |
| `iAu99.99` | International Gold 99.99% |
| `Au(T+D)` | Gold Deferred Settlement (default) |
| `Au(T+N1)` | Gold Deferred Settlement N1 |
| `Au(T+N2)` | Gold Deferred Settlement N2 |
| `mAu(T+D)` | Mini Gold Deferred Settlement |
| `Pt99.95` | Platinum 99.95% |
| `Ag99.99` | Silver 99.99% |
| `Ag(T+D)` | Silver Deferred Settlement |
| `NYAuTN06` | New York Gold June |
| `NYAuTN12` | New York Gold December |
| `PGC30g` | PGC 30g |

## Usage Examples

### Query recent month data

```bash
# Default contract (Au(T+D))
python scripts/sge_gold_query.py --recent

# Specific contract
python scripts/sge_gold_query.py --recent --contract "Ag(T+D)"
```

### Query historical data

```bash
# 3 months ago
python scripts/sge_gold_query.py --ago 3

# 6 months ago with specific contract
python scripts/sge_gold_query.py --ago 6 --contract "Au99.99"

# 12 months ago
python scripts/sge_gold_query.py --ago 12 -c "mAu(T+D)"
```

## Output Format

The script outputs a formatted ASCII table with trading data:

**Query recent month:**

```
# 最近1个月的交易信息 (Au(T+D))
+------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+--------------+---------+-------+--------+
|日期          |合约       |开盘价      |最高价      |最低价      |收盘价      |涨跌（元）    |涨跌幅      |加权平均价    |成交量（kg）  |成交金额（元）       |市场持仓（手）  |交收方向   |交收量（手）  |
+------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+--------------+---------+-------+--------+
|2026-04-10  |Au(T+D)  |1048.00  |1055.37  |1043.00  |1046.45  |4.42     |0.42%    |1047.75  |41402    |43379211260   |213152   |多支付给空  |9926    |
|2026-04-09  |Au(T+D)  |1056.00  |1057.11  |1035.62  |1037.92  |-18.53   |-1.75%   |1042.03  |58436    |60892230220   |217996   |空支付给多  |9898    |
|2026-04-08  |Au(T+D)  |1031.11  |1069.99  |1020.65  |1059.08  |29.32    |2.85%    |1056.45  |65284    |68969896200   |221448   |多支付给空  |16470   |
|...         |...      |...      |...      |...      |...      |...      |...      |...      |...      |...           |...      |...     |...     |
|2026-03-13  |Au(T+D)  |1146.26  |1149.05  |1129.30  |1131.25  |-14.03   |-1.23%   |1136.57  |52266    |59404317800   |238270   |多支付给空  |23076   |
+------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+--------------+---------+-------+--------+
```

**Query N months ago:**

```
# 6个月前的交易信息 (Au99.99)
日期: 2025-10-10
+------------+---------+--------+--------+--------+--------+--------+--------+--------+---------+---------------+---------+------+--------+
|日期          |合约       |开盘价     |最高价     |最低价     |收盘价     |涨跌（元）   |涨跌幅     |加权平均价   |成交量（kg）  |成交金额（元）        |市场持仓（手）  |交收方向  |交收量（手）  |
+------------+---------+--------+--------+--------+--------+--------+--------+--------+---------+---------------+---------+------+--------+
|2025-10-10  |Au99.99  |913.50  |917.80  |896.05  |897.63  |-13.87  |-1.52%  |900.70  |16002    |14413113037.2  |-        |      |        |
+------------+---------+--------+--------+--------+--------+--------+--------+--------+---------+---------------+---------+------+--------+
```

Column headers (in Chinese):
- 日期: Date
- 合约: Contract
- 开盘价: Open price
- 最高价: High price
- 最低价: Low price
- 收盘价: Close price
- 涨跌（元）: Change (CNY)
- 涨跌幅: Change percentage
- 加权平均价: Weighted average price
- 成交量（kg）: Volume (kg)
- 成交金额（元）: Turnover (CNY)
- 市场持仓（手）: Open interest (lots)
- 交收方向: Delivery direction
- 交收量（手）: Delivery volume (lots)

## Agent Usage Guidelines

1. **Always specify a mode**: Either `--recent` or `--ago N` is required
2. **Default contract**: If user doesn't specify a contract, use `Au(T+D)`
3. **Error handling**: If the script returns an error, check network connectivity and retry
4. **Rate limiting**: Avoid making rapid successive requests

## Data Sources

- Quotation data: [Shanghai Gold Exchange](https://www.sge.com.cn/)
- Trading calendar: BaoStock (A-share trading days)

## Limitations

- Trading calendar is based on A-share market, which may slightly differ from actual SGE trading days
- Historical data availability depends on SGE website
- Data is for reference only and should not be used as sole basis for investment decisions
