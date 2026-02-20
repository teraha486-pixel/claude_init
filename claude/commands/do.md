# 작업 자동화 스킬

두레이 업무 기반으로 전체 작업 워크플로우를 자동화합니다.
위키가 작업 히스토리 DB 역할을 하며, 이전 작업 참조/롤백도 지원합니다.

## 위키 정보 (히스토리 저장소)
- **wiki_id**: `3051057878725260241`
- **기본 페이지**: claude code (`4248918788553579171`)
- **URL**: `https://nhnent.dooray.com/wiki/3051057873186173159/{page_id}`

## 지원 프로젝트
| 프로젝트 | 경로 | Java | 빌드 명령 |
|----------|------|------|-----------|
| hangame-poker-server | /Users/nhn/work/hangame-poker-server | 11 | `mvn -B clean compile install -DskipTests -Plocal` |
| gia | /Users/nhn/work/gia | 17 | gia-core 먼저 → gia-poker-admin |
| betting_base | /Users/nhn/work/betting_base | 17 | `./mvnw compile -DskipTests` |

## BMAD 코드베이스 분석 문서 (필수 참조)

각 프로젝트에 BMAD 풀스캔 결과가 있으며, **코드 작업 전 반드시 참조**한다.
사용자가 별도로 BMAD를 언급하지 않아도 **항상 자동으로 활용**할 것.

### 프로젝트별 BMAD 문서 경로

| 프로젝트 | 프레임워크 | 분석 문서 |
|----------|-----------|----------|
| hangame-poker-server | `_bmad/` | `docs/bmad/` |
| gia | `_bmad/` | `docs/bmad/` |
| betting_base | `_bmad/` | - |

### 활용 규칙
1. **코드 수정 전**: 해당 프로젝트의 `docs/bmad/bmad-index.md`부터 읽어서 관련 문서 파악
2. **아키텍처 파악**: `bmad-architecture.md`, `bmad-integration-architecture.md`
3. **데이터 모델 확인**: `bmad-data-models.md` (Entity, 테이블 구조)
4. **컴포넌트 위치 확인**: `bmad-component-inventory.md`, `bmad-source-tree-analysis.md`
5. **API 확인**: `bmad-api-contracts.md` (REST API, Protocol Buffer)
6. **코드 패턴 참고**: `bmad-development-guide.md` (빌드, 실행, 환경)
7. 관련 BMAD 문서를 먼저 읽고 코드 구조를 파악한 뒤 작업 시작

### 활용 시점
- **새 작업**: 두레이 업무 분석 후, 코드 수정 전에 BMAD 문서로 영향 범위 파악
- **기존 작업 계속**: 이전 작업과 관련된 BMAD 문서 재확인
- **코드 리뷰**: BMAD 아키텍처/패턴과 일관성 있는지 검증

---

## 사용 방법

### 1. 새 작업 시작
```
/do https://nhnent.dooray.com/project/tasks/1234567890 작업해줘
/do 두레이URL 쿠폰 API MSA 전환 작업
```

### 2. 기존 작업 계속
```
/do coupon-api 계속 작업해줘
/do coupon-api 커밋 추가해줘
```

### 3. 롤백/되돌리기
```
/do coupon-api 롤백해줘
/do gia coupon-api 작업 롤백해줘
```

### 4. 작업 목록 조회
```
/do 목록
/do 작업목록
```

## ⚠️ 절대 준수 규칙

### 커밋 전 필수 확인
```bash
# 1. 브랜치 확인 (develop/master면 절대 커밋 금지!)
git branch --show-current

# 2. feature 브랜치 아니면 작업 브랜치로 이동
git checkout feature/{작업명}
```

### 작업자 이름
- **커밋 메시지: `[근형]`** (복성 아님!)

### docs 폴더 규칙
- 관련 작업 문서는 **반드시 해당 폴더 안에** 생성
- 예: `docs/룸패킷_memberId_제거/xxx.md`
- docs/ 루트에 직접 파일 생성 금지

### 작업 연속성
- 작업할 때마다 **위키 + md에 기록**
- 기록 필수: 브랜치명, 커밋 해시, 진행 상황, 남은 작업
- 세션 시작 시 위키에서 이전 작업 확인

---

## 워크플로우 상세

