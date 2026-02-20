# 두레이 캘린더

두레이 캘린더를 조회하고 일정을 생성/삭제합니다.

## 내 캘린더 ID

| 캘린더 | ID |
|--------|-----|
| 개인 | `3051057880790584417` |
| 포커서버팀 | `3842792407803282659` |
| 웹보드개발랩 | `2935428400867751158` |
| 근태-포커사업팀 | `2934647066272242745` |

## 사용 시나리오

### 1. 일정 조회
```
/dooray-calendar 이번 주 일정
/dooray-calendar 2026-02-17 ~ 2026-02-21 일정
```

### 2. 일정 생성
```
/dooray-calendar 내일 오후 3시 팀 회의 일정 추가
/dooray-calendar 2026-02-20 오전 10시~11시 스프린트 플래닝 생성
```

### 3. 일정 삭제
```
/dooray-calendar 내일 회의 일정 삭제
```

## API 목록

| API | 용도 |
|-----|------|
| `get_my_calendars` | 내 캘린더 목록 조회 |
| `get_detail_of_calendar` | 특정 캘린더 상세 정보 (calendar_id) |
| `get_all_events_of_calendars` | 일정 목록 조회 (최대 1개월 단위) |
| `get_detail_of_event_on_calendar` | 특정 일정 상세 (calendar_id + event_id) |
| `create_event_to_calendar` | 일정 생성 (반복 일정 지원) |
| `delete_event_from_calendar` | 일정 삭제 |

## 실행 방법

### 일정 조회 시
1. 기간 파악 (없으면 이번 주 기본)
2. `get_all_events_of_calendars(calendar_ids=[...], from="{시작일}", until="{종료일}")`
3. 캘린더별로 묶어서 표 형태로 출력

### 일정 생성 시
1. 제목, 시작/종료 시각, 캘린더 파악
2. 캘린더 미지정이면 개인 캘린더(`3051057880790584417`) 사용
3. `create_event_to_calendar(calendar_id, subject, startAt, endAt, ...)`
4. 반복 일정 필요 시 recurrence 파라미터 활용

### 일정 삭제 시
1. `get_all_events_of_calendars`로 해당 일정 ID 조회
2. `delete_event_from_calendar(calendar_id, event_id)`

## 출력 형식

```
📅 {날짜 범위} 일정

| 시간 | 제목 | 캘린더 | 참석자 |
|------|------|--------|--------|
| 10:00~11:00 | 스프린트 플래닝 | 포커서버팀 | ... |
```

## 입력값

$ARGUMENTS
