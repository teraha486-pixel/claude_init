# GameData Zone 동기화 스킬

ALPHA(zone_id=1)를 기준으로 다른 zone의 game_data를 동기화합니다.

## 사용 방법

```
/sync-gamedata [zone_name]
```

예시:
- `/sync-gamedata ALPHA5` - ALPHA5 동기화
- `/sync-gamedata 알파6` - ALPHA6 동기화
- `/sync-gamedata ALPHA8` - 없으면 새로 생성 후 동기화
- `알파5 최신화 시켜줘` - 자연어로도 사용 가능

## 입력 파싱

사용자 입력에서 zone_name 추출:
- "알파5", "ALPHA5", "alpha5" → ALPHA5
- "알파6 최신화", "ALPHA6 동기화해줘" → ALPHA6
- 숫자만 있으면: "5" → ALPHA5

## 실행 흐름

### STEP 0: Stage 테이블 조회 (필수!)

**반드시 먼저** stage 테이블에서 zone_id 매핑 확인:

```sql
SELECT zone_id, zone_name, create_datetime, create_account
FROM hcardp_game.stage
ORDER BY zone_id;
```

**중요**: zone_name과 zone_id는 1:1 매핑이 아님!
- ALPHA = zone_id 1
- ALPHA1 = zone_id 2
- ALPHA5 = zone_id 6
- ALPHA6 = zone_id 7
- 등등...

### STEP 1: Zone 존재 여부 확인

요청된 zone_name이 stage 테이블에 있는지 확인:

```sql
SELECT zone_id FROM hcardp_game.stage WHERE zone_name = '{요청된_zone_name}';
```

**결과에 따라 분기:**
- **존재함**: 해당 zone_id로 동기화 진행 → STEP 2로
- **없음**: STEP 1-1로 이동하여 신규 zone 생성

### STEP 1-1: 신규 Zone 생성 (zone이 없을 경우)

1. 다음 zone_id 확인:
```sql
SELECT MAX(zone_id) + 1 as next_zone_id FROM hcardp_game.stage;
```

2. stage 테이블에 INSERT:
```sql
INSERT INTO hcardp_game.stage (zone_id, zone_name, create_datetime, create_account)
VALUES ({next_zone_id}, '{zone_name}', NOW(), '{사용자_사번}');
```

**주의**: 사용자 사번이 필요하면 AskUserQuestion으로 질문

### STEP 2: 사전 분석

대상 zone과 ALPHA 간 차이 분석:

```sql
SELECT 'SAME' as status, COUNT(*) as cnt FROM game_data a
  JOIN game_data b ON a.game_data_key = b.game_data_key
  WHERE a.zone_id = 1 AND b.zone_id = {대상_zone_id} AND a.game_data_json = b.game_data_json
UNION ALL
SELECT 'DIFF', COUNT(*) FROM game_data a
  JOIN game_data b ON a.game_data_key = b.game_data_key
  WHERE a.zone_id = 1 AND b.zone_id = {대상_zone_id} AND a.game_data_json != b.game_data_json
UNION ALL
SELECT 'ONLY_ALPHA', COUNT(*) FROM game_data a
  LEFT JOIN game_data b ON a.game_data_key = b.game_data_key AND b.zone_id = {대상_zone_id}
  WHERE a.zone_id = 1 AND b.game_data_key IS NULL
UNION ALL
SELECT 'ONLY_TARGET', COUNT(*) FROM game_data b
  LEFT JOIN game_data a ON a.game_data_key = b.game_data_key AND a.zone_id = 1
  WHERE b.zone_id = {대상_zone_id} AND a.game_data_key IS NULL;
```

분석 결과 요약 표시:
- 동일: N건
- 다름: N건 (UPDATE 대상)
- ALPHA에만 있음: N건 (INSERT 대상)
- 대상 zone에만 있음: N건 (유지)

### STEP 3: 백업 (기존 데이터가 있을 경우)

SELECT 결과를 JSON 파일로 저장:

```sql
SELECT * FROM game_data WHERE zone_id = {대상_zone_id};
```

저장 위치: `/Users/nhn/work/hangame-poker-server/docs/backup_zone{N}_{YYYYMMDD}.json`

### STEP 4: INSERT 실행

ALPHA에만 있는 데이터를 대상 zone에 추가:

```sql
INSERT INTO game_data (zone_id, game_data_key, game_data_json, expose_scope, mod_date, modifier, reg_date, register, tags)
SELECT {대상_zone_id}, game_data_key, game_data_json, expose_scope, mod_date,
       CONCAT('SYNC_FROM_ALPHA (', IFNULL(modifier, ''), ')'),
       NOW(), register, tags
FROM game_data
WHERE zone_id = 1
  AND game_data_key NOT IN (SELECT game_data_key FROM game_data WHERE zone_id = {대상_zone_id});
```

### STEP 5: UPDATE 실행

다른 데이터를 ALPHA 기준으로 동기화:

```sql
UPDATE game_data t
JOIN game_data src ON src.game_data_key = t.game_data_key AND src.zone_id = 1
SET t.game_data_json = src.game_data_json,
    t.mod_date = NOW(),
    t.modifier = CONCAT('SYNC_FROM_ALPHA (', IFNULL(src.modifier, ''), ')')
WHERE t.zone_id = {대상_zone_id}
  AND t.game_data_json != src.game_data_json;
```

