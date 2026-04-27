#!/usr/bin/env python3
"""
财经日报图片预览生成器
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager
import numpy as np
from datetime import datetime
import pandas as pd

# 手动加载中文字体
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

class FinanceDailyPreview:
    def __init__(self, company_name="公司名称", department="财务管理部 资金管理科", date=None):
        self.company_name = company_name
        self.department = department
        self.date = date or datetime.now().strftime("%Y年%m月%d日")
        
    def create_preview(self, output_path=None):
        """创建日报预览图"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 20))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        
        y_pos = 96
        
        # 1. 头部信息
        ax.text(5, y_pos, self.company_name, fontsize=12, fontweight='bold', va='top')
        ax.text(95, y_pos, f"{self.department}    {self.date}", fontsize=9, ha='right', va='top')
        y_pos -= 3
        
        # 密级
        ax.text(5, y_pos, "□ 绝密    □ 机密    □ 秘密    ☑ 一般", fontsize=8, va='top')
        y_pos -= 4
        
        # 标题
        ax.text(50, y_pos, "今日财经新闻（日报）", fontsize=16, fontweight='bold', 
                color='#FF0000', ha='center', va='top')
        y_pos -= 5
        
        # 2. 聚焦热点标题
        self._draw_section_header(ax, 5, y_pos, 90, 3, "一、聚焦热点", '#FFF2CC')
        y_pos -= 4
        
        # 表头
        headers = ["项目", "涉及方面", "新闻/政策"]
        col_widths = [12, 15, 63]
        x_start = 5
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            self._draw_cell(ax, x_start, y_pos, width, 3, header, '#F4B084', fontweight='bold')
            x_start += width
        y_pos -= 3
        
        # 数据内容
        sections = [
            ("资金动向", "", "1、中国银行间债市表现强势，避险情绪主导之下债券向暖。利率债收益率纷纷下行，中短券表现较好。财政部拟3月11日第一次续发行320亿元50年期记账式附息国债，票面利率2.28%。"),
            ("宏观经济", "", "1、十四届全国人大四次会议将于3月5日上午9时开幕，国务院总理李强将作《政府工作报告》，3月12日下午闭幕，会期8天，共安排3次全体会议。\\n2、中国2月官方制造业PMI为49.0%，环比下降0.3个百分点；非制造业PMI为49.5%，上升0.1个百分点。"),
            ("国内新闻", "", "1、国家能源局召开会议强调，要深入推进农村能源革命，着力提升农村电网供电保障和综合承载能力，大力推进农村风电、光伏开发利用，扩大农村充电设施覆盖范围。\\n2、华为鸿蒙智行技术焕新发布会在深圳举办，全系累计交付量已达128万辆。\\n3、小米集团董事长雷军向大会提交五份建议案，涵盖人形机器人、智能汽车等不同领域。\\n4、本田汽车宣布，计划将在中国生产的纯电动汽车进口至日本市场销售。"),
            ("行业新闻", "", "1、长城汽车2月销售数据显示，海外市场销量持续增长，新能源汽车渗透率提升至35%。\\n2、国内动力电池装机量2月同比增长42%，磷酸铁锂电池占比超过70%。"),
            ("俄乌相关", "", "1、俄罗斯统计局：2025年实际工资增长4.4%，1月份失业率为2.2%。\\n2、俄罗斯经济部：1月国内生产总值（GDP）同比下降2.1%，前一个月同比增长1.9%。"),
            ("各国政策", "", "1、美国国防部长皮特·赫格塞斯表示，美伊冲突可能持续8周甚至更长时间。\\n2、美国财政部长贝森特表示，关税税率很快就会恢复到最高法院否决特朗普对等关税之前的水平。\\n3、美国总统特朗普正式提名凯文·沃什出任下一任美联储主席。\\n4、欧元区1月失业率意外下滑至6.1%，创历史新低。"),
            ("国际新闻", "", "1、美联储3月利率决议即将公布，市场预期维持利率不变。\\n2、日本央行行长表示将继续评估政策效果，yen汇率波动引发关注。"),
            ("资本市场", "", "美国三大股指全线收涨，道指涨0.49%报48739.41点，标普500指数涨0.78%报6869.5点，纳指涨1.29%报22807.48点。欧洲三大股指止跌反弹，德国DAX指数涨1.74%报24205.36点。"),
            ("黄金原油", "", "国际贵金属期货普遍收涨，COMEX黄金期货涨0.54%报5151.60美元/盎司。国际原油价格上涨，美油主力合约收涨2.08%，报76.11美元/桶；布油主力合约涨1.36%，报82.51美元/桶。"),
        ]
        
        for section, aspect, content in sections:
            # 计算内容高度
            lines = content.count('\\n') + 1
            # 根据内容长度估算行数
            content_lines = len(content) // 50 + lines
            height = max(6, content_lines * 1.2)
            
            # 项目列
            self._draw_cell(ax, 5, y_pos - height, 12, height, section, '#F2F2F2', fontsize=9)
            # 涉及方面
            self._draw_cell(ax, 17, y_pos - height, 15, height, aspect, '#FFFFFF', fontsize=9)
            # 新闻/政策（合并列）
            self._draw_cell(ax, 32, y_pos - height, 63, height, content.replace('\\n', '\\n'), '#FFFFFF', fontsize=8, wrap=True)
            
            y_pos -= height
        
        # 3. 国家政策标题
        y_pos -= 2
        self._draw_section_header(ax, 5, y_pos, 90, 3, "二、国家政策", '#FFF2CC')
        y_pos -= 4
        
        # 表头
        headers2 = ["国家部委", "涉及方面", "新闻/政策", "政策解读"]
        col_widths2 = [12, 12, 38, 28]
        x_start = 5
        for i, (header, width) in enumerate(zip(headers2, col_widths2)):
            self._draw_cell(ax, x_start, y_pos, width, 3, header, '#9BC2E6', fontweight='bold')
            x_start += width
        y_pos -= 3
        
        # 政策数据
        policies = [
            ("财政部", "国债发行", "拟于3月11日续发行320亿元50年期记账式附息国债，票面利率维持2.28%", "长期国债发行维持稳定利率，显示货币政策保持稳健，有利于锁定长期融资成本。"),
            ("国家能源局", "农村能源", "推进农村能源革命，提升电网供电保障，扩大农村充电设施覆盖", "利好新能源产业链，尤其是分布式光伏、充电桩等相关企业。"),
            ("工信部", "智能驾驶", "L2级辅助驾驶脱手脱眼拟纳入交通违法处罚，加快明确L3/L4级智驾安全准则", "智能驾驶法规加速完善，有利于行业规范化发展，关注自动驾驶技术领先企业。"),
        ]
        
        for dept, aspect, policy, interp in policies:
            height = 8
            self._draw_cell(ax, 5, y_pos - height, 12, height, dept, '#F2F2F2', fontsize=9)
            self._draw_cell(ax, 17, y_pos - height, 12, height, aspect, '#FFFFFF', fontsize=9)
            self._draw_cell(ax, 29, y_pos - height, 38, height, policy, '#FFFFFF', fontsize=8, wrap=True)
            self._draw_cell(ax, 67, y_pos - height, 28, height, interp, '#FFFFFF', fontsize=8, wrap=True)
            y_pos -= height
        
        # 保存
        if output_path is None:
            from pathlib import Path
            output_dir = Path("/root/.openclaw/workspace/finance-reports")
            output_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            output_path = output_dir / f"财经日报_{date_str}_预览.png"
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ 预览图已生成: {output_path}")
        return output_path
    
    def _draw_section_header(self, ax, x, y, width, height, text, color):
        """绘制章节标题"""
        rect = FancyBboxPatch((x, y - height), width, height,
                              boxstyle="round,pad=0.02",
                              facecolor=color,
                              edgecolor='#000000',
                              linewidth=1)
        ax.add_patch(rect)
        ax.text(x + 0.5, y - height/2, text, fontsize=10, fontweight='bold', 
                va='center', ha='left')
    
    def _draw_cell(self, ax, x, y, width, height, text, color, fontsize=9, fontweight='normal', wrap=False):
        """绘制单元格"""
        rect = patches.Rectangle((x, y), width, height,
                                  linewidth=1,
                                  edgecolor='#000000',
                                  facecolor=color)
        ax.add_patch(rect)
        
        # 文本处理
        if wrap and len(text) > 50:
            # 简单的文本换行
            words = text.replace('\\n', ' ').split()
            lines = []
            current_line = []
            current_len = 0
            for word in words:
                if current_len + len(word) < 45:
                    current_line.append(word)
                    current_len += len(word) + 1
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_len = len(word) + 1
            if current_line:
                lines.append(' '.join(current_line))
            display_text = '\\n'.join(lines[:8])  # 最多显示8行
        else:
            display_text = text
        
        # 处理换行
        display_text = display_text.replace('\\n', '\n')
        
        ax.text(x + width/2, y + height/2, display_text, 
                fontsize=fontsize, fontweight=fontweight,
                va='center', ha='center', wrap=True,
                linespacing=1.2)


if __name__ == "__main__":
    preview = FinanceDailyPreview(
        company_name="公司名称",
        department="财务管理部 资金管理科",
        date="2026年3月10日"
    )
    preview.create_preview()
