# env 레포 동기화 스킬

init 레포의 MCP/스킬 변경사항을 env 레포에 동기화합니다.

## 상태 파일

`~/env/.sync-state.json`에서 동기화 상태 관리:
```json
{
  "lastSyncCommit": "커밋해시",
  "lastSyncDate": "날짜",
  "excluded": {
    "skills": ["제외할 스킬"],
    "mcps": ["제외할 MCP"]
  },
  "synced": {
    "skills": ["동기화된 스킬 목록"],
    "mcps": ["동기화된 MCP 목록"]
  }
}
```

## 실행 흐름

### 1단계: 상태 파일 및 init 확인

```bash
# env 레포 최신화
cd ~/env && git pull origin main

# 상태 파일 읽기
cat ~/env/.sync-state.json

# init 최신 커밋 확인
cd ~/init && git rev-parse --short HEAD

# 마지막 동기화 이후 변경된 파일 확인
cd ~/init && git diff --name-only {lastSyncCommit}..HEAD
```

### 2단계: init 스캔

```bash
# 커스텀 스킬 목록 (심볼릭 링크 제외 = Anthropic 스킬 제외)
find ~/init/claude/commands -maxdepth 1 -type f -name "*.md" | xargs -n1 basename | sed 's/.md$//'

# MCP 목록
ls -d ~/init/mcp/*/ 2>/dev/null | xargs -n1 basename
```

### 3단계: 변경사항 분석

상태 파일과 비교해서 분류:
- **새로 추가됨**: init에 있는데 synced에 없음
- **삭제됨**: synced에 있는데 init에 없음
- **제외됨**: excluded에 있는 항목 (표시만, 반영 안 함)
- **동일**: 변경 없음

### 4단계: 변경사항 표시

```
## 🔄 init → env 동기화

마지막 동기화: {lastSyncDate} (커밋: {lastSyncCommit})
현재 init 커밋: {currentCommit}

### 커스텀 스킬
| 상태 | 스킬명 | 비고 |
|------|--------|------|
| ➕ 새로 추가 | /new-skill | init에 추가됨 |
| ➖ 삭제됨 | /old-skill | init에서 삭제됨 |
| 🚫 제외됨 | /test-skill | 사용자가 제외함 |
| ✓ 동기화됨 | /do | |

### MCP 서버
| 상태 | MCP명 | 비고 |
|------|-------|------|
| ➕ 새로 추가 | new-mcp | init에 추가됨 |
| ✓ 동기화됨 | dooray-mcp | |
```

### 5단계: 사용자 선택

```
어떻게 할까요?

1. 전체 반영 (새로 추가 + 삭제 모두)
2. 추가만 반영 (삭제는 유지)
3. 하나씩 선택
4. 취소
```

**"하나씩 선택" 시:**
- 각 항목별로 "반영 / 제외 / 건너뛰기" 선택
- "제외" 선택하면 excluded에 추가 → 다음에 안 물어봄

### 6단계: env 업데이트 (승인 시)

1. **setup.html 수정**
   - 새 스킬: `<tr>` 추가 (커스텀 스킬 섹션에)
   - 새 MCP: `<tr>` 추가 + 설정 필요하면 입력 폼도 추가
   - 삭제된 항목: 해당 행 제거

2. **CLAUDE.md 수정** (MCP 추가/삭제 시)
   - 새 MCP: 설치 명령어 섹션 추가
   - 삭제된 MCP: 해당 섹션 제거

3. **.sync-state.json 업데이트**
   ```json
   {
     "lastSyncCommit": "새커밋해시",
     "lastSyncDate": "오늘날짜",
     "excluded": { ... },
     "synced": { "skills": [...], "mcps": [...] }
   }
   ```

4. **커밋 & 푸시**
   ```bash
   cd ~/env
   git add -A
   git commit -m "[태양] init 동기화: {변경내용 요약}"
   git push origin main
   git reflog expire --expire=now --all && git gc --prune=now
   ```

### 7단계: 완료 안내

```
✅ env 동기화 완료!

동기화 커밋: {lastSyncCommit} → {newCommit}

반영된 변경사항:
- 스킬 추가: /new-skill
- 스킬 삭제: /old-skill
- MCP 추가: new-mcp

제외 목록에 추가됨:
- /test-skill (다음에 안 물어봄)

env 레포: https://github.com/zman-lab/env
```

## 옵션

### 제외 목록 관리

제외했던 항목 다시 추가하고 싶으면:
```
/sync-env --show-excluded
```

excluded 목록 보여주고 "다시 포함할까요?" 물어봄

### 강제 전체 스캔

상태 무시하고 처음부터 비교:
```
/sync-env --full
```

## 주의사항

- Anthropic 스킬(심볼릭 링크)은 스캔에서 제외 (별도 관리)
- 새 MCP의 설정 입력 폼은 MCP 특성에 맞게 수동 확인 필요할 수 있음
- 스킬 설명은 .md 파일의 첫 번째 `#` 제목에서 추출
