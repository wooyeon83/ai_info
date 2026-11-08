# AI_Learning_Digest

공식 기술 소식을 매일 수집하고 Notion에 저장하는 개인 학습 자동화입니다.
피드 10곳의 실제 수집과 로컬 테스트 11개를 검증했습니다. GitHub Actions 및 Notion 저장 검증은 진행 중입니다.

## 동작

- 매일 한국 시간 오전 8시 17분 예약 실행. 실행 시각은 GitHub 상황에 따라 지연될 수 있습니다.
- 글로벌 기술 출처 4곳과 네이버·카카오·라인(LY)·쿠팡·배달의민족·토스 기술 블로그 6곳에서 관련 항목 수집.
- 최근 14일 내 피드에 남아 있는 항목을 최신순으로 확인해 아직 저장하지 않은 항목 최대 3개 저장.
- 같은 원문 URL은 Notion의 항목 ID로 중복 방지. 기존 학습 상태는 수정하지 않습니다.
- 공식 피드가 제공한 본문·발췌를 사용하며, 웹 전체 검색이나 전체 기사 본문 수집은 하지 않습니다.
- 원문 발췌 모드가 기본입니다. 한국어 AI 요약은 선택 설정이며 추가 API 비용이 발생합니다.
- 저장 항목: 제목, 원문, 게시일, 수집일, 핵심 변화, 업무 활용 제안, 작은 실습 제안, 확인할 점, 학습 상태.
- 소식이 없으면 빈 페이지를 만들지 않습니다. 소스 일부 실패 시 나머지를 처리하고 실행 결과를 실패로 표시합니다.
- 실행 결과는 Actions 요약과 14일 보관 아티팩트에 남습니다. 별도 이메일·메신저 발송은 없습니다.

## 공식 수집 출처

설정 원본: `sources.json`. 현재 구성은 글로벌 기술 출처 4곳과 국내 기업 기술 블로그 6곳, 총 10곳입니다.

