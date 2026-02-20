---
name: day-work
description: 오늘 해야 할 일을 정리해주는 스킬. 두레이 업무(담당자로 할당된 진행 중인 업무)와 캘린더 일정을 조회하여 프로젝트별로 정리. 아침에 "오늘 뭐해야돼?", "할일 정리해줘", "/day-work" 등으로 호출.
---

# 오늘 할 일 정리 스킬

두레이 업무와 캘린더 일정을 조회하여 오늘 해야 할 일을 프로젝트별로 정리합니다.
**로컬 웹서버**에서 대시보드를 제공합니다.

## 기본 정보

- **member_id**: `2802458672652277190` (이태양)
- **조회 대상 프로젝트**:
  - 한게임포커통합-업데이트관리: `3287834850785742288`
  - 웹보드개발랩-전체공유: `2779708918315063486`
  - 포커클래식-QA: `2378020467797929507`
- **서버 포트**: 8765
- **HTML 경로**: `/tmp/day-work-server/index.html`

## 워크플로우

### STEP 0: 웹서버 확인 및 시작

```bash
# 서버 상태 확인
python3 /Users/nhn/init/claude/commands/day-work/scripts/server.py status

# 서버가 안 떠있으면 시작
python3 /Users/nhn/init/claude/commands/day-work/scripts/server.py start
```

### STEP 1: 현재 시간 확인

```
get_date_time_now()
```

### STEP 2: 캘린더 일정 조회

```
1. 오늘 일정 조회
   - 개인 캘린더: 2802458680507427114
   - 웹보드개발랩: 2935428400867751158
   - 근태-포커사업팀: 2934647066272242745

2. 휴가 일정 제외 (아래 키워드 포함 시 표시 안함)
   - 휴가, 연차, 오프, 오프데이, 병가, 건강검진

3. 내가 참석자인 회의만 표시

4. 향후 7일 일정 추가 조회 (점검 알림용)
   - "클래식검수" 또는 "정기점검" 키워드 포함 일정 확인

5. **이전 정기점검일 조회** (커밋 검색 기준일용)
   - 이전 달 1일 ~ 오늘까지 "정기점검" 키워드 포함 일정 검색
   - 예: 현재 1월 → 작년 12월 1일부터 검색
   - 예: 현재 2월 → 올해 1월 1일부터 검색
   - 가장 최근 정기점검일을 기준일로 저장
```

### STEP 2.5: 정기점검/클래식검수 알림 체크

캘린더에서 7일 이내 "클래식검수" 또는 "정기점검" 일정이 발견되면 알림 표시

#### 2.5-1. 점검 일정 감지

```
점검 키워드: "클래식검수", "정기점검"
알림 시작: 점검일 7일 전부터
D-day 계산: 점검일까지 남은 일수
```

#### 2.5-2. 반영 필요 항목 수집

**Git 커밋 분석** (이전 정기점검일 이후 커밋):

```bash
# 기준일: STEP 2에서 찾은 이전 정기점검일

# hangame-poker-server 프로젝트 (develop + 로컬 브랜치 모두)
git -C /Users/nhn/work/hangame-poker-server log --oneline --since="{이전정기점검일}" --all

# gia 프로젝트 (develop + 로컬 브랜치 모두)
git -C /Users/nhn/work/gia log --oneline --since="{이전정기점검일}" --all
```

분석 대상:
- **Entity 변경**: `**/entity/**/*.java` 파일 수정 → DB 스키마 변경 가능성 (모든 커밋)
- **인덱스 변경**: 커밋 메시지에 "index", "인덱스" 포함 (모든 커밋)
- **GameData/Config 변경**: `resources*/GameData*`, `*Config*.json` 파일 수정 (모든 커밋)
- **내 커밋**: 커밋 메시지에 "[태양]" 포함된 것 (기타 커밋용)

**중요**: DB/GameData 변경은 다른 작업자 커밋도 포함하여 표시
- 표시 형식: `파일명 - 설명 (해시7자리, 작업자명)`
- 예: `LasPokerConfig.json - 홀덤 룸최소머니 통일 (3cccdc2, 태양)`

**위키 문서 분석**:

```
1. 개인 위키 조회
   - wiki_id: 2802458678798138998
   - 기본 페이지: claude wiki (4271894589584642618)

2. 하위 문서 조회
   - get_child_wiki_list(wiki_id, parentPageId)

3. 미완료 작업 판별
   - 문서 제목에 "완료", "done", "반영완료" 없으면 진행 중으로 간주
   - 최근 30일 내 생성/수정된 문서만
```

### STEP 3: 두레이 업무 조회

