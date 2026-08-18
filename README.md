#  국내 여행 추천 CLI 프로그램

> OpenAI API와 Kakao Local API를 활용한 국내 여행지 및 주변 맛집 추천 CLI 애플리케이션

이 프로젝트는 사용자가 입력한 여행 날짜를 기준으로 국내 여행지를 추천하고, 각 여행지 주변의 맛집 정보를 함께 제공하는 Python 기반 CLI 프로그램입니다.

OpenAI API를 이용해 여행지 추천 데이터를 생성하고, Kakao Local API를 이용해 추천 여행지 주변의 맛집 정보를 검색합니다.  
최종 결과는 JSON 파일과 Markdown 리포트 파일로 저장됩니다.

또한 OpenAI API 크레딧 부족, 네트워크 오류, 응답 형식 오류 등 외부 API 사용 중 발생할 수 있는 문제를 고려하여 **샘플 데이터 폴백 처리**를 구현했습니다.

---

##  프로젝트 개요

본 프로젝트는 단순한 API 호출 예제가 아니라, 실제 CLI 프로그램의 기본 구조를 갖추는 것을 목표로 제작되었습니다.

사용자는 날짜만 입력하면 다음과 같은 여행 추천 정보를 받을 수 있습니다.

- 추천 여행지
- 지역 정보
- 추천 이유
- 당일 여행 코스
- 여행 팁
- 주변 맛집 정보
- JSON 결과 파일
- Markdown 리포트 파일

---

##  주요 기능

| 기능 | 설명 |
|---|---|
| CLI 실행 | `argparse`를 사용하여 명령줄에서 날짜 입력 |
| 날짜 기반 추천 | 사용자가 입력한 날짜를 기준으로 여행 추천 실행 |
| OpenAI 여행지 추천 | OpenAI API를 활용해 국내 여행지 추천 데이터 생성 |
| API 재시도 처리 | OpenAI 응답 실패 시 최대 3회 재시도 |
| 폴백 데이터 처리 | OpenAI 크레딧 부족 또는 오류 발생 시 샘플 여행지 데이터 사용 |
| Kakao 맛집 검색 | Kakao Local API를 활용해 여행지 주변 맛집 검색 |
| 결과 파일 저장 | 추천 결과를 JSON 파일로 저장 |
| Markdown 리포트 생성 | 사람이 읽기 쉬운 Markdown 형식의 여행 리포트 생성 |
| 폴더 자동 생성 | `results` 폴더가 없으면 자동 생성 |
| 환경변수 관리 | `.env` 파일을 사용하여 API 키 보안 관리 |

---

##  사용 기술

- Python
- argparse
- requests
- python-dotenv
- OpenAI API
- Kakao Local API
- JSON
- Markdown

---

##  프로젝트 구조

```text
2-2st-VSCode02/
│
├─ main.py
├─ README.md
├─ requirements.txt
├─ .env.example
├─ .gitignore
│
└─ results/
   ├─ travel_YYYY-MM-DD_YYYYMMDD_HHMMSS.json
   └─ travel_YYYY-MM-DD_YYYYMMDD_HHMMSS.md
```

---

##  설치 방법

프로젝트 폴더에서 아래 명령어를 실행하여 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

`requirements.txt` 예시:

```txt
openai
python-dotenv
requests
```

---

##  환경변수 설정

프로젝트 루트 경로에 `.env` 파일을 생성한 뒤, 아래 내용을 입력합니다.

```env
OPENAI_API_KEY=your_openai_api_key
KAKAO_REST_API_KEY=your_kakao_rest_api_key
```

실제 API 키는 보안상 `.env` 파일에만 저장해야 합니다.  
`.env` 파일은 제출하거나 GitHub에 업로드하지 않습니다.

대신 예시 파일인 `.env.example`을 함께 제공합니다.

```env
OPENAI_API_KEY=your_openai_api_key
KAKAO_REST_API_KEY=your_kakao_rest_api_key
```

---

##  실행 방법

아래 명령어로 프로그램을 실행합니다.

```bash
python main.py -date 2026-08-20
```

###  실행 옵션