| 출처 | 수집 피드 | 범위 |
| --- | --- | --- |
| [Claude Code 공식 릴리스](https://github.com/anthropics/claude-code/releases) | https://github.com/anthropics/claude-code/releases.atom | 새 기능, 변경 사항, 버그 수정 |
| [MCP Python SDK 공식 릴리스](https://github.com/modelcontextprotocol/python-sdk/releases) | https://github.com/modelcontextprotocol/python-sdk/releases.atom | 에이전트 도구 연결용 Python SDK 변경 사항 |
| [LangGraph 공식 릴리스](https://github.com/langchain-ai/langgraph/releases) | https://github.com/langchain-ai/langgraph/releases.atom | 에이전트 워크플로 프레임워크 변경 사항 |
| [Hugging Face 공식 블로그](https://huggingface.co/blog) | https://huggingface.co/blog/feed.xml | 제목·발췌에 agent, tool calling, mcp, evaluation, rag 중 하나가 포함된 글 |

| [NAVER D2](https://d2.naver.com/) | https://d2.naver.com/d2.atom | AI·데이터 기술과 실무 사례 |
| [Kakao Tech](https://tech.kakao.com/) | https://tech.kakao.com/feed/ | AI·에이전트 활용 및 데이터 운영 사례 |
| [LY Corporation Tech Blog](https://techblog.lycorp.co.jp/ko) | https://techblog.lycorp.co.jp/ko/feed/index.xml | LINE 계열의 한국어 기술·운영 사례 |
| [Coupang Engineering](https://medium.com/coupang-engineering) | https://medium.com/feed/coupang-engineering | AI·데이터 인프라 및 엔지니어링 사례 |
| [우아한형제들 기술블로그](https://techblog.woowahan.com/) | https://techblog.woowahan.com/feed/ | 배달의민족의 AI·데이터 및 개발 생산성 사례 |
| [Toss Tech](https://toss.tech/) | https://toss.tech/rss.xml | 토스의 AI·데이터 및 개발 생산성 사례 |

국내 블로그는 제목·발췌에서 다음 키워드 중 하나가 확인되는 글을 수집합니다: AI, LLM, 에이전트, agent, agentic, Claude, MCP, RAG, 프롬프트, 생성형, 데이터 엔지니어링, data engineering, Spark, Kafka, Airflow, Databricks, 데이터 파이프라인, 데이터 플랫폼.
짧은 영문 키워드는 단어 경계로 구분해 mail 같은 단어가 AI로 잘못 분류되지 않도록 합니다.
기업의 공개 실무 사례이며 제품 기능 명세와는 성격이 다릅니다. 2026-11-08 실제 수집에서 10곳 모두 정상 응답·파싱을 확인했습니다. 쿠팡 피드의 XML 제어문자를 정리하도록 파서를 보완했습니다.

공식 피드의 본문·발췌를 사용합니다. 웹 전체 검색이나 기사 전체 본문 수집은 하지 않습니다.
최근 14일 범위에서 미저장 항목을 최신순으로 최대 3개 선택합니다. 중요도를 AI로 순위화하는 구성은 아닙니다.
각 저장 항목에 출처와 원문 링크를 남깁니다. 공식 출처라도 요약·활용 제안은 사용자 검증 전 초안입니다.
2026-11-08 로컬 실제 피드 수집은 10곳 성공, 최근 14일 후보 33개·오류 0개입니다. GitHub Actions 및 실제 Notion 저장은 아직 미검증입니다.



## 1. GitHub에 코드 올리기

사용자 저장소: `https://github.com/wooyeon83/ai_info`

이 폴더 **안의 파일**을 해당 저장소 최상위에 올립니다. 상위 CareerTransition 폴더나 이력서는 올리지 않습니다.
`.github/workflows/daily-digest.yml`이 저장소 최상위 `.github/workflows/`에 있어야 예약이 인식됩니다.

Mac 터미널에서 로그인:

```sh
gh auth login --hostname github.com --git-protocol https --web
gh auth status
```

로그인 후 기존 저장소를 별도 위치에 clone하고 이 폴더의 코드만 복사한 뒤 커밋·push합니다.
빈 저장소와 기존 파일이 있는 저장소를 구분해 기존 내용을 보존하세요. 예약은 기본 브랜치에 워크플로가 있어야 작동합니다.

## 2. Notion 연결

이미 생성한 데이터베이스:

- [AI·에이전트 학습 소식](https://app.notion.com/p/6a521ccfdcd14d51811052f14efeaa3d)
- 데이터 소스 ID: `967bda67-5ca6-46d0-b95d-2c4b6163ff25`

Notion에서 개인용 내부 integration을 만들고 **콘텐츠 읽기·추가** 권한을 설정합니다.
데이터베이스의 연결 메뉴에서 그 integration에 접근을 허용합니다.
이 대화의 Notion 플러그인 인증과 GitHub Actions의 인증은 별개입니다.
토큰은 채팅이나 저장소 코드에 붙이지 않고 아래 GitHub Secret에 입력합니다.

GitHub 저장소 → Settings → Secrets and variables → Actions:

| 구분 | 이름 | 값 |
| --- | --- | --- |
| Secret | `NOTION_TOKEN` | 위에서 만든 Notion integration 토큰 |
| Variable | `NOTION_DATA_SOURCE_ID` | `967bda67-5ca6-46d0-b95d-2c4b6163ff25` |
| Variable | `SUMMARY_MODE` | `off` (기본) 또는 `anthropic` |
| Variable | `DIGEST_ENABLED` | 검증 전 미설정 또는 `false`. 실제 저장·중복 방지 검증 후 `true` |

`DIGEST_ENABLED`가 `true`일 때만 예약 실행합니다. 수동 실행은 이 값과 관계없이 가능합니다.
최초 배포 때는 `SUMMARY_MODE=off`로 두고 아래 최초 검증을 마친 뒤 예약을 활성화합니다.

## 3. 한국어 AI 요약 켜기 (선택)

| 구분 | 이름 | 값 |
| --- | --- | --- |
| Secret | `ANTHROPIC_API_KEY` | 개인 Anthropic API 키 |
| Variable | `ANTHROPIC_MODEL` | 해당 API 계정에서 사용할 수 있는 모델 ID |
| Variable | `SUMMARY_MODE` | `anthropic` |

Claude 구독의 포함 여부를 추정하지 말고 API 계정의 결제·사용 가능 모델·지출 한도를 확인합니다.
소식 하나당 API 1회, 정상 실행에서 하루 최대 3회 호출합니다. 수동 재실행과 실패 후 재시도에는 추가 비용이 들 수 있습니다.
입력 발췌는 항목당 최대 10,000자, 출력은 최대 1,000토큰입니다. 비용의 정확한 상한은 모델과 계정에서 별도 관리합니다.
원문은 명령이 아닌 데이터로 전달하며 모델에 외부 도구 권한을 주지 않습니다. 요약은 검증 전 AI 초안으로 표시합니다.

`off` 모드로 저장한 항목은 나중에 AI 모드를 켜도 자동 재요약하지 않습니다.
사용자가 읽음·실습 등으로 수정한 기록을 보호하기 위해 기존 항목은 건드리지 않습니다.

## 4. 최초 검증

1. Actions → Daily AI learning digest → Run workflow에서 `dry_run` 체크 상태로 실행합니다.
2. 실행 성공과 `report.json`의 피드별 수집 결과·미리보기를 확인합니다. 이 단계는 AI 및 Notion API를 호출하지 않습니다.
3. Secrets·Variables 설정 후 `dry_run` 체크를 해제해 실행합니다.
4. Notion에 새 항목이 생기고 학습 상태가 미확인인지 확인합니다.
5. 한 번 더 실행해 같은 원문이 중복되지 않는지 확인합니다. 아직 미저장 항목이 있으면 다음 최대 3개가 추가되는 것이 정상입니다.

이 단계까지 통과해야 실제 연동 완료입니다. 로컬 테스트만으로 원격 연동 완료라고 보지 않습니다.

## 개발·제한

Python 3.12 이상, 외부 패키지 설치 없이 실행합니다.

```sh
python3 -m unittest discover -s tests -v
DRY_RUN=true python3 digest.py
```

네트워크가 필요한 명령은 인터넷 접근 가능한 환경에서 실행해야 합니다.
피드 보관 수와 14일 조회 범위 밖의 소식은 복구하지 않으며, 하루 3개 제한으로 모든 소식을 보관하지는 않습니다.
같은 URL의 원문 수정은 새 항목으로 보지 않습니다. 출처나 구조가 바뀌면 sources.json과 파서를 조정합니다.
정확히 정시에 실행되는 알림 시스템은 아닙니다. GitHub의 실행 지연·사용량 정책이 적용되며,
공개 저장소는 활동이 60일 없으면 예약 실행이 비활성화될 수 있습니다. 정기적으로 Actions 상태를 확인합니다.

## 공식 참고

- [GitHub 예약 실행](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [Notion 데이터 소스 조회](https://developers.notion.com/reference/query-a-data-source)
- [Notion integration 생성](https://www.notion.so/profile/integrations)
- [Claude Messages API](https://platform.claude.com/docs/en/api/messages/create)
