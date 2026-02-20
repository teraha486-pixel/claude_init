# Claude Code 설정

## ⚠️ 절대 준수 규칙 (실수 방지)

### Git 브랜치 규칙
```bash
# 커밋 전 반드시 확인!
git branch --show-current

# develop/master면 절대 커밋 금지!
# 반드시 feature/{작업명} 브랜치에서 작업
```

### 커밋 작업자 이름
- **작업자 이름: 근형** (복성 아님!)
- 커밋 메시지: `[근형] 작업내용`
- **Co-Authored-By 절대 금지!**

### docs 폴더 구조
- 관련 작업 문서는 **반드시 해당 폴더 안에** 생성
- 예: `docs/룸패킷_memberId_제거/xxx.md`
- docs/ 루트에 직접 파일 생성 금지

### 작업 연속성 유지
- 작업할 때마다 **위키 + md에 기록**
- 기록 필수: 브랜치명, 커밋 해시, 진행 상황, 남은 작업
- 세션 시작 시 위키에서 이전 작업 확인

---

## Maven 설치

빌드 스킬에서 사용하는 Maven을 설치합니다.

### 설치 위치
```
~/work/maven/apache-maven-3.6.3
```

### 설치 방법
```bash
# init 저장소에서 복사
cp -r ~/init/maven/apache-maven-3.6.3 ~/work/maven/
```

### 확인
```bash
/Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -version
```

### 참고
- 모든 빌드 스킬에서 이 경로의 Maven 사용
- homebrew Maven과 별도로 버전 고정 (3.6.3)

---

## 자동 승인 설정

매번 yes/no 승인 창이 뜨는 것을 비활성화하고 모든 작업 자동 승인되도록 설정

### 설정 파일
`~/.claude/settings.json`

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "alwaysThinkingEnabled": true
}
```

### 설정 항목 설명
- `bypassPermissions`: 모든 작업 자동 승인 (yes/no 창 비활성화)
- `alwaysThinkingEnabled`: ultrathink 항상 활성화 (extended thinking 모드)

### 설정 후
Claude Code 재시작 필요

---

## Ultrathink (Extended Thinking) 설정

복잡한 작업 시 더 깊은 사고를 위해 ultrathink 기본 활성화

### 설정 방법
`~/.claude/settings.json`에 `"alwaysThinkingEnabled": true` 추가

### 참고
- 최대 31,999 tokens까지 thinking에 사용 가능
- thinking tokens에 대해 비용 청구됨
- 단일 요청에만 적용하려면 메시지에 `ultrathink:` 키워드 사용
- 토글 단축키: `Option+T` (macOS) / `Alt+T` (Windows/Linux)

---

## 커스텀 슬래시 커맨드

### `/ut` - Ultrathink 단축 커맨드

매번 `ultrathink`를 타이핑하기 귀찮아서 `/ut`로 단축 커맨드 생성

### 설정 파일
`~/.claude/commands/ut.md`

```markdown
ultrathink

