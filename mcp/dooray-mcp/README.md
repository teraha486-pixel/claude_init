# Dooray MCP Server

Dooray API를 MCP(Model Context Protocol)를 통해 사용할 수 있게 해주는 서버입니다.

## 기능 목록

### 📅 캘린더
| 기능 | 설명 |
|------|------|
| `get_my_calendars` | 내 캘린더 목록 조회 |
| `get_detail_of_calendar` | 특정 캘린더 상세 정보 |
| `get_all_events_of_calendars` | 일정 목록 조회 (최대 1개월 단위) |
| `get_detail_of_event_on_calendar` | 특정 일정 상세 |
| `create_event_to_calendar` | 일정 생성 (반복 일정 지원) |
| `delete_event_from_calendar` | 일정 삭제 |

### ✅ 업무 (Task)
| 기능 | 설명 |
|------|------|
| `get_my_project_list` | 프로젝트 목록 조회 |
| `get_task_list_by_assignee_or_cc` | 담당자/참조자별 업무 조회 |
| `get_task_list_with_param` | 조건별 업무 검색 (마일스톤, 상태 등) |
| `get_detail_of_task` | 업무 상세 조회 (project_id + post_id) |
| `get_detail_of_task_by_id` | 업무 상세 조회 (post_id만으로) |
| `get_full_detail_of_task` | 업무 전체 상세 조회 (워크플로우, 담당자, 참조자, 태그 등) |
| `get_full_detail_of_task_by_id` | 업무 전체 상세 조회 (post_id만으로) |
| `create_task` | 업무 생성 |
| `modify_task` | 업무 수정 |
| `set_post_workflow` | 업무 상태(워크플로우) 변경 |
| `set_post_done` | 업무 완료 처리 |
| `upload_file_to_task` | 업무에 파일 첨부 |
| `get_project_milestones` | 프로젝트 마일스톤 조회 |
| `get_project_tags` | 프로젝트 태그 조회 |
| `get_post_comments` | 업무 댓글 조회 |
| `create_post_comment` | 업무 댓글 생성 |
| `update_post_comment` | 업무 댓글 수정 |
| `delete_post_comment` | 업무 댓글 삭제 |

### 📝 위키
| 기능 | 설명 |
|------|------|
| `get_wiki_list` | 위키 도메인 목록 |
| `get_personal_wiki` | 개인 위키 조회 |
| `get_child_wiki_list` | 하위 페이지 목록 |
| `get_wiki_page_content` | 페이지 내용 조회 (wiki_id + page_id) |
| `get_wiki_page_by_id` | 페이지 내용 조회 (page_id만으로) |
| `create_wiki` | 위키 페이지 생성 |
| `modify_wiki_page` | 페이지 수정 |
| `upload_file_to_wiki` | 위키에 파일/이미지 업로드 |
| `get_wiki_page_comments` | 댓글 조회 |
| `create_wiki_page_comment` | 댓글 작성 |
| `update_wiki_page_comment` | 댓글 수정 |
| `delete_wiki_page_comment` | 댓글 삭제 |

### 💬 메신저
| 기능 | 설명 |
|------|------|
| `get_channels_belongs_to` | 내가 속한 채널 목록 |
| `send_message_to_member_directly` | 1:1 메시지 전송 |
| `send_message_to_channel` | 채널에 메시지 전송 |
| `modify_message_sent_to_channel` | 채널 메시지 수정 |
| `delete_message_sent_to_channel` | 채널 메시지 삭제 |

### 📁 드라이브
| 기능 | 설명 |
|------|------|
| `get_drive_list` | 드라이브 목록 |
| `get_folder_list_in_drive` | 폴더 목록 |
| `upload_file_to_drive` | 파일 업로드 |
| `upload_not_file_content_to_drive` | 텍스트 내용을 파일로 저장 |

### 👤 기타
| 기능 | 설명 |
|------|------|
| `get_date_time_now` | 현재 시간 조회 |
| `get_my_member_identifier` | 내 멤버 ID 조회 |
| `get_members_information_by_name` | 이름으로 멤버 검색 |

---

## 실행 방법
### UV
1. 가상 환경 생성
```bash
$ uv venv --python 3.12.0
```
2. 의존성 설치
```bash
$ uv sync
```
3. 실행(환경변수 설정 필요)
```bash
$ uv run main.py
```

### MCP 클라이언트 내에서 서버 설정 방법
```json
{
  "mcpServers": {
    "dooray-mcp-server": {
      "command": "/path/to/project/.venv/bin/python3",
      "args": ["/path/to/project/main.py"],
      "env": {"DOORAY_API_TOKEN": "DOORAY API TOKEN STRING HERE"}
    }
  }
}
```
