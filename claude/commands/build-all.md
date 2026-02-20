# 전체 프로젝트 빌드

모든 프로젝트를 의존성 순서대로 빌드합니다.

## 빌드 순서
1. betting_base (Java 11) - 먼저!
2. hangame-poker-server (Java 11)
3. gia-core (Java 17)
4. gia-poker-admin (Java 17)

## 실행할 명령어

### 1. betting_base (Java 11)
```bash
JAVA_HOME=$(/usr/libexec/java_home -v 11) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/betting_base/pom.xml clean compile install -DskipTests
```

### 2. hangame-poker-server (Java 11)
```bash
JAVA_HOME=$(/usr/libexec/java_home -v 11) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/hangame-poker-server/pom.xml -B clean compile install -DskipTests -Plocal
```

### 3. gia-core (Java 17)
```bash
JAVA_HOME=$(/usr/libexec/java_home -v 17) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/gia/gia-core/pom.xml clean compile install -DskipTests
```

### 4. gia-poker-admin (Java 17)
```bash
JAVA_HOME=$(/usr/libexec/java_home -v 17) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/gia/gia-poker-admin/pom.xml clean compile install -DskipTests
```

위 명령어들을 순서대로 실행하고 각 결과를 알려주세요.