#### 3-1. 담당자(to)로 할당된 미완료 업무

```
get_task_list_with_param(project_id, task_query={
  toMemberIds: "2802458672652277190",
  postWorkflowClasses: "backlog,registered,working",
  order: "-updatedAt"
})
```

#### 3-2. 참조자(cc)로 태그된 최근 업무

```
get_task_list_with_param(project_id, task_query={
  ccMemberIds: "2802458672652277190",
  updatedAt: "prev-7d",
  order: "-updatedAt"
})
```

#### 3-3. 각 프로젝트별로 조회

- 한게임포커통합-업데이트관리 (3287834850785742288)
- 웹보드개발랩-전체공유 (2779708918315063486)
- 포커클래식-QA (2378020467797929507)

### STEP 4: 업무 상세 정보 및 최근 활동 조회

진행중(working) 업무와 주요 업무는 상세 정보 + 최근 활동 조회:

#### 4-1. 업무 상세 조회
```
get_detail_of_task_by_id(post_id)
- body.content에서 업무 설명 추출 (1-2줄 요약)
- updatedAt으로 마지막 수정일 확인
```

#### 4-2. 최근 댓글 조회 (7일 이내 업데이트된 업무만)
```
get_post_comments(project_id, post_id, order="-createdAt", size=5)
- 가장 최근 댓글의 내용과 시간 확인
- 댓글 작성자와 내용 1줄 요약
```

#### 4-3. 업데이트 정보 계산
```
현재시간 - updatedAt 또는 최신댓글시간 비교:
- 24시간 이내: "NEW" 배지 + "N시간 전"
- 1~7일: "N일 전 업데이트" 표시
- 7일 초과: 표시 안함

최근 댓글이 있으면:
- "💬 {작성자}: {내용요약} (N시간/일 전)" 형태로 표시
```

### STEP 5: HTML 대시보드 생성

결과를 `/tmp/day-work-server/index.html` 파일로 생성

## 출력 규칙

1. **프로젝트별 그룹화**: 같은 프로젝트 업무는 묶어서 표시
2. **상태별 분류**: 진행중 → 할일 → 대기 순서로 표시
3. **만기일 강조**: 만기일이 오늘이거나 임박한 업무는 강조 표시
4. **참조자 업무 별도 섹션**: 내가 참조자로 태그된 업무는 "확인 필요" 섹션에 표시
5. **주간보고 제외**: 제목에 "주간보고"가 포함된 업무는 목록에서 제외
6. **업무 설명 표시**: 각 업무의 body 내용을 요약하여 표시
7. **오래된 업무 분리**: 마지막 갱신일이 40일 초과된 업무는 "기타 업무" 섹션으로 분리
   - 표시: 프로젝트명 | #번호 | 제목 | 마지막 갱신일
8. **점검 알림 배너**: 정기점검 7일 전부터만 표시 (그 외에는 숨김)
   - **좌우 2단 레이아웃**: DB/GameData 변경 왼쪽, 위키/기타커밋 오른쪽
9. **GameData/DB 변경**: 내 커밋뿐 아니라 다른 작업자 커밋도 포함
   - 표시: 파일명 - 설명 (커밋해시 짧게, 작업자명)
10. **레이아웃 순서**: 점검알림 → 요약 → 캘린더 → **집중포인트** → 업무목록 → 기타업무
11. **최근 업데이트 표시** (업무 제목 옆에 표시):
    - **24시간 이내**: `NEW` 배지 + "N시간 전" (빨간색 강조)
    - **1~7일 이내**: "N일 전" 표시 (노란색)
    - **7일 초과**: 표시 안함
    - **최근 댓글 있으면**: 업무 아래에 "💬 {작성자}: {내용 한줄 요약} (N시간/일 전)" 표시
    - 예시: `#1234 업무제목 NEW 3시간 전` 또는 `#1234 업무제목 2일 전`

## 상태 분류

| 상태 | 아이콘 | 설명 |
|------|--------|------|
| working | 🔴 | 진행중 - 현재 작업 중 |
| registered | 📝 | 할일 - 시작 대기 |
| backlog | ⏸️ | 대기 - 검토/보류 |
| closed | ✅ | 완료 (참조자 태그된 것만 표시) |

