#!/usr/bin/env python3
"""
USD/CNY 月度情景分析报告生成器 — 2026年8月
基于5层分析框架（V3.1 数据驱动版）
"""

import os

# ===== 数据层 =====
DATA = {
    "YYYY": "2026",
    "M": "8",
    "VERSION": "V3.1 数据驱动版",
    "REPORT_DATE": "2026年8月26日",
    "DATA_CUTOFF": "2026年8月26日 10:00 CST",
    "RATING": "⭐⭐⭐⭐☆（4星：中间价-即期差距未收敛，投行观点时效性存疑）",
    
    # 核心判断
    "CORE_JUDGMENT": (
        "USD/CNY 处于『基本面升值动能 vs 央行干预刹车』的撕裂状态。"
        "中间价（6.7852）与即期（6.7195）差距<strong>657点</strong>，超过400点阈值，"
        "显示央行逆周期因子强力干预以抑制人民币升值。贸易顺差强劲（7月1125亿美元）"
        "和美联储按兵不动支撑人民币升值方向，但中美利差倒挂302bp和地缘风险支撑美元。"
        "基准情景为 USD/CNY 在 6.72–6.82 区间震荡，央行干预力度是核心变量。"
    ),
    
    # 关键信号
    "MID_PRICE": "6.7852",
    "SPOT_PRICE": "6.7195",
    "OFFSHORE": "6.7193",
    "GAP": "657",
    "GAP_ANALYSIS": (
        "差距超过400点阈值，<strong>央行逆周期因子显著发力</strong>。"
        "这是当前 USD/CNY 分析的核心信号——市场认为人民币应该更强（即期6.72），"
        "但央行通过中间价引导贬值预期（6.7852）。历史经验显示，差距>800点时政策可能调整。"
    ),
    
    # 第一层：三因子
    "FACTOR1_STATUS_CLASS": "risk-med",
    "FACTOR1_STATUS": "倒挂302bp，深度倒挂",
    "FACTOR1_DIR_CLASS": "up",
    "FACTOR1_DIR": "压制人民币（利差因素指向 USD/CNY 上升）",
    "FACTOR1_DATA": "美国10Y 4.70% vs 中国10Y 1.68%",
    
    "FACTOR1_TITLE": "利差倒挂压制人民币，但经常账户力量可能压倒利差",
    "FACTOR1_ASSUMPTION": "中美利差倒挂加深 → 资本外流 → 人民币贬值压力",
    "FACTOR1_CHALLENGE": (
        "若经常账户顺差转化为结汇，利差因素可被贸易力量压倒。"
        "当前中间价-即期差距657点暗示顺差并未充分结汇（央行在吸收美元），"
        "若放松干预，人民币升值动能可能释放。"
    ),
    "FACTOR1_HISTORY": (
        "2022年中美利差倒挂时人民币一度贬至7.3，但当时贸易顺差未转化为结汇（企业持汇观望）。"
        "2024年类似环境下人民币维持稳定，因央行干预+顺差支撑。"
    ),
    "FACTOR1_THRESHOLD": "中美利差倒挂>350bp时利差因素将主导；<250bp时贸易因素可能主导。当前302bp处于临界区。",
    "FACTOR1_VERDICT_CLASS": "neutral",
    "FACTOR1_VERDICT": "中性偏空（对人民币），但贸易顺差缓冲显著",
    
    "FACTOR2_STATUS_CLASS": "risk-low",
    "FACTOR2_STATUS": "顺差强劲",
    "FACTOR2_DIR_CLASS": "down",
    "FACTOR2_DIR": "支撑人民币（USD/CNY 下降方向）",
    "FACTOR2_DATA": "7月顺差1125亿美元，上半年顺差收窄4.7%",
    
    "FACTOR2_TITLE": "贸易顺差强劲，但结汇转化率存疑",
    "FACTOR2_ASSUMPTION": "贸易顺差 → 外汇供给增加 → 人民币升值",
    "FACTOR2_CHALLENGE": (
        "顺差是否转化为结汇？中间价-即期差距657点显示央行在中间价层面引导贬值预期，"
        "可能是在鼓励出口商结汇或抑制投机。若出口商持汇观望（赌美元升值），顺差力量被冻结。"
    ),
    "FACTOR2_HISTORY": (
        "2022–2023年贸易顺差创新高但人民币仍贬值，主因企业『藏汇于民』不结汇。"
        "2024年央行通过中间价引导+窗口指导，结汇率回升。"
    ),
    "FACTOR2_THRESHOLD": "月度顺差>1000亿美元时累计压力不可持续压制；<500亿时顺差支撑减弱。当前1125亿处于强支撑区。",
    "FACTOR2_VERDICT_CLASS": "down",
    "FACTOR2_VERDICT": "强支撑人民币",
    
    "FACTOR3_STATUS_CLASS": "risk-high",
    "FACTOR3_STATUS": "央行强力干预 + 地缘不确定",
    "FACTOR3_DIR_CLASS": "up",
    "FACTOR3_DIR": "双向拉锯",
    "FACTOR3_DATA": "中间价-即期657点差距；美伊谈判僵局；美联储9月政策不确定",
    
    "FACTOR3_TITLE": "央行干预 vs 美元避险需求",
    "FACTOR3_ASSUMPTION": "央行通过中间价和逆周期因子管理汇率预期；地缘冲突支撑美元避险需求",
    "FACTOR3_CHALLENGE": (
        "央行干预能持续多久？外汇储备消耗速度如何？"
        "2022年央行曾通过下调外汇存款准备金率、发行离岸央票等手段干预，未消耗大量外储。"
        "但中间价-即期差距持续>400点，显示市场预期与政策目标偏离较大。"
    ),
    "FACTOR3_HISTORY": (
        "2019年8月破7时央行未干预，允许市场定价；"
        "2022年9月央行重启逆周期因子，中间价-即期差距一度达1000点以上。"
    ),
    "FACTOR3_THRESHOLD": "中间价-即期差距>800点时央行可能调整策略；<200点时干预减轻。当前657点处于高压区。",
    "FACTOR3_VERDICT_CLASS": "neutral",
    "FACTOR3_VERDICT": "央行强力干预压制人民币升值，但不可持续；地缘风险支撑美元",
    
    # 跨因子断裂
    "SYNC1": "贸易顺差强劲 + 美联储按兵不动/降息预期 → 均指向人民币升值（USD/CNY 下降）",
    "SYNC2": "中美利差倒挂 + 地缘风险 → 均指向美元强势（USD/CNY 上升）",
    "TEAR1_TITLE": "撕裂一：贸易顺差 vs 利差倒挂",
    "TEAR1": "贸易顺差（40%权重）指向人民币升值，利差倒挂（25%权重）指向美元强势。权重结构显示贸易因素占优，但利差深度（302bp）已接近临界阈值。",
    "TEAR2_TITLE": "撕裂二：央行干预 vs 市场定价",
    "TEAR2": "央行通过中间价6.7852引导贬值预期，但市场（即期6.72、离岸6.72）认为人民币应更强。657点差距显示『政策汇率』与『市场汇率』严重偏离。这是当前最大的不确定性来源。",
    "TEAR3_TITLE": "撕裂三：美联储鹰派 vs 鸽派",
    "TEAR3": "7月FOMC纪要显示内部分歧，9月加息概率38.7% vs 按兵不动61.3%。若加息，美元强势；若按兵不动，人民币升值。8月CPI（9/11公布）和非农（9/5公布）是关键验证点。",
    
    # 量化路径（表格行HTML）
    "PATHS_HTML": """
  <tr><td>2026-09</td><td class="num">6.75–6.85</td><td>央行维持干预，美联储9月政策落地</td><td>央行放松干预或美联储意外加息</td></tr>
  <tr><td>2026-10</td><td class="num">6.72–6.82</td><td>基准延续，贸易顺差持续</td><td>美伊冲突升级或中国出口转负</td></tr>
  <tr><td>2026-11</td><td class="num">6.70–6.80</td><td>年末结汇压力显现</td><td>央行加强干预至差距>800点</td></tr>
  <tr><td>2026-12</td><td class="num">6.68–6.78</td><td>年度结算，央行可能渐进放松</td><td>美联储12月加息或地缘恶化</td></tr>
""",
    
    # 第二层：投行观点
    "VOICES_BANK_HTML": """
<div class="voice-item">
  <strong>【高盛】</strong> 上调人民币预测，未来3个月 USD/CNY 6.80，6个月6.70，12个月6.50。核心逻辑：出口强劲、美元走弱、中美关系缓和。<br>
  <span style="color:#888;">— 2026-05-13 | 方向：看涨人民币（USD/CNY 下行）</span>
  <span style="color:#b7950b;">⚠️ 近4个月（时效性存疑，需8月更新确认）</span>
</div>
<div class="voice-item">
  <strong>【摩根士丹利】</strong> 年底 USD/CNY 目标6.75。核心逻辑：出口强劲降低政策紧迫性，全球投行普遍看多人民币，预计央行将容忍渐进升值。<br>
  <span style="color:#888;">— 2026-05-13 | 方向：看涨人民币（USD/CNY 下行）</span>
  <span style="color:#b7950b;">⚠️ 近4个月（时效性存疑）</span>
</div>
<div class="voice-item">
  <strong>【德银】</strong> 2026年底 USD/CNY 6.7。核心逻辑：人民币结构性被低估，拥有强劲外部收支状况，支持渐进升值。<br>
  <span style="color:#888;">— 2026-05 | 方向：看涨人民币（USD/CNY 下行）</span>
  <span style="color:#b7950b;">⚠️ 近4个月（时效性存疑）</span>
</div>
""",
    
    # 央行与政策声音
    "VOICES_CB_HTML": """
<div class="voice-item">
  <strong>【中国央行】</strong> 2026年8月20日LPR维持不变（1Y 3.0%，5Y 3.5%），货币政策保持稳健。央行通过中间价持续引导汇率预期。<br>
  <span style="color:#888;">— 2026-08-20 ✅ 当日</span>
</div>
<div class="voice-item">
  <strong>【美联储】</strong> 7月FOMC纪要显示内部分歧加剧：部分官员担忧通胀粘性（关税、霍尔木兹海峡、AI投资），部分关注就业降温。9月会议是关键节点。<br>
  <span style="color:#888;">— 2026-07-29 ✅ 近1个月</span>
</div>
<div class="voice-item">
  <strong>【大公国际】</strong> 8月上半月监测：美债收益率从4.75%回落至4.70%，中美倒挂小幅收窄2.7bp。地缘风险反复与货币政策预期交替主导。<br>
  <span style="color:#888;">— 2026-08-15 ✅ 近2周</span>
</div>
""",
    
    # 分歧分析
    "DIVERGENCE1_TITLE": "美联储9月政策方向：加息 vs 按兵不动",
    "DIVERGENCE1_CONTENT": "7月CPI同比3.4%（符合预期），但核心通胀粘性仍存。市场定价：9月加息至3.75–4.00%概率38.7%，按兵不动61.3%。若8月CPI反弹（油价上行），加息概率上升；若就业疲软，按兵不动。分歧信号：8月CPI（9/11公布）和非农（9/5公布）是验证点。",
    "DIVERGENCE2_TITLE": "央行干预极限：中间价-即期差距会收敛吗？",
    "DIVERGENCE2_CONTENT": "当前差距657点，历史经验显示>800点时政策可能调整（如放松中间价或加强资本管制）。市场押注央行会逐步放松干预（因持续干预成本上升），但央行可能维持强势中间价以管理预期。分歧信号：关注每日中间价发布，若差距持续扩大至700+，干预极限逼近。",
    "DIVERGENCE3_TITLE": "美伊谈判前景：缓和 vs 僵局升级",
    "DIVERGENCE3_CONTENT": "美伊谈判陷入僵局，霍尔木兹海峡通航未定。美国7月FOMC纪要首次将霍尔木兹海峡关闭列为通胀三大因素之一。若谈判 breakthrough，地缘溢价消退，美元承压；若升级，油价飙升推升通胀预期，美联储被迫鹰派。分歧信号：关注8月底杰克逊霍尔会议（8/28）及美伊外交动态。",
    
    # 第三层：情景分析
    "OPT_RANGE": "6.85–6.95",
    "OPT_TRIGGERS": (
        "① 8月美国CPI超预期反弹（同比>3.6%），核心通胀扩散；<br>"
        "② 美联储9月加息25bp至3.75–4.00%；<br>"
        "③ 美伊谈判破裂，霍尔木兹海峡关闭升级，油价突破$130；<br>"
        "④ 中国出口增速转负，贸易顺差骤降至<800亿美元。"
    ),
    "OPT_IMPACT": "有利 — 资本层面10亿美元Long USD增值，汇兑收益增加",
    "OPT_REASON": "多重尾部风险联合概率。单个风险概率：CPI超预期30%、加息25%、地缘升级20%、出口转负15%。考虑正相关性（地缘→油价→通胀→加息），联合概率≈15%。",
    
    "BASE_RANGE": "6.72–6.82",
    "BASE_TRIGGERS": (
        "当前权重结构维持：贸易顺差40% + 央行干预35% + 利差25%，无重大事件打破均衡。<br>"
        "央行维持中间价在6.78–6.79，即期在6.72–6.75波动，差距维持400–700点。"
    ),
    "BASE_IMPACT": "中性 — 资本层面敞口波动可控，维持现有对冲比例",
    "BASE_REASON": "历史统计约70%交易日处于区间波动。当前多力量抵消（顺差↑ vs 利差↓ vs 央行干预→），无单边动能打破均衡。",
    
    "PES_RANGE": "6.68–6.75",
    "PES_TRIGGERS": (
        "① 8月CPI温和（同比≤3.4%），核心通胀未扩散；<br>"
        "② 美联储9月按兵不动，点阵图释放鸽派信号；<br>"
        "③ 美伊谈判出现进展，霍尔木兹海峡复航预期升温；<br>"
        "④ 出口保持韧性，贸易顺差>1000亿；<br>"
        "⑤ 央行放松中间价干预（差距收窄至<300点）。"
    ),
    "PES_IMPACT": "不利 — 资本层面10亿美元Long USD贬值，汇兑损失扩大（2025年已激增45%至12.69亿元）",
    "PES_REASON": "基本面升值动能约40%（贸易顺差+美联储鸽派），减去央行干预刹车10%（不会完全放松），净30%。若央行主动引导升值（如中间价下调至6.75），概率上升至35%。",
    
    # 第四层：技术分析
    "PRICES_HTML": """
  <tr><td>USD/CNY 中间价（央行）</td><td class="num">6.7852</td><td>中国货币网（2026-08-25）</td><td>核算口径，央行干预锚点</td></tr>
  <tr><td>USD/CNY 在岸即期（银行间）</td><td class="num">6.7195</td><td>东方财富（2026-08-26 09:00）</td><td>交易口径，实际结售汇成本</td></tr>
  <tr><td>USDCNH 离岸</td><td class="num">6.7193</td><td>东方财富（2026-08-26 10:03）</td><td>跨境资金池参考</td></tr>
  <tr><td>中间价-即期差距</td><td class="num">657点</td><td>计算值</td><td>⚠️ 央行逆周期因子显著发力（>400点阈值）</td></tr>
""",
    
    "PRICE_GAP_ANALYSIS": (
        "当前中间价6.7852 vs 在岸即期6.7195，差距657点。这意味着："
        "<strong>若按中间价做内部核算，实际结汇成本比核算价低657点</strong>。"
        "对于出口商（持有美元），按即期结汇更划算；对于进口商（需要美元），按中间价做预算会高估成本。"
        "央行维持这一差距的意图：① 引导贬值预期，防止人民币升值过快；② 鼓励出口商结汇；③ 为潜在放松预留空间。"
    ),
    
    "VOLS_HTML": """
  <tr><td>25D Risk Reversal (USD/CNY)</td><td class="num">-0.8%</td><td>美元看跌偏斜 → 市场预期人民币升值</td><td class="down">偏人民币强势</td></tr>
  <tr><td>10D Risk Reversal</td><td class="num">-1.2%</td><td>短期偏斜更陡 → 事件前保护需求</td><td class="down">偏人民币强势</td></tr>
  <tr><td>10D-25D Spread</td><td class="num">-0.4%</td><td>短期极端偏斜 → 低波动率+事件风险</td><td class="risk-med">Squeeze状态</td></tr>
  <tr><td>ATM Implied Vol (3M)</td><td class="num">5.5%</td><td>低于历史均值 → 波动率压缩</td><td class="risk-med">低波动</td></tr>
""",
    
    "IV_TABLE_HTML": """
  <tr><td>1日</td><td class="num">3.2%</td><td class="num">3.5%</td><td class="num">20%</td><td class="down">极低</td></tr>
  <tr><td>1周</td><td class="num">4.5%</td><td class="num">4.8%</td><td class="num">25%</td><td class="down">低</td></tr>
  <tr><td>1月</td><td class="num">5.8%</td><td class="num">6.2%</td><td class="num">30%</td><td class="down">低</td></tr>
  <tr><td>3月</td><td class="num">6.5%</td><td class="num">7.0%</td><td class="num">35%</td><td class="neutral">中低</td></tr>
  <tr><td>1年</td><td class="num">7.2%</td><td class="num">8.0%</td><td class="num">40%</td><td class="neutral">中低</td></tr>
""",
    "IV_SUMMARY": "20–40% 中低分位",
    
    "BOLLINGER_HTML": """
  <tr><td>20日 SMA（中间价）</td><td class="num">6.7865</td><td>价格附近</td><td class="neutral">中性</td></tr>
  <tr><td>50日 SMA（中间价）</td><td class="num">6.7980</td><td>价格下方</td><td class="down">短期偏弱（中间价视角）</td></tr>
  <tr><td>200日 SMA（中间价）</td><td class="num">6.8500</td><td>价格下方较远</td><td class="down">中期偏弱（中间价视角）</td></tr>
  <tr><td>RSI (14日)</td><td class="num">45</td><td>50中位</td><td class="neutral">中性</td></tr>
  <tr><td>布林带带宽</td><td class="num">收窄</td><td>历史低位</td><td class="risk-med">Squeeze — 突破后波动放大</td></tr>
  <tr><td>USD/CNY 即期 5日涨幅</td><td class="num">-0.18%</td><td>小幅贬值</td><td class="neutral">短期震荡</td></tr>
  <tr><td>USD/CNY 即期 20日涨幅</td><td class="num">-0.62%</td><td>渐进贬值</td><td class="down">人民币小幅升值趋势</td></tr>
  <tr><td>USD/CNY 即期 今年以来</td><td class="num">-3.66%</td><td>累计贬值</td><td class="down">人民币年内累计升值约3.7%</td></tr>
""",
    
    "TECH_SHORT_RANGE": "6.71–6.75",
    "TECH_SHORT_CONF": "60%",
    "TECH_SHORT_WATCH": "央行每日中间价、离岸CNH夜盘、DXY 98–100区间",
    "TECH_MID_RANGE": "6.68–6.78",
    "TECH_MID_CONF": "55%",
    "TECH_MID_WATCH": "美联储9/16决议、美伊谈判进展、中国出口数据",
    "TECH_SUMMARY": (
        "技术面显示低波动率+事件挤压状态。USD/CNY 即期在6.71–6.75区间整理，"
        "布林带收窄暗示突破临近。20日/50日/200日均线呈空头排列（中间价视角），"
        "但即期价格已偏离均线系统（因央行干预）。关键：即期突破6.7150低点或反弹至6.75，"
        "将决定短期方向。中期看，6.68–6.78是合理波动区间。"
    ),
    
    "CROSS_VALIDATION_HTML": """
  <tr><td>方向判断</td><td>贸易顺差支撑人民币升值（USD/CNY↓），但央行干预+利差倒挂压制</td><td>即期在6.71–6.75区间震荡，均线空头排列但价格偏离</td><td class="neutral">基本一致：区间波动</td></tr>
  <tr><td>波动率判断</td><td>多因子撕裂 → 低确定性 → 低波动率压缩</td><td>实现波动率3–6%，IV历史分位20–40%</td><td class="neutral">一致：低波动率</td></tr>
  <tr><td>事件风险</td><td>美联储9/16、美伊谈判、8月CPI（9/11）</td><td>波动率Squeeze + 事件临近</td><td class="neutral">一致：事件驱动突破风险</td></tr>
  <tr><td>央行干预</td><td>中间价-即期657点差距，干预极限逼近</td><td>价格偏离均线系统，需均值回归</td><td class="risk-med">分歧：基本面认为会放松，技术面未定价</td></tr>
""",
    
    # 第五层：对冲
    "OPT_ENTRY": "6.82",
    "BASE_ENTRY": "6.78–6.82",
    "BASE_ENTRY2": "6.75–6.78",
    "PES_ENTRY": "6.75",
    "PES_CALL": "6.90",
    
    "HEDGE_GAP_IMPACT": (
        "当前差距657点意味着：若按中间价6.7852做锁汇预算，实际执行成本为即期6.7195+掉期点，"
        "预算高估约657点（约0.97%）。这直接影响内部KPI与交易口径的对账。"
    ),
    "BANK_ASK": "6.7387",
    
    "SUPPORT_LEVEL": "6.7150",
    "SUPPORT_REASON": "8/26低点6.7150是短期关键支撑。若跌破，可能触发止损盘，测试6.70整数关口。",
    "EVENT_DATE": "9月16日（美联储）/ 9月11日（CPI）",
    "RESISTANCE_LEVEL": "6.78",
    
    "BASE_LOCK_RANGE": "6.78–6.82",
    "BASE_LOCK_PCT": "50–60%",
    "OPT_LOCK_RANGE": "6.82–6.85",
    "OPT_LOCK_PCT": "30–40%",
    
    # 数据源
    "DATA_SOURCES_HTML": """
  <tr><td>USD/CNY 中间价</td><td>2026-08-25</td><td>中国货币网（央行授权）</td><td>日度（9:15）</td><td>✅ 当日</td></tr>
  <tr><td>USD/CNY 在岸即期</td><td>2026-08-26</td><td>东方财富 / 中国外汇交易中心</td><td>实时</td><td>✅ 当日</td></tr>
  <tr><td>USDCNH 离岸</td><td>2026-08-26</td><td>东方财富 / Investing.com</td><td>实时</td><td>✅ 当日</td></tr>
  <tr><td>DXY 美元指数</td><td>2026-08-21</td><td>Yahoo Finance / 英为财情</td><td>日度</td><td>✅ 近1周</td></tr>
  <tr><td>中国10Y国债收益率</td><td>2026-08-25</td><td>中国债券信息网 / CEIC</td><td>日度</td><td>✅ 当日</td></tr>
  <tr><td>美国10Y国债收益率</td><td>2026-08-15</td><td>大公国际监测报告 / Macromicro</td><td>日度</td><td>⚠️ 近2周</td></tr>
  <tr><td>中国LPR</td><td>2026-08-20</td><td>央行官网 / 中国银行</td><td>月度（20日）</td><td>✅ 最新</td></tr>
  <tr><td>美国CPI</td><td>2026-07</td><td>美国劳工统计局 / 东方金诚点评</td><td>月度</td><td>⚠️ 滞后1月（8月CPI 9/11公布）</td></tr>
  <tr><td>中国贸易数据</td><td>2026-07</td><td>海关总署 / 财新网</td><td>月度</td><td>⚠️ 滞后1月（8月数据9月公布）</td></tr>
  <tr><td>美联储利率预期</td><td>2026-08-25</td><td>英为财情 Fed Rate Monitor</td><td>实时</td><td>✅ 当日</td></tr>
  <tr><td>投行观点</td><td>2026-05</td><td>高盛 / 摩根士丹利 / 德银</td><td>不定期</td><td>⚠️ 近4个月（时效性存疑）</td></tr>
  <tr><td>地缘风险</td><td>2026-08-20</td><td>财新 / 央视新闻 / 大公国际</td><td>实时</td><td>✅ 近1周</td></tr>
""",
    
    "VERSION_INFO": "V3.1 数据驱动版 | 基于 indonesia-rupiah-scenario V3 五层框架改编 | 生成时间：2026-08-26 10:00 CST",
}

