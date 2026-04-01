import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# 한글 폰트 설정
for fc in ['Malgun Gothic', 'NanumGothic', 'Gulim']:
    if any(f.name == fc for f in fm.fontManager.ttflist):
        plt.rcParams['font.family'] = fc
        break
plt.rcParams['axes.unicode_minus'] = False

output_dir = r'D:\Family\Juwon\data\charts'
os.makedirs(output_dir, exist_ok=True)

# =============================================================
# 데이터 정리 (지난주 3/22 + 이번주 3/28)
# =============================================================

# 지난주 (3/22) - 제61회 빙상인후보 전국남녀 스피드스케이팅대회
# 여자중학부 3000m
race_3000m_0322 = {
    '손하니': '4:24.88', '차윤지': '4:34.35', '최하연': '4:34.68',
    '전서현': '4:36.58', '박서영': '4:37.32', '오정선': '4:39.25',
    '안경인': '4:40.58', '조주원': '4:47.93', '이혜수': '4:50.40',
    '김태희': '4:51.48', '김현영': '4:55.74', '김가연': '4:55.95',
    '최서이': '4:57.23', '임연서': '5:01.51',
}

# 이번주 (3/28) - 2026 전국남녀 초/중/고/대/실업 스피드스케이팅대회
# 500m 여자중학부
race_500m_0328_top = [
    ('김하엘', '다산한강중'),
    ('박수연', '서현중'),
    ('최윤서', '낙원중'),
    ('김다현', '고양제일중'),
    ('홍다은', '위례중'),
    ('정예진', '갈매중'),
    ('임주아', 'US'),
    ('조주원', '서울강명중'),  # 전체 8위, 1학년 1위
]

# 1000m (이번주 3/28)
race_1000m_0328 = {
    '김하엘': 85.18,   # 1:25.18
    '안경인': 85.56,   # 1:25.56 (2학년)
    '차윤지': 85.98,   # 1:25.98
    '최운서': 86.47,   # 1:26.47 (3학년)
    '한마음': 86.58,   # 1:26.58 (3학년)
    '조주원': 89.25,   # 1:29.25 (중1)
}

# 매스스타트 (이번주 3/28) - 중/고등 여자
# 지난주: 주원 6위 (5포인트), 윤지 2위
# 이번주: 주원 3위, 오정선 1위, 한마음 2위

def time_to_seconds(t):
    """'m:ss.xx' -> seconds"""
    parts = t.split(':')
    return int(parts[0]) * 60 + float(parts[1])

# =============================================================
# 1. 3000m 기록 비교 (지난주 3/22) - 주원 vs 라이벌들
# =============================================================
fig, ax = plt.subplots(figsize=(14, 7))

players_3000 = list(race_3000m_0322.keys())
times_3000 = [time_to_seconds(t) for t in race_3000m_0322.values()]

colors_3000 = []
for p in players_3000:
    if p == '조주원':
        colors_3000.append('#E74C3C')
    elif p == '차윤지':
        colors_3000.append('#3498DB')
    else:
        colors_3000.append('#BDC3C7')

bars = ax.barh(range(len(players_3000)), times_3000, color=colors_3000, height=0.6, edgecolor='white')

for i, (bar, name) in enumerate(zip(bars, players_3000)):
    t = race_3000m_0322[name]
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            t, va='center', fontsize=11, fontweight='bold',
            color='#E74C3C' if name == '조주원' else '#333')

ax.set_yticks(range(len(players_3000)))
ax.set_yticklabels(players_3000, fontsize=12)
ax.set_xlabel('기록 (초)', fontsize=13)
ax.set_title('3000m 여자중학부 — 3/22 전국대회', fontsize=16, fontweight='bold')
ax.invert_yaxis()
ax.grid(True, axis='x', alpha=0.3)
ax.set_xlim(260, 310)

# 주원이 하이라이트
idx_jw = players_3000.index('조주원')
ax.annotate('중1 (8위)', xy=(times_3000[idx_jw], idx_jw),
            xytext=(times_3000[idx_jw]+3, idx_jw+0.5),
            fontsize=11, color='#E74C3C', fontweight='bold')

fig.tight_layout()
fig.savefig(os.path.join(output_dir, '1_3000m_기록비교_0322.png'), dpi=150)
plt.close()
print("1. 3000m 기록 비교 (3/22) 저장 완료")

# =============================================================
# 2. 500m 순위 (이번주 3/28)
# =============================================================
fig, ax = plt.subplots(figsize=(12, 7))

