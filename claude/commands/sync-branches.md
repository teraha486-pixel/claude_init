# 브랜치 최신화 스킬

로컬 feature 브랜치들을 메인 브랜치 기준으로 최신화합니다.

## 사용 방법

```
/sync-branches [프로젝트명]
```

예시:
- `/sync-branches gia` - gia 프로젝트 브랜치 최신화
- `/sync-branches hangame-poker-server` - 한게임포커서버 브랜치 최신화
- `/sync-branches hps` - hangame-poker-server 약칭
- `/sync-branches all` - 모든 프로젝트 최신화
- `gia 최신화해줘` - 자연어로도 가능

## 프로젝트별 설정

| 프로젝트 | 경로 | 메인 브랜치 |
|----------|------|-------------|
| gia | `/Users/nhn/work/gia` | alpha |
| hangame-poker-server | `/Users/nhn/work/hangame-poker-server` | develop |

## 실행 흐름

### STEP 1: 로컬 브랜치 목록 조회 (필수!)

**⚠️ 중요: 위키가 아닌 실제 로컬 git 브랜치 목록을 확인해야 합니다!**

```bash
cd /Users/nhn/work/{프로젝트}
git branch | grep feature
```

이 명령으로 실제 로컬에 있는 모든 feature 브랜치를 확인합니다.

**예시 출력:**
```
  feature/auto-betting-last-round
  feature/coupon-api
  feature/remove-memberid-from-room-packets
  feature/seven-poker-showdown-time-reduce
```

### STEP 1-1: 위키에서 브랜치별 작업 내용 확인 (conflict 해결 참고용)

**위키 정보:**
- wiki_id: `3051057878725260241`
- 기본 페이지: claude code (`4248918788553579171`)

```
get_child_wiki_list(wiki_id, parent_page_id)
get_wiki_page_by_id(page_id)
```

위키는 conflict 발생 시 작업 내용을 파악하기 위한 참고 자료로만 사용합니다.
- 각 브랜치의 작업 목적, 변경 파일, API 변경사항 등 확인
- conflict 해결 시 어떤 코드를 유지해야 할지 판단

### STEP 2: 메인 브랜치 최신화

```bash
cd /Users/nhn/work/{프로젝트}
git checkout {메인_브랜치}
git pull origin {메인_브랜치}
```

### STEP 3: 각 작업 브랜치 최신화

**STEP 1에서 찾은 모든 로컬 feature 브랜치**에 대해:

```bash
cd /Users/nhn/work/{프로젝트}
git checkout {작업_브랜치}
git merge {메인_브랜치}
```

**Conflict 발생 시:**
1. **STEP 1-1**: 위키에서 해당 브랜치의 작업 내용 확인
2. Conflict 파일 내용 분석
3. 작업 내용 기반으로 conflict 해결 (작업 브랜치 변경사항 우선 유지)
4. git add + git commit

**Conflict 없으면:**
- 자동 머지 완료 메시지 출력

### STEP 4: 결과 요약

각 브랜치별 결과를 표로 정리:

| 브랜치 | 상태 | Conflict 파일 | 변경 파일 수 |
|--------|------|----------------|-------------|
| feature/coupon-api | ✅ 완료 | 1개 (해결완료) | 149개 |
| feature/game-money-api | ✅ 완료 | 없음 | 141개 |
| ... | ... | ... | ... |

## 예외 처리

### 1. 이미 최신인 경우
- "Already up to date" 메시지 표시

### 2. Conflict 해결 실패
- 실패한 브랜치 표시
- 사용자에게 수동 해결 안내

### 3. Uncommitted changes 있는 경우
- 해당 브랜치 스킵
- 메시지: "⚠️ {브랜치명}에 uncommitted changes가 있습니다. 스킵합니다."

## 주의사항

1. **작업 중인 변경사항 확인**
   - 최신화 전 각 브랜치에서 `git status` 확인
   - uncommitted changes 있으면 경고 후 스킵

2. **메인 브랜치 직접 작업 금지**
   - alpha, develop 브랜치는 항상 clean 상태 유지

3. **Conflict 해결 원칙**
   - 작업 브랜치의 변경사항 우선 유지
   - 위키 기록(STEP 1-1) 참고해서 작업 의도 파악

4. **실제 로컬 브랜치 기준**
   - 반드시 `git branch` 명령으로 실제 로컬 브랜치 확인
   - 위키는 참고용으로만 사용 (conflict 해결 시)

## 출력 예시

```
## hangame-poker-server 브랜치 최신화

### STEP 1: 로컬 브랜치 목록 조회
발견된 feature 브랜치 (4개):
  - feature/auto-betting-last-round
  - feature/coupon-api
  - feature/remove-memberid-from-room-packets
  - feature/seven-poker-showdown-time-reduce

### STEP 2: develop 브랜치 업데이트
✅ develop: Already up to date

### STEP 3: 작업 브랜치 최신화
🔄 feature/auto-betting-last-round
  ✅ Already up to date

🔄 feature/coupon-api
  ✅ Already up to date

🔄 feature/remove-memberid-from-room-packets
  ✅ Already up to date

🔄 feature/seven-poker-showdown-time-reduce
  ✅ 자동 머지 완료
  📊 3개 파일 변경

### 요약
| 브랜치 | 상태 | Conflict | 변경 파일 |
|--------|------|----------|----------|
| feature/auto-betting-last-round | ✅ | 없음 | 0개 (이미 최신) |
| feature/coupon-api | ✅ | 없음 | 0개 (이미 최신) |
| feature/remove-memberid-from-room-packets | ✅ | 없음 | 0개 (이미 최신) |
| feature/seven-poker-showdown-time-reduce | ✅ | 없음 | 3개 |

✅ 총 4개 브랜치 최신화 완료!
```

## MCP 도구

- `mcp__dooray-mcp__get_child_wiki_list` - 위키 페이지 목록 조회
- `mcp__dooray-mcp__get_wiki_page_by_id` - 위키 페이지 내용 조회

## 입력값

$ARGUMENTS