### [새 작업] 전체 흐름
```
1. 두레이 업무 조회 (dooray_project_get_post)
   - 업무 제목, 내용, 담당자 파악
   - 요구사항 분석

2. 브랜치 확인 + 워크트리 판단 ⚠️ 중요
   - `git branch --show-current`로 현재 브랜치 확인
   - develop/master면 절대 커밋 금지!
   - 현재 브랜치 ≠ 타겟 브랜치(위키/두레이에서 확인)인 경우:
     → 사용자에게 질문: "지금 {현재브랜치}에서 작업 중인 거 있으세요?
        워크트리로 따로 빼서 할까요, 브랜치 전환해도 될까요?"
     → 워크트리 선택 시: `git worktree add ../{프로젝트}-{작업명} {타겟브랜치}`
     → 브랜치 전환 선택 시: 기존처럼 checkout
   - 현재 브랜치 = 타겟 브랜치면 바로 진행
   - 타겟 브랜치 없으면 feature/{작업명} 생성

3. BMAD 문서 참조 + 코드 수정
   - docs/bmad/ 문서로 관련 아키텍처/컴포넌트/데이터 모델 파악
   - 요구사항 기반 코드 작성/수정
   - 기존 코드 패턴 참고

4. 빌드 테스트 (/build-* 스킬 사용!)
   - 반드시 /build-* 스킬을 호출하여 빌드
   - 에러 발생 시 수정 후 재빌드

5. 코드 리뷰 (자동)
   - 변경된 코드에 대해 자동 코드 리뷰 수행
   - NPE, 페이징, 트랜잭션, 보안 등 체크
   - 심각한 이슈 발견 시 자동 수정 후 재빌드

6. docs/ 작업 기록 생성
   - 파일명: {기능명}_{작업내용}.md
   - 내용: 두레이 링크, API 목록, 수정 파일, 커밋 해시

7. 커밋
   - 의미있는 커밋 메시지 작성
   - Co-Authored-By 절대 금지!

8. 위키 생성/업데이트 (/wiki 스킬 활용)
   - 작업 페이지 구조 생성
   - 프로젝트 문서 경로, 브랜치, 커밋 이력 기록
   - 두레이_댓글_초안에 댓글로 진행상황 기록
   - 코드 리뷰 결과도 위키에 기록

9. ⚠️ 주간보고 위키 댓글 남기기 (절대 빠뜨리지 말 것!)
   - 이 단계를 건너뛰면 안 됨! 8번까지 했으면 반드시 9번도 실행!
   - get_child_wiki_list(wiki_id="3051057878725260241", parentPageId="4250340996968691291")
   - 🚨 **주 경계: 금~목이 한 주!** 오늘 기준 다음 목요일 날짜 페이지에 기록 (오늘이 목요일이면 오늘)
     예: 금 2/13 → 2/19 페이지, 화 2/17 → 2/19 페이지, 목 2/19 → 2/19 페이지
   - 내용: 작업명, 커밋 해시, 수정 요약 (2~5줄), 관련 위키/업무 링크
   - ⚠️ 카테고리 분류 필수! H2 제목에 `(N월반영)`, `(기타업무)`, `(인프라)` 등 표기
     → 웹보드개발랩-전체공유(2779708918315063486)에서 "반영업무" 검색
     → 해당 업무가 월별 반영업무 하위업무인지 확인
     → 하위업무에 없지만 반영 대상이면 사용자에게 하위업무 추가 제안
     → 판단 어려우면 기존 댓글 패턴 참고

10. ⚠️ 완료 보고 (절대 누락 금지!)
   - 모든 단계가 끝나면 번호 매겨서 완료 내역을 사용자에게 보고
   - 사용자가 묻기 전에 먼저 알려줘야 함!
   - 보고 형식 예시:
     1. 빌드 성공 (hangame-poker-server)
     2. 코드 리뷰 완료 (이슈 없음 / N건 자동 수정)
     3. docs 작성: docs/{폴더}/{파일명}.md
     4. 커밋: `해시` - 메시지 → 레포: {레포명}, 브랜치: {브랜치명}
     5. 위키 작성: [페이지명](URL)
     6. 주간보고 댓글: [페이지명](URL)
   - 커밋/푸시는 반드시 레포명 + 브랜치명 명시
   - 해당 없는 항목은 생략, 있는 건 절대 누락 금지
```

### [기존 작업 계속] 흐름
```
1. 위키에서 작업 정보 조회
   - 브랜치명, 프로젝트, 이전 커밋 확인

2. 해당 브랜치 체크아웃

3. 추가 작업 수행

4. 빌드 테스트

5. docs/ 문서 업데이트

6. 커밋

7. 위키 커밋 이력 업데이트

8. 주간보고 페이지에 오늘 작업 댓글 남기기

9. ⚠️ 완료 보고 (절대 누락 금지!)
   - 번호 매겨서 완료 내역 보고 (커밋/푸시는 레포명+브랜치명 필수)
```

### [롤백] 흐름
```
1. 위키에서 작업 정보 조회
   - 커밋 해시, 브랜치 확인

2. git revert 또는 reset 수행

3. 빌드 테스트

4. 롤백 커밋

5. 위키에 롤백 이력 추가

6. 주간보고 페이지에 롤백 작업 댓글 남기기

7. ⚠️ 완료 보고 (절대 누락 금지!)
   - 번호 매겨서 완료 내역 보고 (커밋/푸시는 레포명+브랜치명 필수)
```

## 빌드 명령어 상세

⚠️ **반드시 `/build-*` 스킬을 호출하여 빌드할 것!** 직접 명령어 작성 금지!

