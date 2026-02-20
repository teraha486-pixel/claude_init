# Dooray MCP 사용 가이드

Python 기반 Dooray MCP 서버 사용 가이드입니다.

## 개요

두레이 Open API를 MCP(Model Context Protocol)로 래핑하여 Claude Code에서 직접 사용할 수 있게 합니다.

**경로**: `~/init/mcp/dooray-mcp`

## 지원 기능 (총 48개 도구)

### 공통 (3개)
| 도구 | 설명 |
|------|------|
| `get_date_time_now` | 현재 날짜/시간 조회 |
| `get_members_information_by_name` | 멤버 정보 조회 (이름으로 검색) |
| `get_my_member_identifier` | 내 멤버 ID 조회 |

### 캘린더 (6개)
| 도구 | 설명 |
|------|------|
| `get_my_calendars` | 내 캘린더 목록 조회 |
| `get_detail_of_calendar` | 캘린더 상세 정보 조회 |
| `create_event_to_calendar` | 일정 생성 |
| `get_all_events_of_calendars` | 일정 조회 (최대 1개월 범위) |
| `get_detail_of_event_on_calendar` | 일정 상세 조회 |
| `delete_event_from_calendar` | 일정 삭제 |

### 프로젝트/업무 (18개)
| 도구 | 설명 |
|------|------|
| `get_my_project_list` | 프로젝트 목록 조회 |
| `get_project_milestones` | 프로젝트 마일스톤 조회 |
| `get_project_tags` | 프로젝트 태그 조회 |
| `get_task_list_by_assignee_or_cc` | 담당자/참조자별 업무 조회 |
| `get_task_list_with_param` | 상세 조건으로 업무 조회 |
| `get_detail_of_task` | 업무 상세 조회 (project_id + post_id) |
| `get_detail_of_task_by_id` | 업무 상세 조회 (post_id만으로) |
| `get_full_detail_of_task` | 업무 전체 상세 조회 (워크플로우, 담당자, 참조자, 태그 등) |
| `get_full_detail_of_task_by_id` | 업무 전체 상세 조회 (post_id만으로) |
| `create_task` | 업무 생성 |
| `modify_task` | 업무 수정 |
| `set_post_workflow` | 업무 상태(워크플로우) 변경 |
| `set_post_done` | 업무 완료 처리 |
| `upload_file_to_task` | 업무에 파일 업로드 |
| `get_post_comments` | 업무 댓글 조회 |
| `create_post_comment` | 업무 댓글 생성 |
| `update_post_comment` | 업무 댓글 수정 |
| `delete_post_comment` | 업무 댓글 삭제 |

### 위키 (11개)
| 도구 | 설명 |
|------|------|
| `get_wiki_list` | 위키 목록 조회 |
| `get_child_wiki_list` | 하위 페이지 목록 조회 |
| `get_personal_wiki` | 개인 위키 조회 |
| `get_wiki_page_content` | 페이지 내용 조회 (wiki_id + page_id) |
| `get_wiki_page_by_id` | 페이지 내용 조회 (page_id만으로) |
| `create_wiki` | 위키 페이지 생성 |
| `modify_wiki_page` | 위키 페이지 수정 |
| `upload_file_to_wiki` | 위키에 파일 업로드 |
| `get_wiki_page_comments` | 위키 댓글 조회 |
| `create_wiki_page_comment` | 위키 댓글 작성 |
| `update_wiki_page_comment` | 위키 댓글 수정 |
| `delete_wiki_page_comment` | 위키 댓글 삭제 |

### 메신저 (5개)
| 도구 | 설명 |
|------|------|
| `get_channels_belongs_to` | 내가 속한 채널 목록 |
| `send_message_to_member_directly` | 1:1 메시지 전송 |
| `send_message_to_channel` | 채널에 메시지 전송 |
| `modify_message_sent_to_channel` | 채널 메시지 수정 |
| `delete_message_sent_to_channel` | 채널 메시지 삭제 |

### 드라이브 (4개)
| 도구 | 설명 |
|------|------|
| `get_drive_list` | 드라이브 목록 조회 |
| `get_folder_list_in_drive` | 폴더 목록 조회 |
| `upload_file_to_drive` | 파일 업로드 |
| `upload_not_file_content_to_drive` | 텍스트 콘텐츠 업로드 |

## 설정

### Claude Code 설정 (~/.claude/settings.json)

```json
{
  "mcpServers": {
    "dooray-mcp": {
      "command": "/Users/nhn/init/mcp/dooray-mcp/.venv/bin/python",
      "args": [
        "/Users/nhn/init/mcp/dooray-mcp/main.py"
      ],
      "env": {
        "DOORAY_API_KEY": "your-api-key",
        "DOORAY_BASE_URL": "https://api.dooray.com"
      }
    }
  }
}
```

### API 키 발급

1. **Dooray 접속**: https://nhnent.dooray.com
2. **설정 → 개인 설정 → API 키 관리**
3. **API 키 생성** 클릭
4. 발급된 키를 settings.json의 `DOORAY_API_KEY`에 설정

## 사용 예시

### 캘린더
```
# 내 캘린더 목록
내 캘린더 목록 보여줘

# 이번 주 일정 조회
이번 주 일정 보여줘

# 일정 생성
내일 오후 2시에 "회의" 일정 등록해줘
```

### 위키 댓글
```
# 댓글 조회
위키 페이지 댓글 보여줘 (wiki_id, page_id 필요)

# 댓글 작성
위키에 "테스트 댓글입니다" 댓글 달아줘

# 댓글 삭제
위키 댓글 전부 삭제해줘
```

### 업무
```
# 내 업무 조회
내 담당 업무 보여줘

# 업무 상세 조회
업무 상세 내용 보여줘 (project_id, post_id 필요)
```

## 주요 ID 정보

| 항목 | ID |
|------|-----|
| @zman 개인 위키 | `3051057878725260241` |
| claude code 페이지 | `4248918788553579171` |
| 내 기본 캘린더 | `3051057880790584417` |
| 포커서버팀 캘린더 | `3842792407803282659` |

## 트러블슈팅

### MCP 서버 실행 확인
```bash
cd ~/init/mcp/dooray-mcp
DOORAY_API_KEY="your-key" .venv/bin/python main.py
```

### API 테스트
```bash
curl -H "Authorization: dooray-api YOUR_API_KEY" \
  "https://api.dooray.com/calendar/v1/calendars"
```

### 도구 목록 확인
```bash
cd ~/init/mcp/dooray-mcp
DOORAY_API_KEY="your-key" .venv/bin/python -c "
from server.server import tools
from utils import pyloader
pyloader.import_all_modules_from('adapter')
pyloader.import_all_modules_from('context')
print('도구 목록:', list(tools.keys()))
"
```

## 참고

- **소스 코드**: `~/init/mcp/dooray-mcp`
- **adapter**: API 호출 로직
- **context**: MCP 도구 등록
- **model**: 요청/응답 모델

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-01-23 | 업무/위키 ID만으로 조회 기능 추가 (get_detail_of_task_by_id, get_wiki_page_by_id) |
| 2026-01-23 | 업무 전체 상세 조회 추가 (get_full_detail_of_task, get_full_detail_of_task_by_id) |
| 2026-01-23 | 업무 상태 변경 추가 (set_post_workflow, set_post_done) |
| 2026-01-23 | 업무 댓글 CRUD 추가 (get/create/update/delete_post_comment) |
| 2026-01-22 | 위키 댓글 API 경로 수정 (/logs → /comments) |
| 2026-01-22 | 캘린더 기능 테스트 및 문서화 |
