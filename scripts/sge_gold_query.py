import argparse, os, sys, warnings
from datetime import date, datetime
from typing import Dict, List, Optional
import baostock as bs, pandas as pd, requests, urllib3
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

# 屏蔽警告
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'
urllib3.disable_warnings()

# 屏蔽 baostock 的日志输出
class SuppressOutput:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
    
    def __exit__(self, *args):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

def fetch_sge_quotation(start_date: str, end_date: str, inst_id: str = "Au(T+D)") -> List[Dict]:
    """
    抓取上海黄金交易所每日行情数据

    Args:
        start_date: 开始日期，格式 YYYY-MM-DD
        end_date: 结束日期，格式 YYYY-MM-DD
        inst_id: 合约代码，如 Au(T+D)、Ag(T+D) 等

    Returns:
        行情数据列表，每条记录为字典
    """
    url = "https://www.sge.com.cn/sjzx/quotation_daily_new"

    # 构造请求参数
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "inst_ids": inst_id
    }

    # 设置请求头（模拟浏览器）
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        response.raise_for_status()

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找数据表格
        table = soup.find('table')
        if not table:
            print("未找到数据表格")
            return []

        # 提取表头
        headers_list = []
        thead = table.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers_list = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

        # 如果没有 thead，尝试从第一行获取表头
        if not headers_list:
            rows = table.find_all('tr')
            if rows:
                headers_list = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]

        # 提取数据行
        data = []
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
        else:
            rows = table.find_all('tr')[1:]  # 跳过表头行

        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) == 0:
                continue

            row_data = {}
            for i, cell in enumerate(cells):
                header = headers_list[i] if i < len(headers_list) else f"column_{i}"
                row_data[header] = cell.get_text(strip=True)
            data.append(row_data)

        return data

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []
    except Exception as e:
        print(f"解析失败: {e}")
        return []

def parse_number(value: str) -> Optional[float]:
    """将字符串中的数字转换为浮点数"""
    if not value or value == '-':
        return None
    # 移除千分位逗号和百分号
    cleaned = value.replace(',', '').replace('%', '')
    try:
        return float(cleaned)
    except ValueError:
        return None

def format_table_to_string(data: List[Dict]) -> str:
    """
    将行情数据格式化为表格样式的字符串
    """
    if not data:
        return "没有获取到数据"

    # 获取所有表头（去重并保证顺序）
    headers = list(data[0].keys())
    # 定义列宽（根据表头和内容自动适配，预留一定余量）
    column_widths = {}
    for header in headers:
        # 表头长度作为基础宽度
        base_width = len(header)
        # 找出该列所有内容的最大长度
        max_content_width = max(len(str(row.get(header, ""))) for row in data)
        # 列宽取表头和内容的最大值 + 2（预留边距）
        column_widths[header] = max(base_width, max_content_width) + 2

    # 构建表格字符串
    table_str = []
    # 1. 拼接表头
    header_line = "|".join([header.ljust(column_widths[header]) for header in headers])
    table_str.append(f"+{'+'.join(['-' * column_widths[header] for header in headers])}+")
    table_str.append(f"|{header_line}|")
    table_str.append(f"+{'+'.join(['-' * column_widths[header] for header in headers])}+")

    # 2. 拼接数据行
    for row in data:
        row_line = "|".join([str(row.get(header, "")).ljust(column_widths[header]) for header in headers])
        table_str.append(f"|{row_line}|")

    # 3. 拼接表格底部边框
    table_str.append(f"+{'+'.join(['-' * column_widths[header] for header in headers])}+")

    # 合并为完整字符串
    return "\n".join(table_str)

def get_valid_dates():
    """
    获取今天的日期和一个月前的合法日期
    返回：(今天的日期, 一个月前的日期)
    """
    # 1. 获取今天的日期（格式：date对象，仅含年月日）
    today = date.today()

    # 2. 计算一个月前的日期（自动处理边界，确保合法）
    one_month_ago = today - relativedelta(months=1)

    return today, one_month_ago

