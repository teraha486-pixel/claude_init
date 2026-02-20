# 두레이 메신저

두레이 메신저로 채널 메시지 전송 및 1:1 메시지를 보냅니다.

## 사용 시나리오

### 1. 채널 메시지 전송
```
/dooray-messenger #포커서버팀 "배포 완료됐습니다"
/dooray-messenger 포커서버팀 채널에 "금일 18시 점검 예정입니다" 전송
```

### 2. 1:1 메시지 전송
```
/dooray-messenger @홍길동 "확인 부탁드립니다"
/dooray-messenger 홍길동한테 "PR 리뷰 요청드립니다" 전송
```

### 3. 채널 메시지 수정/삭제
```
/dooray-messenger 마지막 메시지 "오타 수정한 내용" 으로 수정
/dooray-messenger 마지막 메시지 삭제
```

## API 목록

| API | 용도 |
|-----|------|
| `get_channels_belongs_to` | 내가 속한 채널 목록 조회 |
| `send_message_to_member_directly` | 1:1 메시지 전송 (member_id + message) |
| `send_message_to_channel` | 채널에 메시지 전송 (channel_id + message) |
| `modify_message_sent_to_channel` | 채널 메시지 수정 (channel_id + log_id + message) |
| `delete_message_sent_to_channel` | 채널 메시지 삭제 (channel_id + log_id) |

## 실행 방법

### 채널 메시지 전송 시
1. 채널명으로 ID를 모르는 경우 → `get_channels_belongs_to()`로 목록 조회
2. `send_message_to_channel(channel_id="{id}", message="{내용}")`

### 1:1 메시지 전송 시
1. 상대방 이름만 있는 경우 → `get_members_information_by_name(name="{이름}")`으로 member_id 조회
2. `send_message_to_member_directly(member_id="{id}", message="{내용}")`

### 채널 메시지 수정/삭제 시
1. 해당 채널의 최근 메시지 목록에서 log_id 확인
2. `modify_message_sent_to_channel(channel_id, log_id, message)` 또는
   `delete_message_sent_to_channel(channel_id, log_id)`

## 주의사항
- 메시지 내용은 Markdown 지원
- 1:1 메시지는 상대방 member_id 필요
- 채널 삭제는 본인이 보낸 메시지만 가능

## 입력값

$ARGUMENTS
