# gia-poker-admin 빌드

gia-poker-admin 프로젝트를 빌드합니다.

## 의존성
- gia-core가 먼저 빌드되어 있어야 합니다. (`/build-gia-core` 먼저 실행)

## 실행할 명령어

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 17) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/gia/gia-poker-admin/pom.xml clean compile install -DskipTests
```

위 명령어를 실행하고 결과를 알려주세요.