빌드 시 아래 명령어 대신 **스킬 호출**을 사용:
- gia: `/build-gia-core` → `/build-gia-admin` (순서 필수)
- hangame-poker-server: `/build-betting-base` → `/build-poker-server` (순서 필수)
- 전체: `/build-all`

### 참고용 명령어 (`-f` 옵션으로 cd 불필요)

#### hangame-poker-server
```bash
JAVA_HOME=$(/usr/libexec/java_home -v 11) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/hangame-poker-server/pom.xml -B clean compile install -DskipTests -Plocal
```

#### gia (순서 중요)
```bash
# 1. gia-core 먼저
JAVA_HOME=$(/usr/libexec/java_home -v 17) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/gia/gia-core/pom.xml clean compile install -DskipTests

# 2. gia-poker-admin
JAVA_HOME=$(/usr/libexec/java_home -v 17) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/gia/gia-poker-admin/pom.xml clean compile install -DskipTests
```

#### betting_base
```bash
JAVA_HOME=$(/usr/libexec/java_home -v 11) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/betting_base/pom.xml clean compile install -DskipTests
```

## 커밋 메시지 규칙

⚠️ **작업자 이름: 근형** (복성 아님!)
⚠️ **Co-Authored-By 절대 금지!**

```
[근형] {type}: {간단한 설명}

- 상세 내용 1
- 상세 내용 2
```

**type 종류:**
- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서
- `chore`: 설정, 빌드

**커밋 전 체크리스트:**
1. `git branch --show-current` - develop/master 아닌지 확인
2. 작업자 이름 `[근형]` 맞는지 확인
3. docs 파일 올바른 폴더에 있는지 확인
4. **Co-Authored-By 없는지 확인**

**push 후 필수 작업:**
```bash
# gc로 고아 커밋 정리 (안하면 느려짐)
git reflog expire --expire=now --all && git gc --prune=now
```

## docs/ 문서 템플릿
```markdown
# {기능명} {작업내용}

## 업무 정보
- **두레이**: {URL}
- **작업일**: {날짜}
- **목적**: {간단 설명}

## 수정된 파일 목록
- `path/to/file1.java` - 변경 내용
- `path/to/file2.java` - 변경 내용

## API 변경 (해당 시)
| API | Method | Endpoint | 설명 |
|-----|--------|----------|------|

## 변경 이력
| 날짜 | 작업자 | 커밋 | 내용 |
|------|--------|------|------|
```

## 코드 리뷰 (작업 완료 후 자동 수행)

작업이 완료되면 **변경된 코드를 분석하여 자동 코드 리뷰를 수행**합니다.

### 리뷰 방식
- 고정된 체크리스트가 아닌, **해당 코드의 성격과 맥락에 맞춰** 리뷰
- API면 API 관점, 쿼리면 쿼리 관점, 비즈니스 로직이면 로직 관점으로 리뷰
- 중요도 기준으로 정렬 (최대 10건)
- 심각한 이슈 발견 시 자동 수정 후 재빌드

### 리뷰 결과 포맷
```markdown
## 코드 리뷰 결과 (중요도 기준 정렬)

### 🔴 반드시 수정
- [파일:줄번호] 이슈 설명 + 권장 수정 코드

### ⚠️ 권장 사항
- [파일:줄번호] 이슈 설명

### ✅ 잘한 부분
- 긍정적 피드백

### 최종 요약 테이블
| # | 요약 | 조치 필요 여부 |
```

## 주간보고 댓글 규칙

작업 완료 시 해당 주차 주간보고 위키 페이지에 **댓글**로 오늘 작업 내역을 남긴다.
나중에 주간보고 본문 작성할 때 댓글을 참고하여 빠짐없이 작성하기 위함.

### 주간보고 페이지 찾기
1. claude code 하위 페이지에서 `[주간보고]` 또는 `주간보고` 제목 검색
2. 해당 주차 페이지에 댓글 작성

### 댓글 형식
```markdown
## {날짜} 작업 내역

### {작업명}
- **커밋**: `{해시}` - {간단 설명}
- **내용**: {2~3줄 요약}
- **관련 위키**: [링크](https://nhnent.dooray.com/wiki/...)
- **관련 업무**: https://nhnent.dooray.com/project/tasks/...
```

## 워크트리 사용 시 주의사항
- 워크트리 경로: `../{프로젝트명}-{작업명}` (예: `../hps-coupon-api`)
- 빌드 시 `-f` 옵션으로 워크트리 경로의 pom.xml 지정
- 작업 완료 후 반드시 정리: `git worktree remove ../{폴더명}`
- 위키에 워크트리 사용 여부 기록 (다음 세션에서 이어서 작업 시 참고)

## 주의사항
- 빌드 실패 시 자동으로 에러 분석 후 수정 시도
- 커밋 전 반드시 빌드 성공 확인
- 위키 업데이트는 작업 완료 후 마지막에 수행
- 롤백 시 관련 프로젝트 모두 함께 롤백 (멀티 프로젝트 작업의 경우)

## 입력값

$ARGUMENTS
