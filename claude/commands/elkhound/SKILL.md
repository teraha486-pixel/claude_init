---
name: elkhound
description: "AI ElkHound 개인 프로젝트 작업 자동화. ELK 에러 추적 AI 사냥개 시스템 개발. 'elkhound', '엘크하운드' 언급 시 사용. 세션 시작 시 위키 작업히스토리→CLAUDE.md→TODO→docs에서 진행상황 확인, 기획 업데이트, 코드 작업, 코드 리뷰, 유닛테스트, 빌드, 자동 커밋/푸시, 위키 히스토리 기록을 수행."
---

# AI ElkHound

> ELK에서 에러를 추적하는 AI 사냥개. 개인 프로젝트.

## 프로젝트 정보

| 항목 | 값 |
|------|---|
| **프로젝트명** | AI ElkHound |
| **로컬 경로** | `/Users/nhn/work/ai-elkhound` |
| **두레이 업무** | https://nhnent.dooray.com/project/tasks/4254453353438866051 |
| **두레이 프로젝트** | 웹보드개발랩-전체공유 (`2779708918315063486`) |
| **기술 스택** | Python 3.10+, FastAPI, SQLite, Claude API, React |
| **TODO** | `/Users/nhn/work/ai-elkhound/docs/TODO.md` |

## 위키 정보 (작업 히스토리 저장소)

| 항목 | 값 |
|------|---|
| **wiki_id** | `3051057878725260241` |
| **상위 페이지** | `AI 에러 로그 자동화` (`4254443711291635226`) |
| **작업 히스토리** | `4265333693351916871` |
| **두레이_댓글_초안** | `4254444230506120658` |
| **업무 계획서** | `4254487175692725218` |
| **AI 개발 가이드** | `4254494792071523146` |
| **URL 패턴** | `https://nhnent.dooray.com/wiki/3051057873186173159/{page_id}` |

## 핵심 설계 원칙 (항상 고려!)

### 1. Docker 기반 실행
- **로컬 환경 의존 없이** Docker로 실행
- `docker compose up`으로 전체 시스템 기동
- 개발/프로토타입도 Docker 환경에서 동작 확인

### 2. AI API 추상화 (프로바이더 패턴)
- **현재**: Claude API (프로토타입)
- **미래**: GPT, Gemini 등 다른 AI API로 전환 또는 병행
- `analyzer/ai_provider.py`에 추상 인터페이스 정의
- 각 프로바이더는 `analyzer/providers/` 아래에 구현
- **새 AI 기능 추가 시 반드시 추상 인터페이스를 거칠 것**

### 3. 프로토타입 → 서비스 전환 고려
- 프로토타입은 근형+AI가 같이 만들지만, 서비스 시에는 API 기반으로 전환
- 설정값은 환경변수로 관리 (.env → Docker env)
- DB, API 클라이언트 등 외부 의존성은 인터페이스로 추상화
- 하드코딩 금지, 설정 가능하게 설계

## 프로젝트 규칙 참조

**프로젝트 전용 규칙은 repo에 포함되어 있음:**
- **규칙**: `/Users/nhn/work/ai-elkhound/.claude/CLAUDE.md`
- **TODO**: `/Users/nhn/work/ai-elkhound/docs/TODO.md` (마스터 태스크 리스트)
- **기획 문서**: `/Users/nhn/work/ai-elkhound/docs/`

## 세션 시작 시 반드시 읽기

1. **위키 작업 히스토리 조회** → 이전 작업 이어서 진행
   ```
   get_child_wiki_list(wiki_id="3051057878725260241", parentPageId="4254443711291635226")
   → "작업 히스토리" 페이지 찾기 → 본문 읽기
   ```
2. `/Users/nhn/work/ai-elkhound/.claude/CLAUDE.md` → 프로젝트 규칙
3. `/Users/nhn/work/ai-elkhound/docs/TODO.md` → 마스터 태스크 + 의사결정 히스토리
4. `/Users/nhn/work/ai-elkhound/docs/00_프로젝트_개요.md` → Phase/상태/히스토리
5. `git -C /Users/nhn/work/ai-elkhound pull` (remote 설정되어 있으면)
6. 현재 브랜치 확인 (`git -C /Users/nhn/work/ai-elkhound branch --show-current`)

## 워크플로우

### 작업 진행 (전체 흐름)