names_500 = [f'{i+1}위 {p[0]}\n({p[1]})' for i, p in enumerate(race_500m_0328_top)]
ranks = list(range(1, len(race_500m_0328_top)+1))

colors_500 = ['#BDC3C7'] * len(race_500m_0328_top)
colors_500[7] = '#E74C3C'  # 주원이

bars = ax.barh(names_500, [8-r+1 for r in ranks], color=colors_500, height=0.6, edgecolor='white')

ax.set_xlabel('', fontsize=13)
ax.set_title('500m 여자중학부 — 3/28 전국대회\n조주원: 전체 8위 / 1학년 1위!', fontsize=16, fontweight='bold')
ax.invert_yaxis()
ax.set_xticks([])
ax.grid(False)

for i, bar in enumerate(bars):
    label = '1학년 1위!' if i == 7 else ''
    if label:
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                label, va='center', fontsize=13, fontweight='bold', color='#E74C3C')

fig.tight_layout()
fig.savefig(os.path.join(output_dir, '2_500m_순위_0328.png'), dpi=150)
plt.close()
print("2. 500m 순위 (3/28) 저장 완료")

# =============================================================
# 3. 1000m 기록 비교 (이번주 3/28)
# =============================================================
fig, ax = plt.subplots(figsize=(12, 6))

players_1000 = list(race_1000m_0328.keys())
times_1000 = list(race_1000m_0328.values())
grade_info = ['', '2학년', '동급생', '3학년', '3학년', '중1']
colors_1000 = ['#95A5A6', '#95A5A6', '#3498DB', '#95A5A6', '#95A5A6', '#E74C3C']

labels_1000 = [f'{p}\n({g})' if g else p for p, g in zip(players_1000, grade_info)]

bars = ax.barh(labels_1000, times_1000, color=colors_1000, height=0.6, edgecolor='white', linewidth=1.5)

for bar, t in zip(bars, times_1000):
    m = int(t) // 60
    s = t - m * 60
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f'{m}:{s:05.2f}', va='center', fontsize=12, fontweight='bold')

ax.set_xlabel('기록 (초)', fontsize=13)
ax.set_title('1000m 기록 비교 — 3/28 전국대회\n조주원: 중1 압도적 1위 (상위 전원 2~3학년)', fontsize=15, fontweight='bold')
ax.set_xlim(83, 91)
ax.invert_yaxis()
ax.grid(True, axis='x', alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(output_dir, '3_1000m_기록비교_0328.png'), dpi=150)
plt.close()
print("3. 1000m 기록 비교 (3/28) 저장 완료")

# =============================================================
# 4. 매스스타트 순위 변화 (지난주 vs 이번주)
# =============================================================
fig, ax = plt.subplots(figsize=(10, 6))

weeks = ['지난주 (3/22)', '이번주 (3/28)']

# 주원이: 6위 → 3위
ax.plot(weeks, [6, 3], 'o-', color='#E74C3C', markersize=14, linewidth=3, label='조주원', zorder=5)
ax.annotate('6위', (weeks[0], 6), textcoords="offset points", xytext=(15, 0),
            fontsize=14, fontweight='bold', color='#E74C3C')
ax.annotate('3위', (weeks[1], 3), textcoords="offset points", xytext=(15, 0),
            fontsize=14, fontweight='bold', color='#E74C3C')

# 윤지: 2위 → 미참가
ax.plot([weeks[0]], [2], 'o', color='#3498DB', markersize=14, linewidth=3, label='차윤지', zorder=5)
ax.annotate('2위', (weeks[0], 2), textcoords="offset points", xytext=(15, 0),
            fontsize=14, fontweight='bold', color='#3498DB')
ax.plot([weeks[1]], [2], 'x', color='#3498DB', markersize=14, linewidth=3, zorder=5)
ax.annotate('미참가', (weeks[1], 2), textcoords="offset points", xytext=(15, 0),
            fontsize=12, color='#3498DB', style='italic')

ax.fill_between(weeks, [6, 3], [6, 6], alpha=0.1, color='#E74C3C')

ax.set_ylabel('순위', fontsize=14)
ax.set_title('매스스타트 순위 변화 — 주원 vs 윤지', fontsize=16, fontweight='bold')
ax.set_ylim(0.5, 7.5)
ax.invert_yaxis()
ax.set_yticks(range(1, 8))
ax.set_yticklabels([f'{i}위' for i in range(1, 8)])
ax.legend(fontsize=13, loc='lower right')
ax.grid(True, alpha=0.3)

