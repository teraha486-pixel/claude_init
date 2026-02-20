# SSH 서버 프로필 추가

`~/.ssh/server-profiles.conf`에 새 서버 프로필을 추가합니다.

## 사용 예시

```
/add-connect-server 알파8 pkra-rpkdev-wa888 추가해줘
/add-connect-server alpha-wa807 pkra-rpkdev-wa807
/add-connect-server real-wb904 pkra-rpksvc-wb904 [리얼] Game 노드
```

## 실행 흐름

### 1단계: 사용자 입력 파싱

사용자 메시지에서 다음 정보를 추출:
- **별칭(alias)**: connect 명령에 사용할 이름 (예: `alpha-wa807`)
- **호스트명**: 실제 서버 호스트명 또는 IP 주소 (예: `pkra-rpkdev-wa807`)
- **설명(description)**: 선택사항. 없으면 기존 패턴에서 추론

**필수 정보 누락 시 사용자에게 질문**:
- 별칭만 있고 호스트명/IP가 없는 경우 → "호스트명이나 IP 주소를 알려주세요"
- 호스트명/IP만 있고 별칭이 없는 경우 → "서버 이름(별칭)을 알려주세요 (예: alpha-wa807, 알파8)"
- 둘 다 없으면 → 둘 다 요청

**별칭 변환 규칙**:
- "알파7", "알파 7" → `alpha-` + 호스트명에서 서버번호 추출 (예: `wa807`)
- "리얼", "real" → `real-` + 서버번호
- "개발", "dev" → `dev-` + 서버번호
- 이미 `alpha-xxx` 형식이면 그대로 사용

### 2단계: server-profiles.conf 읽기

```bash
# 현재 프로필 확인
cat ~/.ssh/server-profiles.conf
```

- 중복 확인: 같은 별칭 또는 같은 호스트가 이미 있는지 체크
- 중복이면 사용자에게 알리고 중단

### 3단계: description 결정

사용자가 설명을 지정하지 않은 경우, 기존 프로필 패턴에서 추론:

| 별칭 패턴 | 기존 description 예시 | 추론 규칙 |
|----------|---------------------|----------|
| `alpha-wb8XX` | [알파1] ~ [알파6] | 다음 번호 부여 (예: [알파7]) |
| `alpha-wb804~807` | [알파] 공통노드/Game 노드 | 사용자에게 확인 |
| `real-waXXX` | [리얼] 공통노드/Game 노드 | 사용자에게 확인 |
| `dev-waXXX` | [개발] 게임서버 등 | 사용자에게 확인 |

**"알파N" 형태로 요청 시**: description을 `[알파N]`으로 자동 설정

### 4단계: 삽입 위치 결정

같은 그룹의 마지막 항목 뒤에 삽입:
- `alpha-*` → 알파 그룹 마지막 뒤
- `real-*` → 리얼 그룹 마지막 뒤
- `dev-*` → 개발 그룹 마지막 뒤
- `gia-*` → GIA 그룹 마지막 뒤
- `elk-*` → ELK 그룹 마지막 뒤

### 5단계: 프로필 추가

Edit 도구로 `~/.ssh/server-profiles.conf`에 새 프로필 삽입:

```
[{별칭}]
target_host = {호스트명}
description = {설명}
```

### 6단계: 완료 보고

```
추가 완료! `connect {별칭}`으로 {호스트명}에 접속할 수 있어요.
```
