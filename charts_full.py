import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
from datetime import datetime

# 한글 폰트
for fc in ['Malgun Gothic', 'NanumGothic', 'Gulim']:
    if any(f.name == fc for f in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = fc
        break
plt.rcParams['axes.unicode_minus'] = False

output_dir = r'D:\Family\Juwon\data\charts'
os.makedirs(output_dir, exist_ok=True)

# =============================================================
# speedskatingresults.com API 데이터 (선수 ID: 106570)
# =============================================================

def parse_time(t):
    """'m.ss,xx' or 'ss,xx' -> seconds"""
    t = t.replace(',', '.')
    if '.' in t:
        parts = t.split('.')
        if len(parts) == 3:  # m.ss.xx
            return int(parts[0]) * 60 + int(parts[1]) + float('0.' + parts[2])
        elif len(parts) == 2:
            if int(parts[0]) > 59:  # ss.xx (just seconds)
                return float(t)
            else:  # could be ss.xx
                return float(t)
    return float(t)

# 500m 기록 (시간순)
data_500 = [
    ('2023-10-07', '57,22', '2023 공인기록회'),
    ('2023-12-09', '51,06', '제23회 꿈나무대회'),
    ('2024-02-24', '49,18', '2024 전국선수권'),
    ('2024-11-23', '47,57', '제24회 꿈나무대회'),
    ('2025-01-02', '46,86', '2025 전국선수권'),
    ('2025-11-15', '46,99', '제25회 꿈나무대회'),
    ('2026-01-03', '45,37', '2026 연령별선수권'),
]

# 1000m 기록
data_1000 = [
    ('2024-02-25', '1.38,90', '2024 전국선수권'),
    ('2024-10-10', '1.36,77', '2024 공인기록회'),
    ('2025-01-03', '1.38,07', '2025 전국선수권'),
    ('2025-11-15', '1.32,53', '제25회 꿈나무대회'),
    ('2026-01-04', '1.30,50', '2026 연령별선수권'),
]

# 1500m 기록
data_1500 = [
    ('2023-12-09', '2.45,03', '제23회 꿈나무대회'),
    ('2024-02-24', '2.35,36', '2024 전국선수권'),
    ('2024-11-23', '2.29,45', '제24회 꿈나무대회'),
    ('2025-01-02', '2.29,04', '2025 전국선수권'),
    ('2025-10-01', '2.19,59', '2025 공인기록회'),
    ('2026-01-03', '2.15,78', '2026 연령별선수권'),
    ('2026-03-21', '2.15,53', '제61회 전국대회'),
]

# 3000m 기록
data_3000 = [
    ('2026-01-04', '4.46,00', '2026 연령별선수권'),
    ('2026-03-22', '4.47,93', '제61회 전국대회'),
]

# 개인 최고 기록 (Personal Records)
pr = {
    '500m': ('45,37', '2026-01-03'),
    '1000m': ('1.30,50', '2026-01-04'),
    '1500m': ('2.15,53', '2026-03-21'),
    '3000m': ('4.46,00', '2026-01-04'),
}

def parse_time_kr(t):
    """'m.ss,xx' -> seconds"""
    t = t.replace(',', '.')
    parts = t.split('.')
    if len(parts) == 3:
        return int(parts[0]) * 60 + int(parts[1]) + float('0.' + parts[2])
    else:
        return float(t)

def format_time(secs):
    if secs >= 60:
        m = int(secs) // 60
        s = secs - m * 60
        return f'{m}:{s:05.2f}'
    else:
        return f'{secs:.2f}'

# =============================================================
# 차트 1: 500m 기록 성장 추이
# =============================================================
fig, ax = plt.subplots(figsize=(14, 7))

dates_500 = [datetime.strptime(d[0], '%Y-%m-%d') for d in data_500]
times_500 = [parse_time_kr(d[1]) for d in data_500]
names_500 = [d[2] for d in data_500]

ax.plot(dates_500, times_500, 'o-', color='#E74C3C', linewidth=3, markersize=10, zorder=5)
ax.fill_between(dates_500, times_500, max(times_500)+1, alpha=0.1, color='#E74C3C')

for i, (d, t, n) in enumerate(zip(dates_500, times_500, names_500)):
    ax.annotate(f'{t:.2f}초\n{n}', (d, t),
                textcoords="offset points", xytext=(0, 15 if i % 2 == 0 else -25),
                ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.8))

improvement = times_500[0] - times_500[-1]
ax.set_title(f'500m 기록 성장 추이 — 조주원\n{times_500[0]:.2f}초 -> {times_500[-1]:.2f}초 ({improvement:.2f}초 단축!)',
             fontsize=16, fontweight='bold')
ax.set_ylabel('기록 (초)', fontsize=13)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A1_500m_성장추이.png'), dpi=150)
plt.close()
print("A1. 500m 성장 추이 완료")

# =============================================================
# 차트 2: 1000m 기록 성장 추이
# =============================================================
fig, ax = plt.subplots(figsize=(14, 7))