def get_prev_trade_day(months):
    """
    获取【今天往前推N个月】时间点的最近前一个交易日（BaoStock官方数据源）
    :param months: 往前推的月数（1/2）
    :return: 交易日字符串（YYYY-MM-DD）
    """
    # 屏蔽 baostock 的输出
    with SuppressOutput():
        # 1. 登录BaoStock（免费无需注册）
        bs.login()
        
        # 2. 获取全量交易日历（覆盖过去2年，确保能查到）
        start_date = (datetime.now() - relativedelta(years=2)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
        
        # 3. 筛选所有交易日，转为集合
        trade_days = []
        while rs.error_code == "0" and rs.next():
            row = rs.get_row_data()
            if row[1] == "1":  # 1=交易日，0=非交易日
                trade_days.append(row[0])
        trade_days_set = set(trade_days)
        
        # 4. 计算【今天往前推N个月】的目标日期
        target_date = datetime.now() - relativedelta(months=months)
        
        # 5. 向前查找最近的交易日（核心：只找目标日期及之前的）
        current_date = target_date
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str in trade_days_set:
                bs.logout()
                return date_str
            current_date -= pd.Timedelta(days=1)  # 非交易日则继续往前找

def query_recent_month(inst_id: str = "Au(T+D)") -> str:
    """
    查询最近一个月的所有交易日数据

    Args:
        inst_id: 合约代码，默认为 Au(T+D)

    Returns:
        格式化的表格字符串
    """
    startdate, enddate = get_valid_dates()
    startdate = startdate.strftime("%Y-%m-%d")
    enddate = enddate.strftime("%Y-%m-%d")

    data = fetch_sge_quotation(enddate, startdate, inst_id)
    if data:
        table_string = format_table_to_string(data)
        return f"# 最近1个月的交易信息 ({inst_id})\n{table_string}\n"
    else:
        return "抓取失败，请检查日期格式或网络连接\n"

def query_nth_month_ago(n: int, inst_id: str = "Au(T+D)") -> str:
    """
    查询N个月前最近一个交易日的数据

    Args:
        n: 往前推的月数
        inst_id: 合约代码，默认为 Au(T+D)

    Returns:
        格式化的表格字符串
    """
    prev_trade_day = get_prev_trade_day(n)
    data = fetch_sge_quotation(prev_trade_day, prev_trade_day, inst_id)
    if data:
        table_string = format_table_to_string(data)
        return f"# {n}个月前的交易信息 ({inst_id})\n日期: {prev_trade_day}\n{table_string}\n"
    else:
        return f"抓取失败，请检查日期格式或网络连接\n"

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="上海黄金交易所行情查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 查询最近一个月的所有交易日数据（默认合约 Au(T+D)）
  python scripts/sge_gold_query.py --recent

  # 查询3个月前最近一个交易日的数据
  python scripts/sge_gold_query.py --ago 3

  # 查询最近一个月 Ag(T+D) 合约的数据
  python scripts/sge_gold_query.py --recent --contract "Ag(T+D)"

  # 查询6个月前 mAu(T+D) 合约的数据
  python scripts/sge_gold_query.py --ago 6 --contract "mAu(T+D)"
        """
    )

    # 功能选项（互斥）
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r", "--recent",
        action="store_true",
        help="查询最近一个月的所有交易日数据"
    )
    group.add_argument(
        "-a", "--ago",
        type=int,
        metavar="N",
        help="查询N个月前最近一个交易日的数据"
    )

    # 合约参数
    parser.add_argument(
        "-c", "--contract",
        type=str,
        default="Au(T+D)",
        help="合约代码，默认为 Au(T+D)"
    )

    return parser.parse_args()

def main():
    args = parse_args()

    if args.recent:
        result = query_recent_month(args.contract)
    elif args.ago is not None:
        result = query_nth_month_ago(args.ago, args.contract)
    else:
        print("错误: 必须指定 --recent 或 --ago 参数", file=sys.stderr)
        sys.exit(1)

    return result

if __name__ == "__main__":
    try:
        # 获取结果并通过 stdout 输出
        result = main()
        # 使用 sys.stdout.write 确保纯标准输出，无额外换行
        sys.stdout.write(result)
        # 补充一个换行，保证输出格式整洁
        sys.stdout.write("\n")
        # 强制刷新输出缓冲区，确保内容立即输出
        sys.stdout.flush()
    except Exception as e:
        # 异常信息输出到 stderr，避免污染正常输出
        print(f"脚本运行出错: {str(e)}", file=sys.stderr, flush=True)
        # 非0退出码表示运行失败
        sys.exit(1)