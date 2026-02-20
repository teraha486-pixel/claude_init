# hangame-poker-server 원래 브랜치로 복귀 (stash 복원 + assume-unchanged 재설정)

`/hps-switch-to`로 전환한 후, 원래 브랜치로 돌아가면서 stash된 파일을 복원합니다.

## 사용 방법

```
/hps-switch-back
```

인자 없이 실행하면 stash 메시지에서 원래 브랜치를 자동 감지합니다.

## 실행 흐름

### STEP 1: stash에서 원래 브랜치 확인

```bash
cd /Users/nhn/work/hangame-poker-server
git stash list | grep "hps-switch:" | head -1
```

- stash 메시지 형식: `hps-switch: {출발브랜치} → {도착브랜치} | files: {파일목록}`
- 출발 브랜치 = 돌아갈 브랜치
- 파일 목록 = assume-unchanged 재설정할 파일들

hps-switch stash가 없으면:
> "⚠️ /hps-switch-to 로 전환한 기록이 없습니다. 수동으로 브랜치명을 입력해주세요."

### STEP 2: 브랜치 전환

```bash
cd /Users/nhn/work/hangame-poker-server
git checkout {원래브랜치}
```

### STEP 3: stash pop + assume-unchanged 재설정

```bash
cd /Users/nhn/work/hangame-poker-server

# 1. stash pop (해당 stash 번호 지정)
git stash pop {stash_index}

# 2. assume-unchanged 재설정
git update-index --assume-unchanged {파일1} {파일2} ...
```

- stash 메시지의 파일 목록으로 assume-unchanged 재설정
- stash pop 실패 시 (conflict 등) → 사용자에게 수동 해결 안내

### STEP 4: 결과 출력

```
✅ 브랜치 복귀 완료: {전환브랜치} → {원래브랜치}

🔓 assume-unchanged 복원된 파일:
  - poker-common/pom.xml
  - .run/Main.run.xml

📋 현재 상태:
  - 브랜치: {원래브랜치}
  - stash: 정리 완료
  - assume-unchanged: 재설정 완료
```

### STEP 5: 검증

```bash
cd /Users/nhn/work/hangame-poker-server

# assume-unchanged 플래그 확인
git ls-files -v | grep ^h
```

- stash 메시지에 기록된 파일들이 모두 `h`(소문자)로 표시되는지 확인

## 예외 처리

### 1. stash pop conflict
- conflict 발생 시 사용자에게 안내
- assume-unchanged는 conflict 해결 후 수동 설정하도록 안내

### 2. 원래 브랜치가 삭제된 경우
- 에러 출력 후 사용자에게 브랜치명 입력 요청

### 3. 여러 hps-switch stash가 있는 경우
- 가장 최근(index가 낮은) hps-switch stash를 사용
- 여러 개 있으면 목록 보여주고 선택 요청

## 주의사항

- **반드시 `/hps-switch-to`로 전환한 후에 사용**
- assume-unchanged 재설정을 빠뜨리면 다음 브랜치 전환 시 같은 문제 재발

## 프로젝트 경로

- `/Users/nhn/work/hangame-poker-server`

## 입력값

$ARGUMENTS
