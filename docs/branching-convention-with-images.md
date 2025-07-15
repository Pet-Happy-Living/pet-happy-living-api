# GitHub Branching Name Best Practices

## 1. Prefixes로 브랜치 목적 명시
다음과 같은 접두사를 사용해 브랜치의 목적을 한눈에 알 수 있도록 합니다:

- `feature/`: 신규 기능
- `bugfix/`: 버그 수정
- `hotfix/`: 긴급 수정 (주로 프로덕션 대응)
- `design/`: UI/UX 변경
- `refactor/`: 기능 변경 없이 코드 구조 정리
- `test/`: 테스트 코드 작성/개선
- `doc/`: 문서 업데이트

### 예시
```
feature/user-authentication
bugfix/fix-login-error
hotfix/urgent-patch-crash
design/update-navbar
refactor/remove-unused-code
test/add-unit-tests
doc/update-readme
```

![Git Commit Types](./https___dev-to-uploads.s3.amazonaws.com_uploads_articles_68kturf7t2eg7nufsyws.png)

---

## 2. 간결하지만 설명적인 이름 사용
브랜치 이름은 짧고 명확해야 합니다.

- 단어 사이엔 하이픈(`-`) 사용
- `update`, `changes`, `stuff`처럼 애매한 용어는 피함
- 핵심 작업 내용 중심으로 작성

### 예시
```
feature/add-user-profile
feature/implement-chat-notifications
bugfix/correct-date-display
bugfix/fix-404-error
design/improve-dashboard-ui
design/revise-mobile-layout
refactor/optimize-database-queries
refactor/simplify-api-routes
hotfix/security-patch
hotfix/fix-login-issue
doc/add-api-instructions
doc/update-contributor-guidelines
```

![Effective Branch Names](./https___dev-to-uploads.s3.amazonaws.com_uploads_articles_8bzblesluvtrl0y7aefh.png)

---

## 3. 티켓 번호 포함으로 추적 용이
Jira, Trello 같은 도구를 사용하는 경우 이슈/티켓 번호를 브랜치 이름에 포함하면 좋습니다.

### 예시
```
feature/JIRA-1234-add-login
bugfix/TICKET-567-resolve-crash
hotfix/ISSUE-890-fix-api
```

![Ticket Tracking](./https___dev-to-uploads.s3.amazonaws.com_uploads_articles_6imiq5shnrn5lm9rba1p.png)

---

## 4. 팀 내 naming 전략 협의
공통의 브랜치 네이밍 전략을 팀 전체에 공유 후 `.github/CONTRIBUTING.md` 또는 `README.md` 등에 문서화합니다.

---

## 🌟 일관된 네이밍의 장점
- 협업 강화: 브랜치명만 보고도 목적을 쉽게 파악 가능  
- 탐색 용이: 특정 브랜치 검색이 간편  
- CI/CD 자동화 활용: 브랜치명 기반 자동 배포 등 가능  
([원문 링크 - dev.to](https://dev.to/jps27cse/github-branching-name-best-practices-49ei?utm_source=chatgpt.com))

---

## 📘 브랜칭 전략 시각화

![Branching Strategy](./https___dev-to-uploads.s3.amazonaws.com_uploads_articles_keeyuo9xptnc2rh24sss.png)