| 옵션 | 필수 여부 | 설명 | 예시 |
|---|---|---|---|
| `-date` | 필수 | 여행 날짜 입력 | `2026-08-20` |

---

##  프로그램 동작 흐름

프로그램은 다음 순서로 실행됩니다.

```text
1. 사용자가 -date 옵션으로 여행 날짜 입력
2. .env 파일에서 OpenAI API Key와 Kakao REST API Key 로드
3. OpenAI API를 호출하여 국내 여행지 추천 요청
4. OpenAI 응답 실패 시 최대 3회 재시도
5. 3회 모두 실패하거나 크레딧 부족 오류 발생 시 샘플 여행지 데이터 사용
6. 각 여행지명을 기준으로 Kakao Local API에서 주변 맛집 검색
7. 추천 여행지 + 맛집 정보를 하나의 데이터로 정리
8. results 폴더 자동 생성
9. JSON 파일 저장
10. Markdown 리포트 저장
```

---

##  OpenAI API 예외 처리 및 폴백 구조

이 프로젝트에서는 OpenAI API 호출이 실패해도 프로그램이 중단되지 않도록 예외 처리를 구현했습니다.

OpenAI API는 다음과 같은 이유로 실패할 수 있습니다.

- API 크레딧 부족
- 사용량 한도 초과
- 네트워크 오류
- 일시적인 서버 오류
- JSON 응답 형식 오류
- API 키 설정 오류

특히 개발 과정에서 OpenAI 크레딧 부족 문제가 발생할 수 있기 때문에, 해당 상황에서도 프로그램의 전체 흐름을 확인할 수 있도록 샘플 데이터를 사용한 폴백 로직을 추가했습니다.

###  폴백 처리 방식

OpenAI API 호출이 실패하면 즉시 프로그램을 종료하지 않고 최대 3회까지 재시도합니다.

```text
OpenAI API 호출
   ↓
응답 성공 → 추천 여행지 데이터 사용
   ↓
응답 실패 → 최대 3회 재시도
   ↓
3회 실패 또는 크레딧 부족 발생
   ↓
샘플 여행지 데이터 사용
   ↓
Kakao 맛집 검색 계속 진행
   ↓
JSON / Markdown 결과 저장
```

이 구조 덕분에 OpenAI API를 사용할 수 없는 상황에서도 Kakao API 연동, 결과 저장, Markdown 리포트 생성 기능을 정상적으로 확인할 수 있습니다.

---

##  샘플 데이터 폴백 예시

OpenAI API가 실패할 경우 다음과 같은 샘플 여행지 데이터를 사용합니다.

```text
- 전주 한옥마을
- 강릉 안목해변
- 경주 황리단길
```

이 샘플 여행지들을 기준으로 Kakao Local API를 호출하여 주변 맛집 정보를 검색합니다.

즉, OpenAI 추천 생성은 실패하더라도 이후 과정은 계속 진행됩니다.

```text
샘플 여행지 데이터
   ↓
Kakao Local API 맛집 검색
   ↓
JSON 파일 저장
   ↓
Markdown 리포트 저장
```

---

##  실행 결과

프로그램 실행이 완료되면 `results` 폴더에 결과 파일이 생성됩니다.

```text
results/
├─ travel_2026-08-20_20260818_125743.json
└─ travel_2026-08-20_20260818_125743.md
```
<img width="927" height="433" alt="main 실행 샷" src="https://github.com/user-attachments/assets/e49802f5-1ade-458b-9a94-ea31be013a86" />


###  JSON 파일

JSON 파일은 여행지 추천 결과와 맛집 정보를 구조화된 데이터 형태로 저장합니다.

포함 정보 예시:

- 여행 날짜
- 추천 여행지 목록
- 지역
- 추천 이유
- 당일 코스
- 여행 팁
- 주변 맛집 목록
- 맛집 주소
- Kakao 장소 URL

###  Markdown 파일

Markdown 파일은 사람이 읽기 쉬운 여행 리포트 형식으로 저장됩니다.

포함 정보 예시:

- 여행 날짜
- 추천 여행지
- 추천 이유
- 당일 여행 코스
- 여행 팁
- 주변 맛집 정보

---

