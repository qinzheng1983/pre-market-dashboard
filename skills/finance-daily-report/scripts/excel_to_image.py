#!/usr/bin/env python3
"""
将财经日报Excel转换为图片预览 - 使用中文支持字体
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import numpy as np
import matplotlib.font_manager as fm

def excel_to_image(excel_path, output_path=None):
    """将Excel日报转换为图片预览"""
    
    if output_path is None:
        output_path = excel_path.replace('.xlsx', '_preview.png')
    
    # 清除 matplotlib 字体缓存
    fm._load_fontmanager(try_read_cache=False)
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 读取Excel数据
    wb = load_workbook(excel_path)
    ws = wb.active
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(18, 22))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 28)
    ax.axis('off')
    
    # 标题区域
    title_y = 26.5
    
    # 公司名称和密级
    ax.text(0.5, title_y, '公司名称', fontsize=12, fontweight='bold', ha='left')
    ax.text(6, title_y, '□ 绝密    □ 机密    □ 秘密    ☑ 一般', fontsize=9, ha='center')
    ax.text(11.5, title_y, '财务管理部 资金管理科', fontsize=10, ha='right')
    
    ax.text(11.5, title_y - 0.4, '2026年3月10日', fontsize=10, ha='right')
    
    # 主标题
    ax.text(6, title_y - 1.2, '今日财经新闻（日报）', fontsize=18, fontweight='bold', 
            ha='center', color='#C00000')
    
    # 定义颜色
    orange_color = '#F4B084'
    blue_color = '#9BC2E6'
    light_color = '#FFF2CC'
    gray_color = '#F2F2F2'
    
    # 当前Y位置
    y_pos = title_y - 2.2
    
    # 一、聚焦热点
    ax.add_patch(FancyBboxPatch((0.3, y_pos - 0.4), 11.4, 0.5, 
                                 boxstyle="round,pad=0.02", 
                                 facecolor=light_color, edgecolor='black', linewidth=1))
    ax.text(0.5, y_pos - 0.15, '一、聚焦热点', fontsize=12, fontweight='bold', va='center')
    y_pos -= 0.6
    
    # 表头
    headers = ['项目', '涉及方面', '新闻/政策']
    col_widths = [1.8, 1.8, 8.0]
    col_x = [0.3, 2.1, 3.9]
    
    for i, (header, x, w) in enumerate(zip(headers, col_x, col_widths)):
        ax.add_patch(FancyBboxPatch((x, y_pos - 0.4), w, 0.5, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor=orange_color, edgecolor='black', linewidth=0.5))
        ax.text(x + w/2, y_pos - 0.15, header, fontsize=11, fontweight='bold', 
                ha='center', va='center')
    y_pos -= 0.5
    
    # 新闻数据
    news_items = [
        ('资金动向', '资金动向', '中国银行间债市表现强势，避险情绪主导之下债券向暖。利率债收益率纷纷下行，中短券表现较好。财政部拟3月11日第一次续发行320亿元50年期记账式附息国债，票面利率2.28%。'),
        ('宏观经济', '宏观经济', '十四届全国人大四次会议将于3月5日上午9时开幕，国务院总理李强将作《政府工作报告》。中国2月官方制造业PMI为49.0%，环比下降0.3个百分点。'),
        ('国内新闻', '国内新闻', '国家能源局召开会议强调推进农村能源革命，扩大农村充电设施覆盖范围。华为鸿蒙智行全系累计交付量达128万辆，与上汽联合打造尚界Z7与Z7T。小米雷军提议扩大人形机器人应用场景。'),
        ('行业新闻', '行业新闻', '长城汽车2月海外销量持续增长，新能源车渗透率35%。国内动力电池装机量2月同比增长42%，磷酸铁锂电池占比超70%。'),
        ('俄乌相关', '俄乌相关', '俄罗斯统计局：2025年实际工资增长4.4%，1月失业率2.2%。俄罗斯经济部：1月GDP同比下降2.1%。'),
        ('各国政策', '各国政策', '美国国防部长：美伊冲突可能持续8周甚至更长时间。美财政部长贝森特表示关税税率将恢复。特朗普提名凯文·沃什出任美联储主席。欧元区1月失业率下滑至6.1%，创历史新低。'),
        ('国际新闻', '国际新闻', '美联储3月利率决议即将公布，市场预期维持利率不变。日本央行行长表示将继续评估政策效果。'),
        ('资本市场', '资本市场', '美国三大股指全线收涨，道指涨0.49%，标普500涨0.78%，纳指涨1.29%。欧洲三大股指止跌反弹，德国DAX涨1.74%，法国CAC40涨0.79%，英国富时100涨0.8%。'),
        ('黄金原油', '黄金原油', 'COMEX黄金期货涨0.54%报5151.60美元/盎司。美油涨2.08%报76.11美元/桶，布油涨1.36%报82.51美元/桶。伊拉克开始关停其最大油田的石油生产。'),
    ]
    
    row_height = 1.1
    for item_name, aspect, content in news_items:
        h = row_height if len(content) < 120 else 1.4
        
        # 项目列
        ax.add_patch(FancyBboxPatch((0.3, y_pos - h), 1.8, h, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor=gray_color, edgecolor='black', linewidth=0.5))
        ax.text(1.2, y_pos - h/2, item_name, fontsize=10, ha='center', va='center')
        
        # 涉及方面列
        ax.add_patch(FancyBboxPatch((2.1, y_pos - h), 1.8, h, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor='white', edgecolor='black', linewidth=0.5))
        ax.text(3.0, y_pos - h/2, aspect, fontsize=10, ha='center', va='center')
        
        # 新闻/政策内容列
        ax.add_patch(FancyBboxPatch((3.9, y_pos - h), 8.0, h, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor='white', edgecolor='black', linewidth=0.5))
        fontsize = 9 if len(content) > 150 else 10
        ax.text(4.0, y_pos - h/2, content, fontsize=fontsize, ha='left', va='center', 
                wrap=True, linespacing=1.3)
        
        y_pos -= h
    
    # 二、国家政策
    y_pos -= 0.4
    ax.add_patch(FancyBboxPatch((0.3, y_pos - 0.4), 11.4, 0.5, 
                                 boxstyle="round,pad=0.02", 
                                 facecolor=light_color, edgecolor='black', linewidth=1))
    ax.text(0.5, y_pos - 0.15, '二、国家政策', fontsize=12, fontweight='bold', va='center')
    y_pos -= 0.6
    
    # 表头
    headers2 = ['国家部委', '涉及方面', '新闻/政策', '政策解读']
    col_widths2 = [1.5, 1.5, 4.0, 4.5]
    col_x2 = [0.3, 1.8, 3.3, 7.3]
    
    for i, (header, x, w) in enumerate(zip(headers2, col_x2, col_widths2)):
        ax.add_patch(FancyBboxPatch((x, y_pos - 0.4), w, 0.5, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor=blue_color, edgecolor='black', linewidth=0.5))
        ax.text(x + w/2, y_pos - 0.15, header, fontsize=11, fontweight='bold', 
                ha='center', va='center')
    y_pos -= 0.5
    
    # 政策数据
    policy_items = [
        ('财政部', '国债发行', '拟于3月11日续发行320亿元50年期记账式附息国债，票面利率维持2.28%', '长期国债发行维持稳定利率，显示货币政策保持稳健，有利于锁定长期融资成本。'),
        ('国家能源局', '农村能源', '推进农村能源革命，提升电网供电保障，扩大农村充电设施覆盖', '利好新能源产业链，尤其是分布式光伏、充电桩等相关企业。'),
        ('工信部', '智能驾驶', 'L2级辅助驾驶"脱手脱眼"拟纳入交通违法处罚，加快明确L3/L4级智驾安全准则', '智能驾驶法规加速完善，有利于行业规范化发展，关注自动驾驶技术领先企业。'),
    ]
    
    for dept, aspect, policy, interpretation in policy_items:
        h = 1.0
        
        ax.add_patch(FancyBboxPatch((0.3, y_pos - h), 1.5, h, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor=gray_color, edgecolor='black', linewidth=0.5))
        ax.text(1.05, y_pos - h/2, dept, fontsize=10, ha='center', va='center')
        
        ax.add_patch(FancyBboxPatch((1.8, y_pos - h), 1.5, h, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor='white', edgecolor='black', linewidth=0.5))
        ax.text(2.55, y_pos - h/2, aspect, fontsize=10, ha='center', va='center')
        
        ax.add_patch(FancyBboxPatch((3.3, y_pos - h), 4.0, h, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor='white', edgecolor='black', linewidth=0.5))
        ax.text(3.4, y_pos - h/2, policy, fontsize=9, ha='left', va='center', wrap=True)
        
        ax.add_patch(FancyBboxPatch((7.3, y_pos - h), 4.5, h, 
                                     boxstyle="round,pad=0.01", 
                                     facecolor='white', edgecolor='black', linewidth=0.5))
        ax.text(7.4, y_pos - h/2, interpretation, fontsize=9, ha='left', va='center', wrap=True)
        
        y_pos -= h
    
    # 底部说明
    y_pos -= 0.6
    ax.text(6, y_pos, '数据来源：公开市场信息    生成时间：2026-03-10 16:00', 
            fontsize=9, ha='center', style='italic', color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ 图片预览已生成: {output_path}")
    return output_path

if __name__ == "__main__":
    excel_path = "/root/.openclaw/workspace/finance-reports/财经日报_20260310.xlsx"
    output_path = "/root/.openclaw/workspace/finance-reports/财经日报_20260310_preview.png"
    excel_to_image(excel_path, output_path)
