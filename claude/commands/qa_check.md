# 두레이 QA 업무 조회 스킬

이번 달 정기점검/업데이트 QA 업무 중 내가 담당자 또는 참조자로 등록된 미완료 업무를 조회한다.

## 기본 정보

- **member_id**: `2802458672652277190` (이태양)
- **QA 프로젝트 2개**:
  - pc포커-bts: `1567704068379919418`
  - 포커클래식-QA: `2378020467797929507`

## 조회 절차

### 1단계: 현재 월 확인

`get_date_time_now`로 현재 날짜를 확인하여 N월을 결정한다.

### 2단계: 프로젝트별 제목 검색

두 프로젝트에 대해 각각 `get_task_list_with_param`으로 검색한다.

```
project_id: 각 프로젝트 ID
task_query:
  subjects: "N월정기점검" 또는 "N월업데이트"
  postWorkflowClasses: "backlog,registered,working"
  size: 100
```

- 각 프로젝트 x 2개 키워드(정기점검/업데이트) = 총 4회 호출
- 결과에서 중복 제거 (동일 task ID)

### 3단계: 담당자/참조자 필터링

조회된 각 업무에 대해 `get_full_detail_of_task_by_id`로 상세 조회 후:
- **담당자(TO)**: `users.to[].member.organizationMemberId`에 내 member_id가 있는지 확인
- **참조자(CC)**: `users.cc[].member.organizationMemberId`에 내 member_id가 **직접** 포함되어 있는지 확인
- 그룹(group) CC는 무시 (그룹에 포함되어 있어도 직접 CC가 아니면 제외)

### 4단계: 결과 출력

테이블 형식으로 출력:

```
| # | 프로젝트 | 상태 | 역할 | 제목 |
|---|---------|------|------|------|
```

- 프로젝트명: pc포커-bts 또는 포커클래식-QA
- 역할: 담당자(TO) 또는 참조자(CC)
- 마지막에 총 건수 표시

## 주의사항

- `get_task_list_by_assignee_or_cc`는 200건 한도로 최근 업무가 누락될 수 있으므로 사용하지 않는다
- 반드시 프로젝트 단위 제목 검색 후 full detail 확인 방식을 사용한다
- 마일스톤이 null인 업무도 있으므로 마일스톤이 아닌 제목 기준으로 검색한다
