import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
from datetime import datetime

for fc in ['Malgun Gothic', 'NanumGothic', 'Gulim']:
    if any(f.name == fc for f in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = fc
        break
plt.rcParams['axes.unicode_minus'] = False

output_dir = r'D:\Family\Juwon\data\charts'
os.makedirs(output_dir, exist_ok=True)

def parse_time(t):
    t = t.replace(',', '.')
    parts = t.split('.')
    if len(parts) == 3:
        return int(parts[0]) * 60 + int(parts[1]) + float('0.' + parts[2])
    return float(t)

def fmt(secs):
    if secs >= 60:
        m = int(secs) // 60
        s = secs - m * 60
        return f'{m}:{s:05.2f}'
    return f'{secs:.2f}'

# ===== 데이터 =====
# 조주원 (106570)
jw_500 = [('2023-10-07','57,22'),('2023-12-09','51,06'),('2024-02-24','49,18'),
          ('2024-11-23','47,57'),('2025-01-02','46,86'),('2025-11-15','46,99'),('2026-01-03','45,37')]
jw_1000 = [('2024-02-25','1.38,90'),('2024-10-10','1.36,77'),('2025-01-03','1.38,07'),
           ('2025-11-15','1.32,53'),('2026-01-04','1.30,50')]
jw_1500 = [('2023-12-09','2.45,03'),('2024-02-24','2.35,36'),('2024-11-23','2.29,45'),
           ('2025-01-02','2.29,04'),('2025-10-01','2.19,59'),('2026-01-03','2.15,78'),('2026-03-21','2.15,53')]

# 오정선 (106574)
js_500 = [('2024-02-24','48,52'),('2024-11-23','45,86'),('2025-01-02','45,36'),
          ('2025-11-15','44,83'),('2026-01-03','44,40')]
js_1000 = [('2023-12-09','1.41,54'),('2024-02-25','1.36,35'),('2024-10-10','1.34,10'),
           ('2025-01-03','1.29,96'),('2025-10-02','1.29,33'),('2025-11-15','1.36,57'),('2026-01-04','1.27,64')]
js_1500 = [('2023-10-09','2.34,74'),('2023-12-09','2.35,41'),('2024-02-24','2.28,21'),
           ('2024-11-23','2.19,97'),('2025-01-02','2.18,19'),('2026-01-03','2.12,83'),('2026-03-21','2.12,81')]

# PR 비교
jw_pr = {'500m': 45.37, '1000m': 90.50, '1500m': 135.53, '3000m': 286.00}
js_pr = {'500m': 44.40, '1000m': 87.64, '1500m': 132.81, '3000m': 278.85}

# ===== 차트 1: PR 직접 비교 =====
fig, ax = plt.subplots(figsize=(12, 6))

distances = ['500m', '1000m', '1500m', '3000m']
x = np.arange(len(distances))
width = 0.35

jw_vals = [jw_pr[d] for d in distances]
js_vals = [js_pr[d] for d in distances]

bars1 = ax.bar(x - width/2, jw_vals, width, label='조주원', color='#E74C3C', edgecolor='white', linewidth=1.5)
bars2 = ax.bar(x + width/2, js_vals, width, label='오정선', color='#9B59B6', edgecolor='white', linewidth=1.5)

for bar, v in zip(bars1, jw_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            fmt(v), ha='center', fontsize=10, fontweight='bold', color='#E74C3C')
for bar, v in zip(bars2, js_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            fmt(v), ha='center', fontsize=10, fontweight='bold', color='#9B59B6')

# 차이 표시
for i in range(len(distances)):
    diff = jw_vals[i] - js_vals[i]
    ax.text(x[i], max(jw_vals[i], js_vals[i]) + 8, f'+{diff:.2f}초',
            ha='center', fontsize=9, color='#555',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF3E0', edgecolor='#FF9800'))

ax.set_xticks(x)
ax.set_xticklabels(distances, fontsize=14)
ax.set_ylabel('기록 (초)', fontsize=13)
ax.set_title('개인 최고 기록 비교 — 조주원 vs 오정선 (둘 다 중1)', fontsize=16, fontweight='bold')
ax.legend(fontsize=13)
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'B1_PR비교_주원vs정선.png'), dpi=150)
plt.close()
print("B1. PR 비교 완료")

# ===== 차트 2: 500m 성장 비교 =====
fig, ax = plt.subplots(figsize=(14, 7))

for data, name, color, marker in [(jw_500, '조주원', '#E74C3C', 'o'), (js_500, '오정선', '#9B59B6', 's')]:
    dates = [datetime.strptime(d[0], '%Y-%m-%d') for d in data]
    times = [parse_time(d[1]) for d in data]
    ax.plot(dates, times, f'{marker}-', color=color, linewidth=2.5, markersize=9, label=name, zorder=5)
    for d, t in zip(dates, times):
        ax.annotate(f'{t:.2f}', (d, t), textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=8, fontweight='bold', color=color)

ax.set_title('500m 성장 비교 — 조주원 vs 오정선', fontsize=16, fontweight='bold')
ax.set_ylabel('기록 (초)', fontsize=13)
ax.legend(fontsize=13)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'B2_500m_비교_주원vs정선.png'), dpi=150)
plt.close()
print("B2. 500m 성장 비교 완료")

# ===== 차트 3: 1000m 성장 비교 =====
fig, ax = plt.subplots(figsize=(14, 7))