$ARGUMENTS
```

### 사용법
```
/ut 복잡한 문제를 분석해줘
```

→ 내부적으로 `ultrathink 복잡한 문제를 분석해줘`로 변환됨

### 참고
- 전역 커맨드: `~/.claude/commands/`
- 프로젝트 커맨드: `.claude/commands/`
- 세션 재시작 후 인식됨

---

## CLAUDE.md 파일 설명

### ~/.claude/CLAUDE.md
Claude Code가 세션 시작 시 자동으로 읽는 개인 작업 규칙 파일

포함 내용:
- 응답 언어 (한글)
- 빌드 순서
- 두레이 규칙
- 작업 완료 규칙
- 문서 구분

### 백업 위치
`~/init/claude/CLAUDE.md`

새 컴퓨터에서 설정 시:
```bash
mkdir -p ~/.claude
cp ~/init/claude/CLAUDE.md ~/.claude/CLAUDE.md
```

---

## 빌드 스킬 설정

프로젝트 빌드를 슬래시 커맨드로 등록하여 간편하게 실행

### 스킬 파일 위치
- 전역 스킬: `~/.claude/commands/`
- 백업 위치: `~/init/claude/commands/`

### 등록된 빌드 스킬

| 스킬 | 설명 | Java 버전 |
|------|------|-----------|
| `/build-betting-base` | betting_base 빌드 | Java 17 |
| `/build-poker-server` | hangame-poker-server 빌드 | Java 11 |
| `/build-gia-core` | gia-core 빌드 | Java 17 |
| `/build-gia-admin` | gia-poker-admin 빌드 | Java 17 |
| `/build-all` | 전체 프로젝트 순차 빌드 | - |

### 의존성 순서
```
betting_base → hangame-poker-server
gia-core → gia-poker-admin
```

### 새 컴퓨터에서 설정 시
```bash
mkdir -p ~/.claude/commands
cp ~/init/claude/commands/*.md ~/.claude/commands/
```

### 스킬 파일 예시 (`build-betting-base.md`)
```markdown
# betting_base 빌드

betting_base 프로젝트를 빌드합니다.

## 실행할 명령어

\`\`\`bash
cd /Users/nhn/work/betting_base && JAVA_HOME=$(/usr/libexec/java_home -v 17) ./mvnw clean compile install package -Dmaven.test.skip=true
\`\`\`

위 명령어를 실행하고 결과를 알려주세요.
```

### 참고
- 스킬 파일명이 커맨드명이 됨 (예: `build-all.md` → `/build-all`)
- 세션 재시작 후 인식됨
- `$ARGUMENTS`로 추가 인자 받을 수 있음

---

## 두레이 업무 조회 스킬

두레이 URL 또는 업무 ID로 업무 정보를 조회

### 스킬
| 스킬 | 설명 |
|------|------|
| `/dooray-task` | 두레이 업무 조회 |

### 지원하는 URL 형식
```
https://nhnent.dooray.com/project/tasks/{task_id}
https://nhnent.dooray.com/project/tasks/{task_id}#comment-{comment_id}
https://nhnent.dooray.com/task/view/tasks/{task_id}
https://nhnent.dooray.com/task/comment/{task_id}  (댓글 알림 링크)
또는 업무 ID만 입력
```

### 사용법
```
/dooray-task https://nhnent.dooray.com/project/tasks/4244450624484343354
/dooray-task 4244450624484343354
```

### 검색 대상 프로젝트 (순서대로)
| 순서 | 프로젝트명 | 프로젝트 ID |
|------|-----------|-------------|
| 1 | 웹보드개발랩-전체공유 | 2779708918315063486 |
| 2 | pc포커-bts | 1567704068379919418 |
| 3 | 포커클래식-QA | 2378020467797929507 |
| 4 | 한게임포커통합-업데이트관리 | 3287834850785742288 |

### 기능
- URL에서 업무 ID 자동 추출
- 댓글 ID가 포함된 경우 해당 댓글 하이라이트
- 업무 정보 요약 (제목, 상태, 담당자, 본문)

---

## 클라이언트 코드 분석 규칙

서버 작업 시 클라이언트 영향도 함께 분석하기 위한 규칙

### 클라이언트 코드 경로
```
~/work/hangame-poker-unity
```

### 적용 시점
- `/wiki` 또는 `/do` 스킬로 서버 작업 시
- 패킷 변경, API 변경 등 클라이언트 영향 가능한 작업 시
- 클라이언트 가이드 문서 작성 시

### 작업 흐름
```
1. 서버 작업 전 클라이언트 코드 git pull
   cd ~/work/hangame-poker-unity && git pull

2. 서버 코드 분석 + 클라이언트 코드 영향도 분석
   - 패킷 변경 → 클라에서 해당 패킷 사용하는 곳 검색
   - 필드 추가/제거 → 클라에서 해당 필드 사용하는 곳 검색

3. 위키 문서 작성 시 클라이언트 수정 가이드 포함
   - 파일 경로
   - 메서드/함수명
   - 줄 번호
   - 구체적인 수정 내용
```

### 주요 클라이언트 파일 (참고)
| 파일 | 용도 |
|------|------|
| `UserData.cs` | 유저 정보 (GetMemberId 등) |
| `PlayerControl.cs` | 플레이어 식별/관리 |
| `GameDataManager.cs` | 게임 데이터 관리 |
| `EventBase.cs` | 이벤트 처리 베이스 |

### 주의사항
- **클라이언트 코드는 절대 수정 금지** (분석만)
- 클라이언트 CLAUDE.md 참조: `~/work/hangame-poker-unity/Poker/CLAUDE.md`

---

## 두레이 위키 페이지 관리 규칙

### 위키 정보
| 항목 | 값 |
|------|-----|
| 위키 ID | `3051057878725260241` |
| 기본 페이지 | claude code (`4248918788553579171`) |
| URL 형식 | `https://nhnent.dooray.com/wiki/3051057873186173159/{page_id}` |

### 새 페이지 생성 시 필수 작업

**중요**: 새 위키 페이지를 생성할 때마다 반드시 `claude code` 페이지 본문에 링크 추가

```markdown
# 작업 순서
1. 새 페이지 생성 (parent_page_id: 4248918788553579171)
2. claude code 페이지 본문에 새 페이지 링크 추가
```

### claude code 페이지 본문 형식

```markdown
# Claude Code 작업 위키

Claude Code로 진행한 작업들의 문서 모음입니다.

## 하위 페이지 목록

| 작업명 | 링크 |
|--------|------|
| {작업명1} | [바로가기](https://nhnent.dooray.com/wiki/3051057873186173159/{page_id1}) |
| {작업명2} | [바로가기](https://nhnent.dooray.com/wiki/3051057873186173159/{page_id2}) |
...
```

### 이유
- 즐겨찾기에서 claude code 페이지만 보임
- 하위 페이지 탐색이 불편함
- 본문에 링크가 있어야 빠르게 접근 가능