dates_1000 = [datetime.strptime(d[0], '%Y-%m-%d') for d in data_1000]
times_1000 = [parse_time_kr(d[1]) for d in data_1000]
names_1000 = [d[2] for d in data_1000]

ax.plot(dates_1000, times_1000, 'o-', color='#3498DB', linewidth=3, markersize=10, zorder=5)
ax.fill_between(dates_1000, times_1000, max(times_1000)+1, alpha=0.1, color='#3498DB')

for i, (d, t, n) in enumerate(zip(dates_1000, times_1000, names_1000)):
    ax.annotate(f'{format_time(t)}\n{n}', (d, t),
                textcoords="offset points", xytext=(0, 15 if i % 2 == 0 else -25),
                ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#3498DB', alpha=0.8))

improvement = times_1000[0] - times_1000[-1]
ax.set_title(f'1000m 기록 성장 추이 — 조주원\n{format_time(times_1000[0])} -> {format_time(times_1000[-1])} ({improvement:.2f}초 단축!)',
             fontsize=16, fontweight='bold')
ax.set_ylabel('기록 (초)', fontsize=13)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A2_1000m_성장추이.png'), dpi=150)
plt.close()
print("A2. 1000m 성장 추이 완료")

# =============================================================
# 차트 3: 1500m 기록 성장 추이
# =============================================================
fig, ax = plt.subplots(figsize=(14, 7))

dates_1500 = [datetime.strptime(d[0], '%Y-%m-%d') for d in data_1500]
times_1500 = [parse_time_kr(d[1]) for d in data_1500]
names_1500 = [d[2] for d in data_1500]

ax.plot(dates_1500, times_1500, 'o-', color='#27AE60', linewidth=3, markersize=10, zorder=5)
ax.fill_between(dates_1500, times_1500, max(times_1500)+1, alpha=0.1, color='#27AE60')

for i, (d, t, n) in enumerate(zip(dates_1500, times_1500, names_1500)):
    ax.annotate(f'{format_time(t)}\n{n}', (d, t),
                textcoords="offset points", xytext=(0, 15 if i % 2 == 0 else -25),
                ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#27AE60', alpha=0.8))

improvement = times_1500[0] - times_1500[-1]
ax.set_title(f'1500m 기록 성장 추이 — 조주원\n{format_time(times_1500[0])} -> {format_time(times_1500[-1])} ({improvement:.2f}초 단축!)',
             fontsize=16, fontweight='bold')
ax.set_ylabel('기록 (초)', fontsize=13)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A3_1500m_성장추이.png'), dpi=150)
plt.close()
print("A3. 1500m 성장 추이 완료")

# =============================================================
# 차트 4: 전 종목 성장 종합 (정규화)
# =============================================================
fig, ax = plt.subplots(figsize=(16, 8))

# 각 종목별 최초 기록 대비 개선율(%)
for label, data, color, marker in [
    ('500m', data_500, '#E74C3C', 'o'),
    ('1000m', data_1000, '#3498DB', 's'),
    ('1500m', data_1500, '#27AE60', '^'),
]:
    dates = [datetime.strptime(d[0], '%Y-%m-%d') for d in data]
    times = [parse_time_kr(d[1]) for d in data]
    first = times[0]
    improvement_pct = [(first - t) / first * 100 for t in times]
    ax.plot(dates, improvement_pct, f'{marker}-', color=color, linewidth=2.5, markersize=9, label=label, zorder=5)

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_title('전 종목 기록 개선율 — 조주원\n(첫 공식 기록 대비 단축 비율 %)', fontsize=16, fontweight='bold')
ax.set_ylabel('기록 개선율 (%)', fontsize=13)
ax.legend(fontsize=13, loc='upper left')
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A4_전종목_성장종합.png'), dpi=150)
plt.close()
print("A4. 전 종목 성장 종합 완료")

# =============================================================
# 차트 5: 개인 최고 기록 (PR) 대시보드
# =============================================================
fig, axes = plt.subplots(1, 4, figsize=(16, 5))

pr_data = [
    ('500m', 45.37, '#E74C3C'),
    ('1000m', 90.50, '#3498DB'),
    ('1500m', 135.53, '#27AE60'),
    ('3000m', 286.00, '#F39C12'),
]

for ax_sub, (dist, secs, color) in zip(axes, pr_data):
    ax_sub.text(0.5, 0.6, format_time(secs), transform=ax_sub.transAxes,
                fontsize=28, fontweight='bold', ha='center', va='center', color=color)
    ax_sub.text(0.5, 0.3, pr[dist][1], transform=ax_sub.transAxes,
                fontsize=11, ha='center', va='center', color='#666')
    ax_sub.set_title(dist, fontsize=18, fontweight='bold', pad=10)
    ax_sub.axis('off')
    # 배경 원
    circle = plt.Circle((0.5, 0.5), 0.4, transform=ax_sub.transAxes,
                         fill=True, facecolor=color, alpha=0.08, edgecolor=color, linewidth=2)
    ax_sub.add_patch(circle)

fig.suptitle('조주원 개인 최고 기록 (Personal Records)', fontsize=18, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A5_개인최고기록.png'), dpi=150, bbox_inches='tight')
plt.close()
print("A5. 개인 최고 기록 완료")

# =============================================================
# 차트 6: 3/28 이번 대회 — 1000m 선수별 비교
# =============================================================
fig, ax = plt.subplots(figsize=(12, 6))

players_1000m = ['김하엘', '안경인\n(2학년)', '차윤지\n(동급생)', '최운서\n(3학년)', '한마음\n(3학년)', '조주원\n(중1)']
times_1000m = [85.18, 85.56, 85.98, 86.47, 86.58, 89.25]
colors_1000m = ['#95A5A6', '#95A5A6', '#3498DB', '#95A5A6', '#95A5A6', '#E74C3C']

bars = ax.barh(players_1000m, times_1000m, color=colors_1000m, height=0.6, edgecolor='white', linewidth=1.5)
for bar, t in zip(bars, times_1000m):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            format_time(t), va='center', fontsize=12, fontweight='bold')

ax.set_title('1000m 기록 비교 — 3/28 전국대회\n조주원: 중1 압도적 1위 (상위 전원 2~3학년)', fontsize=15, fontweight='bold')
ax.set_xlim(83, 91)
ax.invert_yaxis()
ax.grid(True, axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A6_1000m_대회비교_0328.png'), dpi=150)
plt.close()
print("A6. 1000m 대회 비교 완료")

# =============================================================
# 차트 7: 라이벌 레이더 (주원 vs 윤지)
# =============================================================
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

categories = ['기술/자세', '두뇌/전략', '매스스타트', '스프린트\n(500m)', '장거리\n(1000m+)', '체격/힘']
N = len(categories)
juwon_scores = [5, 5, 4, 3.5, 2.5, 2]
yunji_scores = [3, 2, 2, 4, 4, 4.5]

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

ax.plot(angles, juwon_scores + juwon_scores[:1], 'o-', linewidth=2.5, label='조주원', color='#E74C3C')
ax.fill(angles, juwon_scores + juwon_scores[:1], alpha=0.15, color='#E74C3C')
ax.plot(angles, yunji_scores + yunji_scores[:1], 's-', linewidth=2.5, label='차윤지', color='#3498DB')
ax.fill(angles, yunji_scores + yunji_scores[:1], alpha=0.15, color='#3498DB')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylim(0, 5.5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_title('라이벌 비교 — 조주원 vs 차윤지', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right', fontsize=12, bbox_to_anchor=(1.15, -0.05))
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A7_라이벌비교_레이더.png'), dpi=150)
plt.close()
print("A7. 라이벌 비교 레이더 완료")

# =============================================================
# 차트 8: 매스스타트 순위 변화
# =============================================================
fig, ax = plt.subplots(figsize=(10, 6))

weeks = ['지난주 (3/22)', '이번주 (3/28)']
ax.plot(weeks, [6, 3], 'o-', color='#E74C3C', markersize=14, linewidth=3, label='조주원', zorder=5)
ax.annotate('6위', (weeks[0], 6), textcoords="offset points", xytext=(15, 0),
            fontsize=14, fontweight='bold', color='#E74C3C')
ax.annotate('3위', (weeks[1], 3), textcoords="offset points", xytext=(15, 0),
            fontsize=14, fontweight='bold', color='#E74C3C')

ax.plot([weeks[0]], [2], 'o', color='#3498DB', markersize=14, label='차윤지', zorder=5)
ax.annotate('2위', (weeks[0], 2), textcoords="offset points", xytext=(15, 0),
            fontsize=14, fontweight='bold', color='#3498DB')
ax.plot([weeks[1]], [2], 'x', color='#3498DB', markersize=14, zorder=5)
ax.annotate('미참가', (weeks[1], 2), textcoords="offset points", xytext=(15, 0),
            fontsize=12, color='#3498DB', style='italic')

ax.set_title('매스스타트 순위 변화 — 주원 vs 윤지', fontsize=16, fontweight='bold')
ax.set_ylim(0.5, 7.5)
ax.invert_yaxis()
ax.set_yticks(range(1, 8))
ax.set_yticklabels([f'{i}위' for i in range(1, 8)])
ax.legend(fontsize=13)
ax.grid(True, alpha=0.3)
ax.annotate('3단계 UP!', xy=(0.5, 4.5), fontsize=15, color='#27AE60', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAFAF1', edgecolor='#27AE60'))
fig.tight_layout()
fig.savefig(os.path.join(output_dir, 'A8_매스스타트_순위변화.png'), dpi=150)
plt.close()
print("A8. 매스스타트 순위 변화 완료")

print(f"\n모든 차트 저장 완료! ({output_dir})")
for f in sorted(os.listdir(output_dir)):
    if f.startswith('A'):
        print(f"  - {f}")