for data, name, color, marker in [(jw_1000, '조주원', '#E74C3C', 'o'), (js_1000, '오정선', '#9B59B6', 's')]:
    dates = [datetime.strptime(d[0], '%Y-%m-%d') for d in data]
    times = [parse_time(d[1]) for d in data]
    ax.plot(dates, times, f'{marker}-', color=color, linewidth=2.5, markersize=9, label=name, zorder=5)
    for d, t in zip(dates, times):
        ax.annotate(fmt(t), (d, t), textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=8, fontweight='bold', color=color)

ax.set_title('1000m 성장 비교 — 조주원 vs 오정선', fontsize=16, fontweight='bold')
ax.set_ylabel('기록 (초)', fontsize=13)
ax.legend(fontsize=13)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'B3_1000m_비교_주원vs정선.png'), dpi=150)
plt.close()
print("B3. 1000m 성장 비교 완료")

# ===== 차트 4: 1500m 성장 비교 =====
fig, ax = plt.subplots(figsize=(14, 7))

for data, name, color, marker in [(jw_1500, '조주원', '#E74C3C', 'o'), (js_1500, '오정선', '#9B59B6', 's')]:
    dates = [datetime.strptime(d[0], '%Y-%m-%d') for d in data]
    times = [parse_time(d[1]) for d in data]
    ax.plot(dates, times, f'{marker}-', color=color, linewidth=2.5, markersize=9, label=name, zorder=5)
    for d, t in zip(dates, times):
        ax.annotate(fmt(t), (d, t), textcoords="offset points", xytext=(0, 10),
                    ha='center', fontsize=8, fontweight='bold', color=color)

ax.set_title('1500m 성장 비교 — 조주원 vs 오정선', fontsize=16, fontweight='bold')
ax.set_ylabel('기록 (초)', fontsize=13)
ax.legend(fontsize=13)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'B4_1500m_비교_주원vs정선.png'), dpi=150)
plt.close()
print("B4. 1500m 성장 비교 완료")

# ===== 차트 5: 기록 격차 추이 (같은 대회 참가 시점만) =====
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 같은 대회에서 비교 가능한 시점 찾기
def find_common(jw_data, js_data):
    jw_dict = {d[0]: parse_time(d[1]) for d in jw_data}
    js_dict = {d[0]: parse_time(d[1]) for d in js_data}
    common_dates = sorted(set(jw_dict.keys()) & set(js_dict.keys()))
    return common_dates, jw_dict, js_dict

for ax_sub, (jw_d, js_d, dist, color) in zip(axes, [
    (jw_500, js_500, '500m', '#E74C3C'),
    (jw_1000, js_1000, '1000m', '#3498DB'),
    (jw_1500, js_1500, '1500m', '#27AE60'),
]):
    common, jw_dict, js_dict = find_common(jw_d, js_d)
    if common:
        dates = [datetime.strptime(d, '%Y-%m-%d') for d in common]
        gaps = [jw_dict[d] - js_dict[d] for d in common]
        ax_sub.bar(dates, gaps, width=20, color=color, alpha=0.7, edgecolor='white')
        for d, g in zip(dates, gaps):
            ax_sub.text(d, g + 0.1, f'{g:.2f}초', ha='center', fontsize=9, fontweight='bold')
        ax_sub.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax_sub.set_title(f'{dist} 격차\n(양수 = 정선이 빠름)', fontsize=13, fontweight='bold')
    ax_sub.set_ylabel('초', fontsize=11)
    ax_sub.grid(True, axis='y', alpha=0.3)
    ax_sub.tick_params(axis='x', rotation=45)

fig.suptitle('기록 격차 추이 — 조주원 vs 오정선 (같은 대회 비교)', fontsize=16, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'B5_격차추이_주원vs정선.png'), dpi=150)
plt.close()
print("B5. 격차 추이 완료")

# ===== 차트 6: 성장률 비교 =====
fig, ax = plt.subplots(figsize=(10, 6))

# 각 선수의 종목별 성장률 (첫 기록 대비 최고 기록 개선율)
categories = ['500m', '1000m', '1500m']
jw_improve = []
js_improve = []

for jw_d, js_d in [(jw_500, js_500), (jw_1000, js_1000), (jw_1500, js_1500)]:
    jw_times = [parse_time(d[1]) for d in jw_d]
    js_times = [parse_time(d[1]) for d in js_d]
    jw_improve.append((jw_times[0] - min(jw_times)) / jw_times[0] * 100)
    js_improve.append((js_times[0] - min(js_times)) / js_times[0] * 100)

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, jw_improve, width, label='조주원', color='#E74C3C', edgecolor='white')
bars2 = ax.bar(x + width/2, js_improve, width, label='오정선', color='#9B59B6', edgecolor='white')

for bar, v in zip(bars1, jw_improve):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{v:.1f}%', ha='center', fontsize=12, fontweight='bold', color='#E74C3C')
for bar, v in zip(bars2, js_improve):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{v:.1f}%', ha='center', fontsize=12, fontweight='bold', color='#9B59B6')

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=14)
ax.set_ylabel('기록 개선율 (%)', fontsize=13)
ax.set_title('성장률 비교 — 조주원 vs 오정선\n(첫 공식 기록 대비 최고 기록 개선율)', fontsize=16, fontweight='bold')
ax.legend(fontsize=13)
ax.grid(True, axis='y', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'B6_성장률비교_주원vs정선.png'), dpi=150)
plt.close()
print("B6. 성장률 비교 완료")

print(f"\n오정선 비교 차트 저장 완료! ({output_dir})")
for f in sorted(os.listdir(output_dir)):
    if f.startswith('B'):
        print(f"  - {f}")