# 성장 표시
ax.annotate('3단계 성장!', xy=(1, 4.5), fontsize=15, color='#27AE60',
            fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAFAF1', edgecolor='#27AE60'))

fig.tight_layout()
fig.savefig(os.path.join(output_dir, '4_매스스타트_순위변화.png'), dpi=150)
plt.close()
print("4. 매스스타트 순위 변화 저장 완료")

# =============================================================
# 5. 종목별 성적 종합 (이번주 3/28)
# =============================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

events = ['매스스타트', '500m', '1000m']
overall_ranks = [3, 8, '-']
grade_ranks = [3, 1, 1]
grade_labels = ['전체 3위', '전체 8위 / 1학년 1위', '중1 1위']
colors_evt = ['#F39C12', '#E74C3C', '#2ECC71']

for i, ax_sub in enumerate(axes):
    # 큰 숫자 표시
    ax_sub.text(0.5, 0.55, f'{grade_ranks[i]}위', transform=ax_sub.transAxes,
                fontsize=48, fontweight='bold', ha='center', va='center',
                color=colors_evt[i])
    ax_sub.text(0.5, 0.25, grade_labels[i], transform=ax_sub.transAxes,
                fontsize=13, ha='center', va='center', color='#555')
    ax_sub.set_title(events[i], fontsize=16, fontweight='bold', pad=10)
    ax_sub.axis('off')

fig.suptitle('조주원 — 3/28 전국대회 종합 성적', fontsize=18, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(output_dir, '5_종목별_종합성적_0328.png'), dpi=150, bbox_inches='tight')
plt.close()
print("5. 종목별 종합 성적 저장 완료")

# =============================================================
# 6. 라이벌 비교 레이더 차트 (조주원 vs 차윤지)
# =============================================================
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

categories = ['기술/자세', '두뇌/전략', '매스스타트', '스프린트\n(500m)', '장거리\n(1000m+)', '체격/힘']
N = len(categories)

juwon_scores = [5, 5, 4, 3.5, 2.5, 2]
yunji_scores = [3, 2, 2, 4, 4, 4.5]

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]
juwon_scores_r = juwon_scores + juwon_scores[:1]
yunji_scores_r = yunji_scores + yunji_scores[:1]

ax.plot(angles, juwon_scores_r, 'o-', linewidth=2.5, label='조주원', color='#E74C3C')
ax.fill(angles, juwon_scores_r, alpha=0.15, color='#E74C3C')
ax.plot(angles, yunji_scores_r, 's-', linewidth=2.5, label='차윤지', color='#3498DB')
ax.fill(angles, yunji_scores_r, alpha=0.15, color='#3498DB')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylim(0, 5.5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=9)
ax.set_title('라이벌 비교 — 조주원 vs 차윤지', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='lower right', fontsize=12, bbox_to_anchor=(1.15, -0.05))

fig.tight_layout()
fig.savefig(os.path.join(output_dir, '6_라이벌비교_레이더.png'), dpi=150)
plt.close()
print("6. 라이벌 비교 레이더 차트 저장 완료")

# =============================================================
# 7. 3000m 주원 vs 윤지 직접 비교 (지난주)
# =============================================================
fig, ax = plt.subplots(figsize=(8, 5))

names = ['차윤지\n(2위)', '조주원\n(8위)']
times = [time_to_seconds('4:34.35'), time_to_seconds('4:47.93')]
diff = times[1] - times[0]

bars = ax.bar(names, times, color=['#3498DB', '#E74C3C'], width=0.5, edgecolor='white', linewidth=2)

for bar, t_val, t_str in zip(bars, times, ['4:34.35', '4:47.93']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            t_str, ha='center', fontsize=14, fontweight='bold')

ax.set_ylabel('기록 (초)', fontsize=13)
ax.set_title(f'3000m 직접 비교 (3/22) — 차이: {diff:.2f}초\n체격 차이(+10cm, +10kg) 감안하면 선전!',
             fontsize=14, fontweight='bold')
ax.set_ylim(260, 295)
ax.grid(True, axis='y', alpha=0.3)

fig.tight_layout()
fig.savefig(os.path.join(output_dir, '7_3000m_주원vs윤지.png'), dpi=150)
plt.close()
print("7. 3000m 주원 vs 윤지 비교 저장 완료")

print(f"\n모든 차트가 {output_dir} 에 저장되었습니다!")
chart_files = sorted(os.listdir(output_dir))
for f in chart_files:
    print(f"  - {f}")