```
1. 세션 시작: 위키 작업히스토리 + TODO + docs 확인
   → 이전 작업 상태 파악, 다음 작업 식별

2. 사용자에게 현재 상태 + 다음 작업 후보 제시
   → "현재 Phase 1의 1.3까지 완료, 다음은 1.4 ELK 연동인데 진행할까요?"

3. 기획 확인/업데이트 (필요 시)
   → 관련 docs 읽기, 추가 요구사항 반영
   → 기획 변경 시 docs/ 업데이트 후 별도 커밋

4. 브랜치 확인 + 워크트리 판단
   → git branch --show-current
   → develop/main 직접 커밋 금지!
   → feature/{기능명} 브랜치에서만 작업

5. 코드 작성/수정
   → 기존 코드 패턴 참고
   → 기획 의견 있으면 적극 제시

6. 유닛테스트 업데이트 + 실행
   → cd /Users/nhn/work/ai-elkhound && python -m pytest tests/
   → 테스트 ALL PASS 확인 → 사용자에게 결과 보고

7. 빌드/실행 테스트
   → cd /Users/nhn/work/ai-elkhound && python -m py_compile {파일}
   → FastAPI 서버: uvicorn api.main:app
   → 에러 시 수정 후 재시도

8. 코드 리뷰 (자동)
   → 변경된 코드에 대해 자동 코드 리뷰
   → 보안, 에러 처리, 성능, 코드 스타일 체크
   → 심각한 이슈 발견 시 자동 수정

9. 자동 커밋
   → [근형] {type}: {설명}
   → Co-Authored-By 절대 금지!

10. 자동 푸시 + gc (remote 설정 시)
    → git push && git reflog expire --expire=now --all && git gc --prune=now

10-1. PR 생성 (feature 브랜치 작업 시)
    → gh pr create --base develop (또는 적절한 base)
    → PR URL 기록 → 이후 두레이 업무/위키에 반드시 포함

11. docs 업데이트
    → 00_프로젝트_개요.md 히스토리
    → TODO.md 완료 항목 체크 + 의사결정 히스토리

12. 위키 작업 히스토리 업데이트 (댓글로 기록)
    → 작업 내역 댓글: 날짜, 작업명, 커밋 해시, 변경 요약
    → 본문 테이블 상태 업데이트 (예정→진행→완료)
    → ⚠️ 주간보고 댓글은 자동으로 남기지 않음! 사용자가 필요한 것만 직접 기록

13. 다음 작업 추천
    → TODO에서 다음 [AI] 작업 확인
    → 우선순위 정렬하여 제시
    → "다음에 뭐 할까요?" 형식으로 제안
```

### 기획 의견 제시 (적극적으로!)

코드 작업뿐 아니라 기획에 대한 의견도 적극 제시:
- **기술 선택**: DB 종류, 프레임워크, 라이브러리
- **아키텍처**: 모듈 분리, API 설계, 데이터 흐름
- **UI/UX**: 대시보드 레이아웃, 사용성
- **배포 방식**: 로컬 Mac / 사내 서버 / Docker / 웹페이지
- **추가 기능 제안**: 알림 방식, 통계 시각화, 보고서 형식
- 의견 제시 후 사용자 결정 → TODO.md 의사결정 히스토리에 기록

### 코드 리뷰 (작업 완료 후 자동)

```markdown
## 코드 리뷰 결과 (중요도 기준 정렬)

### 🔴 반드시 수정
- [파일:줄번호] 이슈 설명 + 권장 수정 코드

### ⚠️ 권장 사항
- [파일:줄번호] 이슈 설명

### ✅ 잘한 부분
- 긍정적 피드백
```

### 유닛테스트 규칙 (필수)

- **코드 변경 시 반드시**: 테스트 추가/수정 → 실행 → ALL PASS → 보고
- **각 작업 단계 완료 시 테스트 실행** → 실패하면 수정 후 재실행
- **테스트 실패 상태에서 커밋 금지**
- 테스트 실행: `cd /Users/nhn/work/ai-elkhound && python -m pytest tests/ -v`
- 결과 보고 형식:
  - 전체 통과: "✅ {N}개 테스트 전부 통과"
  - 실패: "❌ {실패수}/{전체수} 실패" + 실패 항목 리스트

## 위키 작업 히스토리 관리

### 본문 (테이블 형식)
작업 히스토리 페이지 본문에 전체 진행 상황 테이블 유지:

```markdown
| # | 작업 | 상태 | 설명 | 커밋 | 날짜 |
|---|------|------|------|------|------|
| 1 | 프로젝트 초기 세팅 | ✅ 완료 | Git repo, docs, CLAUDE.md | `6ed64d6` | 2026-02-11 |
| 2 | Phase 1.1 프로젝트 구조 | 🔵 진행 | Python 구조, requirements | - | - |
| 3 | Phase 1.2 DB 스키마 | ⬜ 예정 | SQLite schema, models | - | - |
```

### 댓글 (작업 기록)
각 작업 완료 시 댓글로 상세 기록:

```markdown
## {날짜} 작업 내역
### {작업명}
- **내용**: {2~3줄 요약}
- **커밋**: `{해시}` - {설명}
- **브랜치**: {브랜치명}
- **PR**: {PR URL} (있으면 반드시 포함)
- **다음 작업**: {다음에 할 일}
```

### 두레이 업무 생성/업데이트 시 PR 링크 필수
- **두레이 업무를 만들거나 댓글을 달 때 PR 링크를 반드시 포함**
- PR이 있으면 업무 본문 또는 댓글에 `PR: {URL}` 형식으로 추가
- 두레이_댓글_초안 위키에도 PR 링크 포함

## 브랜치 전략
```
main ←── develop ←── feature/{기능명}

main:      안정 버전 (절대 직접 커밋 금지)
develop:   통합 브랜치 (feature에서 머지)
feature/*: 실제 작업 (여기서만 커밋)
```

## 커밋 규칙
```
[근형] {type}: {설명}
```
type: `feat` | `fix` | `refactor` | `style` | `docs` | `chore`
**Co-Authored-By 절대 금지! 주간보고 댓글은 자동으로 남기지 않음 (사용자가 위키 히스토리에서 필요한 것만 직접 기록)**

## 입력값

$ARGUMENTS
