# hangame-poker-server 빌드

hangame-poker-server 프로젝트를 빌드합니다.

## 의존성
- betting_base가 먼저 빌드되어 있어야 합니다. (`/build-betting-base` 먼저 실행)

## 빌드 전 확인사항 (필수)

**macOS 환경에서는 pom.xml 수정이 필요합니다.**

### 1. poker-common/pom.xml 확인

```bash
grep -E "protoc.version|compile-csharp" /Users/nhn/work/hangame-poker-server/poker-common/pom.xml
```

### 2. 수정이 필요한 경우

| 항목 | 원본 (Windows) | macOS용 |
|------|---------------|---------|
| `protoc.version` | `3.6.1` | `3.19.1` |
| protobuf goals | compile, compile-csharp, compile-js, compile-custom | `compile`만 유지 |

수정이 필요하면 다음을 적용:

```xml
<!-- protoc.version 변경 -->
<protoc.version>3.19.1</protoc.version>

<!-- goals에서 compile만 유지 -->
<goals>
    <goal>compile</goal>
</goals>
```

### 3. assume-unchanged 설정

```bash
git -C /Users/nhn/work/hangame-poker-server update-index --assume-unchanged poker-common/pom.xml
```

## 실행할 명령어

```bash
JAVA_HOME=$(/usr/libexec/java_home -v 11) /Users/nhn/work/maven/apache-maven-3.6.3/bin/mvn -f /Users/nhn/work/hangame-poker-server/pom.xml -B clean compile install -DskipTests -Plocal
```

## 트러블슈팅

### protoc 라이브러리 로딩 에러

**증상**: `Library not loaded: @rpath/libprotoc.XX.X.X.dylib`

**원인**: macOS의 protoc 버전과 pom.xml의 protoc.version 불일치

**해결**: 위 "빌드 전 확인사항" 참고하여 protoc.version을 3.19.1로 변경

### 상세 가이드

`~/init/docs/vscode/hangame-poker-server.md` 참고
