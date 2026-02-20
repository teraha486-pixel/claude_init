# Docs 폴더 구조 및 규칙

## 주의사항
- `/Users/nhn/work/CLAUDE.md`는 팀원 공용 파일이므로 **수정 금지**
- 이 docs 폴더는 개인 기록용

## 폴더 구조

```
docs/
├── common/          # IDE 공통 설정 및 가이드 문서
│   ├── ccm-usage-setup.md           # CCM 사용량 설정
│   ├── claude-code-setup.md         # Claude Code 작업 규칙
│   ├── dooray-comment-rules.md      # 두레이 댓글 규칙
│   ├── dooray-mcp-guide.md          # Dooray MCP 사용 가이드
│   ├── dooray-mcp-server-build.md   # Dooray MCP 빌드 가이드
│   ├── elasticsearch-mcp-troubleshooting.md  # ES MCP 트러블슈팅
│   └── sync-gamedata-skill.md       # GameData 동기화 스킬 가이드
│
├── vscode/          # VS Code 설정 관련 문서
│   ├── environment-setup.md
│   ├── hangame-poker-server.md
│   ├── hangame-poker-server-intellij.md
│   ├── gia-poker.md
│   ├── gia-core.md
│   ├── gia-poker-admin.md
│   └── betting_base.md
│
├── intellij/        # IntelliJ 설정 관련 문서
│   └── gia-poker-admin-run.md
│
└── intel-mac/       # Intel Mac 전용 설정
    └── environment-setup.md
```

## 기록 규칙
- 트러블슈팅, 작업 기록은 해당 폴더에 md 파일로 작성
- IDE 설정 관련: vscode/, intellij/, common/
- 새로운 스킬/기능 추가 시: common/ 폴더에 가이드 작성
