# Claude Code 사용량 모니터링 (CCM) 설정

## 초기 설치

새 환경에서 CCM을 설정할 때 아래 순서대로 진행하세요.

### 1. ccm 폴더 복사

```bash
# init에서 ccm 폴더를 홈으로 복사
cp -r ~/init/ccm ~/ccm

# 스크립트 실행 권한 부여
chmod +x ~/ccm/scripts/*.sh
```

### 2. 설정 파일 생성

```bash
# 템플릿을 복사하여 설정 파일 생성
cp ~/ccm/ccm_config.template ~/ccm/ccm_config

# 설정 파일 편집 (USER_NAME 수정 필수)
vi ~/ccm/ccm_config
```

설정 파일 내용:
```
SERVER_URL=http://10.161.31.71:8012
API_KEY=prod-secure-api-key-change-this
USER_NAME=엔에이치엔_포커서버팀_홍길동  # 본인 정보로 수정
```

### 3. 필수 도구 설치

```bash
# ccusage (사용량 조회)
npm install -g ccusage

# jq (JSON 파싱)
brew install jq
```

### 4. 쉘 alias 설정 (~/.zshrc에 추가)

```bash
# CCM 명령어
alias ccu='$HOME/ccm/scripts/collect_and_upload.sh -v'
alias usage='npx ccusage'
alias usaged='npx ccusage daily'
alias usagem='npx ccusage monthly'
```

```bash
# alias 적용
source ~/.zshrc
```

### 5. crontab 설정 (자동 업로드)

```bash
crontab -e
```

다음 줄 추가:
```cron
0 * * * * /Users/nhn/ccm/scripts/collect_and_upload.sh -v >> /Users/nhn/ccu.log 2>&1
```

---

## 단축키 (alias)

| 명령어 | 기능 | 실행 명령 |
|--------|------|-----------|
| `ccu` | 사용량 업로드 | `$HOME/ccm/scripts/collect_and_upload.sh -v` |
| `usage` | 전체 사용량 확인 | `npx ccusage` |
| `usaged` | 일별 사용량 확인 | `npx ccusage daily` |
| `usagem` | 월별 사용량 확인 | `npx ccusage monthly` |

## 자동 업로드 (crontab)

매 정각마다 자동으로 사용량 업로드

```cron
0 * * * * /Users/nhn/ccm/scripts/collect_and_upload.sh -v >> /Users/nhn/ccu.log 2>&1
```

### crontab 관리 명령어
```bash
crontab -l    # 현재 crontab 확인
crontab -e    # crontab 편집
```

## 설정 파일

`/Users/nhn/ccm/ccm_config`

```
SERVER_URL=http://10.161.31.71:8012
API_KEY=prod-secure-api-key-change-this
USER_NAME=엔에이치엔_포커서버팀_김근형
```

## 스크립트 위치

- `/Users/nhn/ccm/scripts/collect_and_upload.sh` - 수집 및 업로드
- `/Users/nhn/ccm/scripts/upload_usage.sh` - 업로드만

## 로그 확인

```bash
tail -f ~/ccu.log
```