## HTML 템플릿

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="300"> <!-- 5분마다 자동 새로고침 -->
    <title>오늘의 할 일 - {날짜}</title>
    <style>
        body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #e0e0e0; font-family: system-ui; min-height: 100vh; margin: 0; padding: 15px; font-size: 13px; }
        .container { max-width: 1800px; margin: 0 auto; }
        h1 { font-size: 1.4em; margin-bottom: 15px; }
        h2 { font-size: 1.1em; margin: 0 0 12px 0; }
        h3 { font-size: 1em; margin: 10px 0 8px 0; color: #aaa; }

        /* 요약 카드 */
        .summary { display: flex; gap: 15px; margin-bottom: 20px; }
        .stat-card { background: rgba(255,255,255,0.1); border-radius: 10px; padding: 12px 16px; flex: 1; font-size: 0.95em; }
        .stat-card.working { border-left: 3px solid #ff6b6b; }
        .stat-card.registered { border-left: 3px solid #4ecdc4; }
        .stat-card.backlog { border-left: 3px solid #95a5a6; }
        .stat-card.cc { border-left: 3px solid #f39c12; }

        /* 프로젝트 섹션 */
        .project { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; margin-bottom: 15px; }
        .project h2 { color: #4ecdc4; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; }

        /* 업무 카드 */
        .task { background: rgba(255,255,255,0.08); border-radius: 6px; padding: 10px 12px; margin: 8px 0; }
        .task-title { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        .task-title a { color: #74b9ff; text-decoration: none; font-size: 0.95em; }
        .task-desc { color: #b0b0b0; font-size: 0.85em; margin-top: 4px; line-height: 1.4; }
        .task-comment { color: #74b9ff; font-size: 0.8em; margin-top: 4px; padding: 4px 8px; background: rgba(116,185,255,0.1); border-radius: 4px; }
        .task-meta { color: #888; font-size: 0.8em; margin-top: 6px; }

        /* 상태 배지 */
        .badge { padding: 2px 6px; border-radius: 3px; font-size: 0.75em; }
        .badge.working { background: #ff6b6b; color: white; }
        .badge.registered { background: #4ecdc4; color: white; }
        .badge.backlog { background: #95a5a6; color: white; }
        .badge.new { background: #e74c3c; color: white; animation: pulse 2s infinite; }
        .badge.comment { background: #3498db; color: white; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }

        /* 업데이트 시간 */
        .update-time { color: #888; font-size: 0.75em; }
        .update-time.recent { color: #f39c12; }

        /* 캘린더 2단 레이아웃 */
        .calendar-row { display: flex; gap: 15px; margin-bottom: 15px; }
        .calendar-row .project { flex: 1; margin-bottom: 0; }
        .calendar-item { padding: 8px 12px; background: rgba(255,255,255,0.08); border-radius: 6px; margin: 6px 0; display: flex; align-items: center; gap: 12px; font-size: 0.9em; }
        .calendar-time { color: #4ecdc4; font-weight: 500; min-width: 90px; }
        .calendar-date { color: #f39c12; font-weight: 500; min-width: 70px; }

        /* 점검 알림 배너 - 좌우 2단 */
        .deploy-alert {
            background: linear-gradient(135deg, #8e7cc3 0%, #674ea7 100%);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #d9d2e9;
        }
        .deploy-alert h2 { color: #fff; margin: 0 0 10px 0; font-size: 1.1em; }
        .deploy-alert .d-day { font-size: 1.2em; font-weight: bold; color: #fff; margin-bottom: 12px; }
        .deploy-alert .checklist-row { display: flex; gap: 15px; }
        .deploy-alert .checklist-col { flex: 1; background: rgba(255,255,255,0.1); border-radius: 6px; padding: 12px; }
        .deploy-alert .checklist-section { margin-bottom: 10px; }
        .deploy-alert .checklist-section:last-child { margin-bottom: 0; }
        .deploy-alert .section-title { font-weight: 600; color: #d9d2e9; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; font-size: 0.9em; }
        .deploy-alert .section-content { color: #e8e8e8; padding-left: 20px; font-size: 0.85em; line-height: 1.5; }
        .deploy-alert .important { background: rgba(255,255,255,0.15); padding: 1px 6px; border-radius: 3px; font-weight: 500; }
        .deploy-alert .minor { color: #c0b8d0; font-size: 0.85em; }
        .deploy-alert .committer { color: #c0b8d0; font-size: 0.85em; }
        .deploy-alert a { color: #d9d2e9; text-decoration: underline; }

        /* 집중 포인트 */
        .focus-box { background: rgba(255,193,7,0.15); border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 4px solid #ffc107; }
        .focus-box h2 { color: #ffc107; margin: 0 0 10px 0; }
        .focus-list { margin: 0; padding-left: 20px; }
        .focus-list li { margin: 4px 0; font-size: 0.9em; }

        /* 기타 업무 테이블 */
        .other-tasks { background: rgba(255,255,255,0.03); }
        .other-task-table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
        .other-task-table th { text-align: left; padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); color: #888; font-weight: 500; }
        .other-task-table td { padding: 6px 8px; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .other-task-table a { color: #74b9ff; text-decoration: none; }
        .other-task-table .date { color: #888; }

        /* 생성 시간 */
        .generated-time { text-align: right; color: #666; font-size: 0.75em; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 오늘의 할 일 - {날짜}</h1>

        <!-- 점검 알림 배너 (7일 이내 점검 있을 때만, 좌우 2단) -->
        <div class="deploy-alert">
            <h2>📦 정기점검 반영 체크</h2>
            <div class="d-day">D-N (MM/DD 요일 한게임 정기점검)</div>
            <div class="checklist-row">
                <div class="checklist-col">
                    <div class="checklist-section">
                        <div class="section-title">🗄️ DB 변경</div>
                        <div class="section-content">없음 또는 Entity 변경 내역</div>
                    </div>
                    <div class="checklist-section">
                        <div class="section-title">⚙️ GameData 변경</div>
                        <div class="section-content">
                            <span class="important">파일명.json</span> - 변경 내용 <span class="committer">(해시, 작업자)</span>
                        </div>
                    </div>
                </div>
                <div class="checklist-col">
                    <div class="checklist-section">
                        <div class="section-title">📝 위키 작업 문서</div>
                        <div class="section-content"><a href="URL">작업명</a></div>
                    </div>
                    <div class="checklist-section">
                        <div class="section-title">💻 기타 커밋</div>
                        <div class="section-content minor">커밋 목록</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 요약 통계 -->
        <div class="summary">
            <div class="stat-card working">🔴 진행중: N건</div>
            <div class="stat-card registered">📝 할일: N건</div>
            <div class="stat-card backlog">⏸️ 대기: N건</div>
            <div class="stat-card cc">👀 확인필요: N건</div>
        </div>

        <!-- 캘린더 (오늘 + 다가오는 일정 나란히) -->
        <div class="calendar-row">
            <div class="project">
                <h2>📅 오늘 일정</h2>
                <div class="calendar-item">
                    <span class="calendar-time">10:00 - 11:00</span>
                    <span>팀 미팅</span>
                </div>
            </div>
            <div class="project">
                <h2>📆 다가오는 일정</h2>
                <div class="calendar-item">
                    <span class="calendar-date">01/27 (월)</span>
                    <span>📦 정기점검</span>
                </div>
            </div>
        </div>

        <!-- 집중 포인트 (캘린더 바로 아래) -->
        <div class="focus-box">
            <h2>💡 오늘 집중 포인트</h2>
            <ul class="focus-list">
                <li>진행중 업무 우선 처리</li>
                <li>만기일 임박 업무 확인</li>
            </ul>
        </div>

        <!-- 프로젝트별 업무 -->
        <div class="project">
            <h2>프로젝트명</h2>
            <h3>🔴 진행중</h3>
            <!-- 24시간 이내 업데이트 예시 -->
            <div class="task">
                <div class="task-title">
                    <a href="URL">#1234 업무제목</a>
                    <span class="badge new">NEW</span>
                    <span class="update-time recent">3시간 전</span>
                </div>
                <div class="task-desc">업무 설명 요약</div>
                <div class="task-comment">💬 홍길동: 확인했습니다. 내일 반영 예정입니다. (3시간 전)</div>
                <div class="task-meta">만기일: MM/DD</div>
            </div>
            <!-- 7일 이내 업데이트 예시 -->
            <div class="task">
                <div class="task-title">
                    <a href="URL">#5678 다른업무</a>
                    <span class="update-time">2일 전</span>
                </div>
                <div class="task-desc">업무 설명</div>
                <div class="task-meta">만기일: MM/DD</div>
            </div>
        </div>

        <!-- 확인 필요 -->
        <div class="project">
            <h2>👀 확인 필요 (참조자 태그)</h2>
        </div>

        <!-- 기타 업무 (40일 이상 미갱신) -->
        <div class="project other-tasks">
            <h2>📦 기타 업무 (40일 이상 미갱신)</h2>
            <table class="other-task-table">
                <thead><tr><th>프로젝트</th><th>번호</th><th>제목</th><th>마지막 갱신</th></tr></thead>
                <tbody>
                    <tr>
                        <td>프로젝트명</td>
                        <td><a href="URL">#번호</a></td>
                        <td>업무 제목</td>
                        <td class="date">2024-11-15</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="generated-time">Generated at {생성시간}</div>
    </div>
</body>
</html>
```

### STEP 6: 브라우저에서 열기

```bash
open http://localhost:8765
```

## 입력값

$ARGUMENTS