### STEP 6: 검증

동기화 결과 확인:

```sql
SELECT COUNT(*) as diff_count
FROM game_data a
JOIN game_data b ON a.game_data_key = b.game_data_key
WHERE a.zone_id = 1 AND b.zone_id = {대상_zone_id}
  AND a.game_data_json != b.game_data_json;
```

결과가 0이면 동기화 성공!

### STEP 7: 롤백 플랜 생성

롤백 SQL 파일 생성:
저장 위치: `/Users/nhn/work/hangame-poker-server/docs/sync_alpha_to_zone{N}_rollback.sql`

**롤백 SQL 파일 내용:**

```sql
-- ============================================
-- ALPHA → {zone_name} 동기화 롤백 SQL
-- 생성일: {YYYY-MM-DD}
-- zone_id: {zone_id}
-- ============================================

-- ============================================
-- STEP 1: INSERT된 {N}건 삭제
-- ============================================
DELETE FROM game_data
WHERE zone_id = {zone_id}
  AND game_data_key IN (
    '{INSERT된 key1}',
    '{INSERT된 key2}',
    ...
  );

-- ============================================
-- STEP 2: UPDATE된 {N}건 복원
-- 백업 파일: /Users/nhn/work/hangame-poker-server/docs/backup_zone{N}_{YYYYMMDD}.json
-- ============================================
-- UPDATE 대상 목록:
-- {UPDATE된 key 목록}

-- 복원 예시:
-- UPDATE game_data
-- SET game_data_json = '{원본 JSON}',
--     mod_date = '{원본 mod_date}',
--     modifier = '{원본 modifier}'
-- WHERE zone_id = {zone_id} AND game_data_key = '{config_key}';

-- ============================================
-- 롤백 검증
-- ============================================
-- SELECT COUNT(*) FROM game_data
-- WHERE zone_id = {zone_id} AND modifier LIKE 'SYNC_FROM_ALPHA%';
-- 결과가 0이면 롤백 완료
```

### STEP 8: 결과 출력

**반드시 아래 형식으로 결과 정리:**

```
## 동기화 결과

### Zone 정보
| 항목 | 값 |
|------|-----|
| zone_name | {zone_name} |
| zone_id | {zone_id} |
| 신규 생성 | 예/아니오 |

### 동기화 내역
| 작업 | 건수 |
|------|------|
| INSERT | N건 |
| UPDATE | N건 |
| 동일 (변경 없음) | N건 |
| 대상 zone 전용 (유지) | N건 |

### 동기화된 config 목록
{game_data_key를 콤마로 나열}

### 롤백 플랜
| 파일 | 경로 |
|------|------|
| 백업 JSON | /Users/nhn/work/hangame-poker-server/docs/backup_zone{N}_{YYYYMMDD}.json |
| 롤백 SQL | /Users/nhn/work/hangame-poker-server/docs/sync_alpha_to_zone{N}_rollback.sql |
```

### STEP 9: 사용자 확인 및 롤백 플랜 정리

**AskUserQuestion 도구로 질문:**

```
동기화가 완료되었습니다. 서버 테스트 후 결과를 알려주세요.

1. 잘 동작함 - 롤백 플랜 삭제
2. 문제 있음 - 롤백 플랜 유지 (수동 롤백 필요)
3. 나중에 확인 - 롤백 플랜 유지
```

**사용자 응답에 따른 처리:**

- **"잘 동작함" 선택**: 롤백 파일들 삭제
  ```bash
  rm -f /Users/nhn/work/hangame-poker-server/docs/backup_zone{N}_{YYYYMMDD}.json
  rm -f /Users/nhn/work/hangame-poker-server/docs/sync_alpha_to_zone{N}_rollback.sql
  ```
  "롤백 플랜이 삭제되었습니다." 메시지 출력

- **"문제 있음" 선택**:
  롤백 파일 경로 다시 안내하고 수동 롤백 방법 설명

- **"나중에 확인" 선택**:
  "롤백 플랜이 유지됩니다. 나중에 삭제하려면 파일을 직접 삭제하세요." 메시지 출력

## 주의사항

1. **ALPHA에 없는 데이터는 삭제 안 함** - 대상 zone 전용 데이터 유지
2. **백업 필수** - 기존 데이터가 있으면 반드시 백업
3. **modifier 기록** - `SYNC_FROM_ALPHA (원본 modifier)` 형식
4. **zone_id=1(ALPHA)은 대상 불가** - 기준 데이터이므로
5. **롤백 플랜** - 동기화 후 반드시 생성, 확인 후 삭제

## 파일 저장 경로

| 파일 | 경로 |
|------|------|
| 백업 JSON | `/Users/nhn/work/hangame-poker-server/docs/backup_zone{N}_{YYYYMMDD}.json` |
| 롤백 SQL | `/Users/nhn/work/hangame-poker-server/docs/sync_alpha_to_zone{N}_rollback.sql` |

## MCP 도구

- `mcp__mysql-alpha-game__execute_sql`

## 입력값

$ARGUMENTS
