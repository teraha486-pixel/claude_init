# hangame-poker-server 브랜치 전환 (assume-unchanged 처리)

assume-unchanged 설정된 파일들을 안전하게 stash하고 타겟 브랜치로 전환합니다.

## 사용 방법

```
/hps-switch-to [브랜치명]
```

예시:
- `/hps-switch-to release` - release 브랜치로 전환
- `/hps-switch-to feature/coupon-api` - feature 브랜치로 전환

## 실행 흐름

### STEP 1: 현재 상태 확인

```bash
cd /Users/nhn/work/hangame-poker-server
git branch --show-current
```

- 현재 브랜치가 타겟 브랜치와 같으면 → "이미 해당 브랜치입니다" 출력 후 종료

### STEP 2: assume-unchanged 파일 목록 확인

```bash
cd /Users/nhn/work/hangame-poker-server
git ls-files -v | grep ^h
```

- 소문자 `h`로 시작하는 파일 = assume-unchanged 설정된 파일
- 없으면 → 바로 STEP 4로 이동 (일반 checkout)

### STEP 3: assume-unchanged 해제 + stash

발견된 assume-unchanged 파일들에 대해:

```bash
cd /Users/nhn/work/hangame-poker-server

# 1. 모든 assume-unchanged 파일 플래그 해제
git update-index --no-assume-unchanged {파일1} {파일2} ...

# 2. 변경된 파일만 stash (변경 없는 파일은 stash 불필요)
git stash push -m "hps-switch: {현재브랜치} → {타겟브랜치} | files: {파일목록}" -- {변경된_파일들}
```

- stash 메시지에 출발/도착 브랜치와 파일 목록을 기록 (복귀 시 참고)
- 변경사항이 없는 assume-unchanged 파일은 플래그만 해제하고 stash하지 않음

### STEP 4: 브랜치 전환

```bash
cd /Users/nhn/work/hangame-poker-server
git checkout {타겟브랜치}
```

### STEP 5: 결과 출력

```
✅ 브랜치 전환 완료: {이전브랜치} → {타겟브랜치}

📦 stash된 assume-unchanged 파일:
  - poker-common/pom.xml
  - .run/Main.run.xml

💡 돌아가려면: /hps-switch-back
```

## 예외 처리

### 1. 일반 uncommitted changes가 있는 경우
- assume-unchanged 파일 외에 다른 변경사항이 있으면 경고:
  > "⚠️ assume-unchanged 외에 uncommitted changes가 있습니다. 함께 stash할까요?"
- 사용자 확인 후 진행

### 2. checkout 실패
- stash한 상태에서 checkout 실패 시 → stash pop + assume-unchanged 재설정으로 원복

### 3. 타겟 브랜치가 없는 경우
- 로컬에 없으면 origin에서 fetch 후 checkout
- origin에도 없으면 에러 출력

## 주의사항

- **develop, master에 직접 커밋 금지** (CLAUDE.md 규칙)
- 브랜치 전환 전 현재 브랜치 확인 필수

## 프로젝트 경로

- `/Users/nhn/work/hangame-poker-server`

## 입력값

$ARGUMENTS
