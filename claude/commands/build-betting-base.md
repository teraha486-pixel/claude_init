# betting_base 빌드

betting_base 프로젝트를 빌드합니다. (hangame-poker-server의 의존성)

> **주의**: JDK 11을 사용해야 합니다. JDK 17에서는 Lombok 호환성 문제 발생

## 실행할 명령어

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 11) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/betting_base/pom.xml clean compile install -DskipTests
```

위 명령어를 실행하고 결과를 알려주세요.
