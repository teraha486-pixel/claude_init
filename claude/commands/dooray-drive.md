# 두레이 드라이브

두레이 드라이브에 파일을 업로드하거나 폴더 목록을 조회합니다.

## 사용 시나리오

### 1. 드라이브 목록 조회
```
/dooray-drive 목록
/dooray-drive 드라이브 목록
```

### 2. 폴더 내 파일 조회
```
/dooray-drive {드라이브명} 폴더 목록
```

### 3. 파일 업로드
```
/dooray-drive /path/to/file.png 업로드
/dooray-drive 이 내용을 report.md 파일로 드라이브에 저장
```

## API 목록

| API | 용도 |
|-----|------|
| `get_drive_list` | 드라이브 목록 조회 |
| `get_folder_list_in_drive` | 드라이브 내 폴더/파일 목록 조회 (drive_id) |
| `upload_file_to_drive` | 로컬 파일 업로드 (drive_id + file_path) |
| `upload_not_file_content_to_drive` | 텍스트 내용을 파일로 저장 (drive_id + filename + content) |

## 실행 방법

### 파일 업로드 시
1. `get_drive_list()`로 드라이브 목록 확인
2. 대상 드라이브 ID 선택
3. 로컬 파일: `upload_file_to_drive(drive_id, file_path)`
4. 텍스트 내용: `upload_not_file_content_to_drive(drive_id, filename, content)`

### 폴더 조회 시
1. `get_drive_list()`로 drive_id 확인
2. `get_folder_list_in_drive(drive_id)`로 목록 조회

## 입력값

$ARGUMENTS
