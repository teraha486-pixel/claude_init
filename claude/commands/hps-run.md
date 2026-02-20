# hangame-poker-server 실행

hangame-poker-server 프로젝트를 실행합니다.

## 실행 모드

사용자 요청에 따라 두 가지 방식으로 실행:

### 1. CLI 직접 실행 (기본)
"실행해봐", "서버 실행해" 등의 요청 시 CLI에서 직접 실행

```bash
cd /Users/nhn/work/hangame-poker-server/poker-game

# slf4j-nop 제외한 클래스패스 생성 (로그 출력을 위해 필수)
CLASSPATH="target/classes"
for jar in target/lib/*.jar; do
  if [[ ! "$jar" == *"slf4j-nop"* ]]; then
    CLASSPATH="$CLASSPATH:$jar"
  fi
done

# 서버 실행
JAVA_HOME=$(/usr/libexec/java_home -v 11) java \
  -Djava.library.path=$HOME/jzmq/jzmq-jni/src/main/c++/.libs:/opt/homebrew/lib \
  -Djava.net.preferIPv4Stack=true \
  -javaagent:$HOME/.m2/repository/com/nhn/gameanvil/quasar-core/0.8.0/quasar-core-0.8.0-jdk11.jar=bm \
  -Xms4g -Xmx4g \
  -XX:+UseG1GC -XX:MaxGCPauseMillis=100 -XX:+UseStringDeduplication \
  -Dfile.encoding=UTF-8 \
  --add-opens=java.base/java.lang=ALL-UNNAMED \
  --add-opens=java.base/sun.security.x509=ALL-UNNAMED \
  -cp "$CLASSPATH" \
  com.nhn.hangame.poker.Main ./src/main/resources 2>&1 &

echo "PID: $!"
```

### 2. IntelliJ 설정 안내
"IntelliJ 설정", "Run Configuration" 등의 요청 시

1. `.run/Main.run.xml` 파일을 읽어서 현재 설정 확인

2. macOS용으로 수정이 필요하면 다음 내용으로 변경:
   - `PROGRAM_PARAMETERS`: `.\src\main\resources` → `./src/main/resources`
   - `VM_PARAMETERS`:
     ```
     -Djava.library.path=$USER_HOME$/jzmq/jzmq-jni/src/main/c++/.libs:/opt/homebrew/lib -Djava.net.preferIPv4Stack=true -javaagent:$USER_HOME$/.m2/repository/com/nhn/gameanvil/quasar-core/0.8.0/quasar-core-0.8.0-jdk11.jar=bm -Xms4g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=100 -XX:+UseStringDeduplication -Dfile.encoding=UTF-8 --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/sun.security.x509=ALL-UNNAMED
     ```

3. 변경 후 git assume-unchanged 설정:
   ```bash
   cd /Users/nhn/work/hangame-poker-server && git update-index --assume-unchanged .run/Main.run.xml
   ```

## 실행 확인 방법

```bash
# 프로세스 확인
ps aux | grep -E "[p]oker.*Main"

# 포트 확인
lsof -i :11200  # Gateway
lsof -i :10880  # CONFIG_SUPPORT

# 로그 확인
tail -f /Users/nhn/work/hangame-poker-server/poker-game/log/gameanvil-$(date +%Y-%m-%d-%H).log
```

## 서버 포트

| 서비스 | 포트 |
|--------|------|
| Gateway (TCP_SOCKET) | 11200 |
| CONFIG_SUPPORT | 10880 |
| GAME_SUPPORT | 10890 |
| API_SUPPORT | 10900 |
| API_GATEWAY_SUPPORT | 10910 |

## 주의사항

- **slf4j-nop 제외 필수**: CLI 실행 시 `slf4j-nop-*.jar`를 클래스패스에서 제외해야 로그가 정상 출력됨
- **빌드 선행**: 실행 전 빌드가 완료되어 있어야 함 (`/build-poker-server` 스킬 사용)
- **JDK 11 필수**: Java 11로 실행해야 함

## 대상 파일

- 프로젝트: `/Users/nhn/work/hangame-poker-server`
- Run Config: `/Users/nhn/work/hangame-poker-server/.run/Main.run.xml`
- 로그: `/Users/nhn/work/hangame-poker-server/poker-game/log/`

$ARGUMENTS
