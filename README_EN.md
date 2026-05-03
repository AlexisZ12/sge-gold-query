<div align="center">

# Gold Hunter.skill

A clean and efficient CLI tool for querying daily market data from Shanghai Gold Exchange (SGE) ✨

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-purple?logo=robot&logoColor=white)](https://github.com/openclaw)
[![QwenPaw](https://img.shields.io/badge/Qwenpaw-Skill-orange?logo=robot&logoColor=white)](https://github.com/qwenpaw)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-brightgreen?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Requests](https://img.shields.io/badge/Requests-2.x-green)](https://docs.python-requests.org/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.x-orange)](https://www.crummy.com/software/BeautifulSoup/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-blue)](https://pandas.pydata.org/)
[![BaoStock](https://img.shields.io/badge/BaoStock-1.x-teal)](https://www.baostock.com/)

[**简体中文**](README.md) | English

</div>

---

## ✨ Features

- 🔍 **Recent Month Query** - Get market data for all trading days in the past month
- 📅 **Historical Data** - Query the nearest trading day for a specified month
- 🎯 **Multiple Contracts** - Support for gold, silver, platinum and more
- 🖥️ **CLI Friendly** - Simple parameter design, easy to integrate and automate

---

## 🚀 Quick Start

### 📦 Install Dependencies

```bash
pip install requests beautifulsoup4 python-dateutil baostock pandas
```

### 🎮 Basic Usage

```bash
# Show help 👀
python sge_gold_query.py --help

# Query recent month data 📈
python sge_gold_query.py --recent

# Query data from 3 months ago 📉
python sge_gold_query.py --ago 3
```

---

## 📖 User Guide

### 🔧 Parameters

| Parameter | Short | Description |
|:----:|:----:|------|
| `--recent` | `-r` | 🔍 Query all trading days in the past month |
| `--ago N` | `-a N` | 📅 Query the nearest trading day N months ago |
| `--contract` | `-c` | 💰 Contract code, default is `Au(T+D)` |

### 💡 Examples

```bash
# 🥇 Gold deferred (default)
python sge_gold_query.py --recent

# 🥈 Silver deferred
python sge_gold_query.py --recent --contract "Ag(T+D)"

# 🥇 Query gold data from 6 months ago
python sge_gold_query.py --ago 6 --contract "Au99.99"

# 📊 Query mini gold from 12 months ago
python sge_gold_query.py --ago 12 -c "mAu(T+D)"
```

---

## 💰 Supported Contracts

### 🥇 Gold Contracts

| Code | Description |
|:--------:|------|
| `Au99.95` | Gold 99.95% |
| `Au99.99` | Gold 99.99% |
| `Au99.5` | Gold 99.5% |
| `Au100g` | Gold 100g |
| `iAu100g` | International Gold 100g |
| `iAu99.5` | International Gold 99.5% |
| `iAu99.99` | International Gold 99.99% |
| `Au(T+D)` | Gold Deferred ⭐ Default |
| `Au(T+N1)` | Gold Deferred N1 |
| `Au(T+N2)` | Gold Deferred N2 |
| `mAu(T+D)` | Mini Gold Deferred |

### 🥈 Silver Contracts

| Code | Description |
|:--------:|------|
| `Ag99.99` | Silver 99.99% |
| `Ag(T+D)` | Silver Deferred |

### 🥉 Other Contracts

| Code | Description |
|:--------:|------|
| `Pt99.95` | Platinum 99.95% |
| `NYAuTN06` | New York Gold June |
| `NYAuTN12` | New York Gold December |
| `PGC30g` | PGC 30g |

---

## 📊 Output Examples

### Query Recent Month

**Trading info for the past 1 month (Au(T+D))**

| Date | Contract | Open | High | Low | Close | Change (CNY) | Change % | Weighted Avg | Volume (kg) | Turnover (CNY) | Open Interest | Delivery Dir | Delivery Vol |
|:----:|:----:|:------:|:------:|:------:|:------:|:----------:|:------:|:----------:|:------------:|:-------------:|:--------------:|:--------:|:------------:|
| 2026-04-10 | Au(T+D) | 1048.00 | 1055.37 | 1043.00 | 1046.45 | 4.42 | 0.42% | 1047.75 | 41402 | 43,379,211,260 | 213,152 | Long→Short | 9,926 |
| 2026-04-09 | Au(T+D) | 1056.00 | 1057.11 | 1035.62 | 1037.92 | -18.53 | -1.75% | 1042.03 | 58,436 | 60,892,230,220 | 217,996 | Short→Long | 9,898 |
| 2026-04-08 | Au(T+D) | 1031.11 | 1069.99 | 1020.65 | 1059.08 | 29.32 | 2.85% | 1056.45 | 65,284 | 68,969,896,200 | 221,448 | Long→Short | 16,470 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2026-03-13 | Au(T+D) | 1146.26 | 1149.05 | 1129.30 | 1131.25 | -14.03 | -1.23% | 1136.57 | 52,266 | 59,404,317,800 | 238,270 | Long→Short | 23,076 |

### Query N Months Ago

**Trading info from 6 months ago (Au99.99) — Date: 2025-10-10**

| Date | Contract | Open | High | Low | Close | Change (CNY) | Change % | Weighted Avg | Volume (kg) | Turnover (CNY) | Open Interest | Delivery Dir | Delivery Vol |
|:----:|:----:|:------:|:------:|:------:|:------:|:----------:|:------:|:----------:|:------------:|:-------------:|:--------------:|:--------:|:------------:|
| 2025-10-10 | Au99.99 | 913.50 | 917.80 | 896.05 | 897.63 | -13.87 | -1.52% | 900.70 | 16,002 | 14,413,113,037.2 | - | - | - |

---

## ⚠️ Notes

> 📌 **Disclaimer**: Data is for reference only and does not constitute any investment advice

> ⏰ **Trading Calendar**: Based on A-share trading days, may slightly differ from actual SGE trading days

> 🌐 **Data Source**: [Shanghai Gold Exchange](https://www.sge.com.cn/) | Trading calendar from BaoStock

> 🚫 **Request Rate**: Please do not make frequent requests to avoid server overload

---

<div align="center">

### 🌟 If this project helps you, a Star would be appreciated!

Made with ❤️ for precious metals traders

</div>