##  Markdown 리포트 예시

```md
#  국내 여행 추천 리포트

##  여행 날짜
2026-08-20

##  1. 전주 한옥마을

###  추천 이유
전통 한옥과 다양한 먹거리를 함께 즐길 수 있는 대표적인 국내 여행지입니다.

###  당일 코스
전주 한옥마을 → 경기전 → 전동성당 → 남부시장

###  여행 팁
도보 이동이 편리하며, 주말에는 방문객이 많기 때문에 오전 방문을 추천합니다.

###  주변 맛집
- 가족회관
- 베테랑 칼국수
- 현대옥
```

---

##  보안 관련 주의사항

API 키는 외부에 공개되면 안 되는 민감한 정보입니다.  
따라서 실제 API 키는 코드에 직접 작성하지 않고 `.env` 파일에서 관리합니다.

제출 또는 GitHub 업로드 시 포함하면 안 되는 파일:

```text
.env
__pycache__/
*.pyc
```

권장 `.gitignore` 설정:

```gitignore
.env
__pycache__/
*.pyc
```

만약 실행 결과 파일까지 제출해야 한다면 `results/`는 `.gitignore`에 포함하지 않습니다.

---

##  제출 파일 구성

최종 제출 시 권장 파일 구성은 다음과 같습니다.

```text
main.py
README.md
requirements.txt
.env.example
.gitignore
results/
```

제출하지 않는 파일:

```text
.env
__pycache__/
*.pyc
```

---

##  프로젝트에서 중점적으로 구현한 부분

이 프로젝트에서는 다음 구현 요소에 집중했습니다.

1. CLI 인자 처리  
   - `argparse`를 사용하여 `-date` 옵션 필수 입력 처리

2. 환경변수 관리  
   - `python-dotenv`를 사용하여 API 키를 안전하게 분리

3. OpenAI API 연동  
   - 여행지 추천 데이터를 JSON 형태로 생성

4. OpenAI API 오류 대응  
   - API 호출 실패 시 최대 3회 재시도
   - 크레딧 부족 등 오류 발생 시 샘플 데이터로 대체

5. Kakao Local API 연동  
   - 추천 여행지 주변 맛집 정보 검색

6. 결과 저장  
   - JSON 파일 저장
   - Markdown 리포트 자동 생성

7. 제출용 프로젝트 정리  
   - `.env.example`
   - `.gitignore`
   - `requirements.txt`
   - `README.md`

---

##  실행 예시

```bash
python main.py -date 2026-08-20
```

실행 중 출력 예시:

```text
여행 날짜: 2026-08-20
OpenAI 여행지 추천 생성 중...
OpenAI API 호출 실패 또는 크레딧 부족 발생
샘플 여행지 데이터를 사용합니다.
Kakao 맛집 검색 중...
JSON 파일 저장 완료
Markdown 리포트 저장 완료
```

---
“파이썬 CLI 프로그램을 실행한 뒤 자동 생성된 여행 추천 Markdown 리포트 파일을 Windows 메모장에서 열어 확인한 화면입니다.”


<img width="900" height="735" alt="리포트 파일01" src="https://github.com/user-attachments/assets/12737047-3092-40ae-9547-d13689b9f819" />
<img width="910" height="857" alt="리포트 파일02" src="https://github.com/user-attachments/assets/46c21879-51e6-40fa-a6e0-5e05cfe2db8d" />
<img width="915" height="765" alt="리포트 파일03" src="https://github.com/user-attachments/assets/f8052bc7-4506-4c42-936b-93e4c08f9b78" />


##  프로젝트 요약

본 프로젝트는 사용자가 입력한 날짜를 기준으로 국내 여행지를 추천하고, Kakao Local API를 통해 주변 맛집 정보를 검색한 뒤, 결과를 JSON과 Markdown 파일로 저장하는 Python CLI 애플리케이션입니다.

특히 OpenAI API 크레딧 부족이나 응답 실패 상황에서도 프로그램이 중단되지 않도록 샘플 데이터 폴백 로직을 구현하여, 외부 API 장애 상황에서도 전체 기능 흐름을 확인할 수 있도록 설계했습니다.