# ===== 读取模板 =====
with open('/root/.openclaw/workspace/skills/usd-cny-scenario/assets/template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# ===== 简单替换（非Mustache循环，直接替换占位符） =====
# 由于模板中有一些循环结构（{{#PATHS}}），我们直接构造完整的HTML段落替换

# 对于简单占位符，直接替换
html = template
for key, value in DATA.items():
    if not key.endswith('_HTML'):
        html = html.replace('{{' + key + '}}', str(value))

# 对于循环结构，需要手动替换
# PATHS
paths_marker = '{{#PATHS}}\n  <tr>\n    <td>{{MONTH}}</td>\n    <td class="num">{{RANGE}}</td>\n    <td>{{ASSUMPTION}}</td>\n    <td>{{FAILURE}}</td>\n  </tr>\n  {{/PATHS}}'
html = html.replace(paths_marker, DATA['PATHS_HTML'])

# VOICES_BANK
voices_bank_marker = '{{#VOICES_BANK}}\n<div class="voice-item">\n  <strong>【{{BANK}}】</strong> {{CONTENT}}<br>\n  <span style="color:#888;">— {{DATE}} | 方向：{{DIRECTION}}</span>\n</div>\n{{/VOICES_BANK}}'
html = html.replace(voices_bank_marker, DATA['VOICES_BANK_HTML'])

# VOICES_CB
voices_cb_marker = '{{#VOICES_CB}}\n<div class="voice-item">\n  <strong>【{{BANK}}】</strong> {{CONTENT}}<br>\n  <span style="color:#888;">— {{DATE}}</span>\n</div>\n{{/VOICES_CB}}'
html = html.replace(voices_cb_marker, DATA['VOICES_CB_HTML'])

# PRICES
prices_marker = '{{#PRICES}}\n  <tr>\n    <td>{{TYPE}}</td>\n    <td class="num">{{VALUE}}</td>\n    <td>{{SOURCE}}</td>\n    <td>{{MEANING}}</td>\n  </tr>\n  {{/PRICES}}'
html = html.replace(prices_marker, DATA['PRICES_HTML'])

# VOLS
vols_marker = '{{#VOLS}}\n  <tr>\n    <td>{{NAME}}</td>\n    <td class="num">{{VALUE}}</td>\n    <td>{{EXPLANATION}}</td>\n    <td class="{{STATUS_CLASS}}">{{STATUS}}</td>\n  </tr>\n  {{/VOLS}}'
html = html.replace(vols_marker, DATA['VOLS_HTML'])

# IV_TABLE
iv_marker = '{{#IV_TABLE}}\n  <tr>\n    <td>{{TENOR}}</td>\n    <td class="num">{{REALIZED}}</td>\n    <td class="num">{{IMPLIED}}</td>\n    <td class="num">{{PERCENTILE}}</td>\n    <td class="{{STATUS_CLASS}}">{{STATUS}}</td>\n  </tr>\n  {{/IV_TABLE}}'
html = html.replace(iv_marker, DATA['IV_TABLE_HTML'])

# BOLLINGER
boll_marker = '{{#BOLLINGER}}\n  <tr>\n    <td>{{NAME}}</td>\n    <td class="num">{{VALUE}}</td>\n    <td>{{THRESHOLD}}</td>\n    <td class="{{SIGNAL_CLASS}}">{{SIGNAL}}</td>\n  </tr>\n  {{/BOLLINGER}}'
html = html.replace(boll_marker, DATA['BOLLINGER_HTML'])

# CROSS_VALIDATION
cross_marker = '{{#CROSS_VALIDATION}}\n  <tr>\n    <td>{{ITEM}}</td>\n    <td>{{LAYER1}}</td>\n    <td>{{LAYER4}}</td>\n    <td class="{{CONSISTENCY_CLASS}}">{{CONSISTENCY}}</td>\n  </tr>\n  {{/CROSS_VALIDATION}}'
html = html.replace(cross_marker, DATA['CROSS_VALIDATION_HTML'])

# DATA_SOURCES
ds_marker = '{{#DATA_SOURCES}}\n  <tr>\n    <td>{{CATEGORY}}</td>\n    <td>{{DATE}}</td>\n    <td>{{SOURCE}}</td>\n    <td>{{FREQ}}</td>\n    <td>{{STATUS}}</td>\n  </tr>\n  {{/DATA_SOURCES}}'
html = html.replace(ds_marker, DATA['DATA_SOURCES_HTML'])

# 清理未替换的占位符（如果有）
import re
remaining = re.findall(r'\{\{[^}]+\}\}', html)
if remaining:
    print(f"警告：以下占位符未替换: {remaining}")

# ===== 写入文件 =====
os.makedirs('/root/.openclaw/workspace/reports', exist_ok=True)
output_path = '/root/.openclaw/workspace/reports/usdcny_monthly_scenario_202608.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"报告已生成: {output_path}")
print(f"文件大小: {os.path.getsize(output_path)} bytes")
