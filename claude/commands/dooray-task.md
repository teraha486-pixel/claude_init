# 두레이 업무 조회

두레이 URL 또는 업무 ID로 업무 정보를 조회합니다.

## 지원하는 URL 형식
- `https://nhnent.dooray.com/project/tasks/{task_id}`
- `https://nhnent.dooray.com/project/tasks/{task_id}#comment-{comment_id}`
- `https://nhnent.dooray.com/task/view/tasks/{task_id}`
- `https://nhnent.dooray.com/task/comment/{task_id}` (댓글 알림 링크)
- 또는 단순히 업무 ID만 입력

## 실행 방법

1. 입력값에서 업무 ID 추출 (URL 또는 숫자)
   - URL 패턴: `/tasks/(\d+)` 에서 숫자 추출
   - URL 패턴: `/task/comment/(\d+)` 에서 숫자 추출
   - 댓글 ID 패턴: `#comment-(\d+)` 에서 숫자 추출 (있는 경우)

2. `get_detail_of_task_by_id` 또는 `get_full_detail_of_task_by_id` API 호출
   - 기본 조회: `get_detail_of_task_by_id(post_id)` - 제목, 본문 등 기본 정보
   - 상세 조회: `get_full_detail_of_task_by_id(post_id)` - 워크플로우, 담당자, 참조자, 태그, 만기일 등 전체 정보

3. 댓글 ID가 있는 경우:
   - `get_post_comments` API로 댓글 목록 조회
   - 해당 댓글 ID 찾아서 하이라이트

4. 출력 형식:
   - 업무번호, 제목, 상태(워크플로우), 등록자, 담당자, 참조자
   - 태그, 마일스톤, 만기일
   - 본문 요약
   - 댓글이 요청된 경우 댓글 목록

## 사용 가능한 API

| API | 용도 |
|-----|------|
| `get_detail_of_task_by_id` | post_id만으로 업무 기본 정보 조회 |
| `get_full_detail_of_task_by_id` | post_id만으로 업무 전체 상세 조회 |
| `get_post_comments` | 업무 댓글 목록 조회 |
| `create_post_comment` | 업무에 댓글 작성 |
| `set_post_workflow` | 업무 상태 변경 |
| `set_post_done` | 업무 완료 처리 |

## 입력값

$ARGUMENTS
