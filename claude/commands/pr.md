# PR 리뷰 검토 스킬

PR에 달린 코드 리뷰를 조회하고, 각 항목의 수용 여부를 판단합니다.
수정이 필요한 항목은 코드를 수정하고, 과한 태클은 사유와 함께 스킵합니다.

## 사용법

```
/pr {PR_URL}
/pr {PR_URL} 리뷰만 봐줘
/pr {PR_URL} 수정까지 해줘
```

- URL만 주면: 리뷰 분석 + 수용 여부 판단 + 정리 (수정은 사용자 확인 후)
- "리뷰만": 분석/판단만 하고 수정 안 함
- "수정까지": 수정 필요한 것 자동 수정 + 빌드까지

## 지원 URL 형식

```
https://github.nhnent.com/{org}/{repo}/pull/{number}
https://github.nhnent.com/{org}/{repo}/pull/{number}/files
https://github.nhnent.com/{org}/{repo}/pull/{number}#discussion_r{id}
```

## 프로젝트 매핑

| GitHub 저장소 | 로컬 경로 | 빌드 스킬 |
|--------------|----------|-----------|
| hangame-poker/gia | `/Users/nhn/work/gia` | `/build-gia-core` → `/build-gia-admin` |
| hangame-poker/hangame-poker-server | `/Users/nhn/work/hangame-poker-server` | `/build-betting-base` → `/build-poker-server` |
| hangame-poker/betting_base | `/Users/nhn/work/betting_base` | `/build-betting-base` |

## 실행 흐름

### Step 1: PR 정보 파싱

URL에서 추출:
```
org = URL의 {org} 부분
repo = URL의 {repo} 부분
pr_number = URL의 {number} 부분
```

### Step 2: PR 기본 정보 조회

```bash
GH_HOST=github.nhnent.com gh pr view {pr_number} --repo {org}/{repo} --json title,body,headRefName,baseRefName,state,files
```

### Step 3: 리뷰 코멘트 조회

```bash
# 리뷰 목록
GH_HOST=github.nhnent.com gh api repos/{org}/{repo}/pulls/{pr_number}/reviews

# 리뷰 코멘트 (코드에 달린 인라인 코멘트)
GH_HOST=github.nhnent.com gh api repos/{org}/{repo}/pulls/{pr_number}/comments
```

**코멘트가 없으면**: "리뷰 코멘트가 없습니다" 출력 후 종료

### Step 4: 리뷰 항목별 분석

각 리뷰 코멘트에 대해:

1. **해당 파일/코드 확인** - 로컬에서 실제 코드 읽기
2. **맥락 파악** - 리뷰어가 지적한 부분의 전후 코드, 기존 코드 패턴 확인
3. **수용 여부 판단** - 아래 기준으로 판단

### Step 5: 수용 여부 판단 기준

**수정 필요 (수용):**
- 실제 버그 또는 런타임 에러 가능성
- NPE, 리소스 누수, 동시성 이슈 등 실질적 문제
- 보안 취약점
- 데이터 정합성 문제
- 명백한 로직 오류

**스킵 (과한 태클):**
- 기존 코드와 동일한 패턴인데 새 코드만 지적
- 스타일/네이밍 수준의 제안 (팀 컨벤션 위반 아닌 경우)
- 이론적으로는 맞지만 현재 컨텍스트에서 문제 안 되는 것
- Spring/JPA 등 프레임워크 기본 동작을 모르고 하는 지적
- 성능 이슈지만 실제 트래픽에서 문제 없는 수준
- 과도한 방어적 코딩 요구

**판단 보류:**
- 비즈니스 로직 관련으로 사용자 확인 필요
- 기존 코드를 모르면 판단 불가한 것

### Step 6: 결과 정리

아래 형식으로 정리:

```markdown
## PR 리뷰 검토 결과

**PR**: #{pr_number} {title}
**브랜치**: {head} → {base}
**리뷰 항목**: {총 N건}

---

### 수정 필요 ({n}건)

#### 1. [{파일명}:{줄번호}] {요약}
- **리뷰 내용**: {리뷰어 코멘트 요약}
- **판단**: 수정 필요 - {사유}
- **조치**: {수정 내용 또는 수정 예정}

---

### 스킵 - 과한 태클 ({n}건)

#### 1. [{파일명}:{줄번호}] {요약}
- **리뷰 내용**: {리뷰어 코멘트 요약}
- **판단**: 스킵 - {사유}

---

### 판단 보류 ({n}건)

#### 1. [{파일명}:{줄번호}] {요약}
- **리뷰 내용**: {리뷰어 코멘트 요약}
- **확인 필요**: {무엇을 확인해야 하는지}

---

### 요약

| # | 항목 | 파일 | 판단 | 사유 |
|---|------|------|------|------|
| 1 | {요약} | {파일} | 수정/스킵/보류 | {한줄 사유} |
```

### Step 7: 코드 수정 (수정 모드일 때만)

"수정까지 해줘" 또는 사용자가 수정 승인한 경우:

1. "수정 필요" 항목만 코드 수정
2. **빌드 테스트** - 해당 프로젝트의 `/build-*` 스킬 호출
3. 빌드 성공 확인
4. 수정 결과를 Step 6 결과에 추가

**빌드 실패 시**: 에러 분석 후 수정, 재빌드

### Step 8: 커밋 (사용자 확인 후)

수정이 완료되면 사용자에게 커밋 여부 확인:
- 커밋 시 `/commit` 스킬 활용
- 커밋 메시지: `[태양] fix: PR 리뷰 반영 - {수정 요약}`

## 주의사항

- **gh CLI 환경변수**: 모든 gh 명령에 `GH_HOST=github.nhnent.com` 필수
- **로컬 브랜치 확인**: 수정 전 PR의 head 브랜치로 체크아웃 되어있는지 확인
- **기존 코드 패턴 확인**: 리뷰 지적이 기존 코드에도 해당되는지 반드시 확인 (기존 코드와 동일하면 스킵 근거)
- **빌드는 반드시 `/build-*` 스킬 사용**
- **수정 범위**: 리뷰에서 지적된 부분만 수정, 추가 리팩토링 금지

## 입력값

$ARGUMENTS
