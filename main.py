import os
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv
from openai import OpenAI


# =========================
# 환경변수 로드
# =========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


# =========================
# 날짜 검증 함수
# =========================
def validate_date(date_text: str) -> str:
    """
    YYYY-MM-DD 형식인지 확인하는 함수
    """
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        raise ValueError("날짜 형식은 YYYY-MM-DD 여야 합니다. 예: 2026-08-20")


# =========================
# OpenAI 여행 추천 생성
# =========================
def get_travel_recommendations(date: str, max_retries: int = 3) -> dict:
    """
    OpenAI에게 국내 여행지를 추천받고 JSON으로 반환
    실패하면 최대 max_retries번 재시도
    """

    system_prompt = """
너는 국내 여행 전문 가이드다.
사용자가 입력한 날짜에 맞춰 국내 여행지를 추천한다.
반드시 JSON 형식으로만 답변한다.
마크다운, 설명문, 코드블록은 절대 쓰지 않는다.
"""

    user_prompt = f"""
여행 날짜: {date}

아래 JSON 구조를 정확히 지켜서 국내 여행지 3곳을 추천해줘.

{{
  "date": "{date}",
  "recommendations": [
    {{
      "destination": "여행지 이름",
      "region": "시/도 및 시/군/구",
      "reason": "추천 이유",
      "one_day_course": ["코스1", "코스2", "코스3"],
      "food_keywords": ["맛집 검색 키워드1", "맛집 검색 키워드2"],
      "tips": ["팁1", "팁2"]
    }}
  ]
}}
"""

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[OpenAI] 여행 추천 생성 중... ({attempt}/{max_retries})")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            content = response.choices[0].message.content
            data = json.loads(content)

            if "recommendations" not in data:
                raise ValueError("JSON 안에 recommendations 키가 없습니다.")

            return data

        except Exception as e:
            print(f"[OpenAI] 오류 발생: {e}")
            if attempt < max_retries:
                print("[OpenAI] 잠시 후 재시도합니다...")
                time.sleep(2)
            else:
                raise RuntimeError("OpenAI 추천 생성에 실패했습니다.")


# =========================
# Kakao Local API 맛집 검색
# =========================
def search_kakao_restaurants(query: str, size: int = 3) -> list:
    """
    Kakao Local API로 맛집 검색
    실패해도 프로그램은 멈추지 않고 빈 리스트 반환
    """

    if not KAKAO_REST_API_KEY:
        print("[Kakao] API 키가 없습니다. 맛집 검색을 건너뜁니다.")
        return []

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }

    params = {
        "query": query,
        "size": size
    }

    try:
        print(f"[Kakao] 맛집 검색 중: {query}")

        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()

        result = response.json()
        documents = result.get("documents", [])

        restaurants = []

        for item in documents:
            restaurants.append({
                "name": item.get("place_name"),
                "category": item.get("category_name"),
                "address": item.get("road_address_name") or item.get("address_name"),
                "phone": item.get("phone"),
                "url": item.get("place_url"),
            })

        return restaurants

    except Exception as e:
        print(f"[Kakao] 검색 실패: {e}")
        return []


# =========================
# 추천 데이터에 맛집 정보 추가
# =========================
def add_restaurants_to_recommendations(data: dict) -> dict:
    """
    OpenAI 추천 결과에 Kakao 맛집 검색 결과를 붙임
    """

    for rec in data.get("recommendations", []):
        region = rec.get("region", "")
        destination = rec.get("destination", "")

        query = f"{region} {destination} 맛집"
        restaurants = search_kakao_restaurants(query)

        rec["restaurants"] = restaurants

    return data


# =========================
# Markdown 리포트 생성
# =========================
def create_markdown_report(data: dict) -> str:
    """
    최종 여행 리포트를 Markdown 문자열로 생성
    """

    lines = []

    lines.append(f"# 국내 여행 추천 리포트")
    lines.append("")
    lines.append(f"- 여행 날짜: `{data.get('date')}`")
    lines.append("")

    for idx, rec in enumerate(data.get("recommendations", []), start=1):
        lines.append(f"## {idx}. {rec.get('destination')}")
        lines.append("")
        lines.append(f"**지역:** {rec.get('region')}")
        lines.append("")
        lines.append(f"**추천 이유:** {rec.get('reason')}")
        lines.append("")

        lines.append("### 당일 코스")
        for course in rec.get("one_day_course", []):
            lines.append(f"- {course}")
        lines.append("")

        lines.append("### 여행 팁")
        for tip in rec.get("tips", []):
            lines.append(f"- {tip}")
        lines.append("")

        lines.append("### 주변 맛집")
        restaurants = rec.get("restaurants", [])

        if restaurants:
            for r in restaurants:
                lines.append(f"- **{r.get('name')}**")
                lines.append(f"  - 분류: {r.get('category')}")
                lines.append(f"  - 주소: {r.get('address')}")
                lines.append(f"  - 전화: {r.get('phone') or '정보 없음'}")
                lines.append(f"  - 링크: {r.get('url')}")
        else:
            lines.append("- 맛집 정보를 찾지 못했습니다.")

        lines.append("")

    return "\n".join(lines)


# =========================
# 결과 저장
# =========================
def save_results(data: dict, markdown: str) -> None:
    """
    results 폴더에 JSON과 Markdown 저장
    """

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    date_text = data.get("date", "unknown")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_path = results_dir / f"travel_{date_text}_{timestamp}.json"
    md_path = results_dir / f"travel_{date_text}_{timestamp}.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print("")
    print("[저장 완료]")
    print(f"JSON 파일: {json_path}")
    print(f"Markdown 파일: {md_path}")



def get_mock_recommendations(date: str) -> dict:
    """
    OpenAI 크레딧이 없을 때 테스트용으로 쓰는 샘플 여행 추천 데이터
    """
    return {
        "date": date,
        "recommendations": [
            {
                "destination": "전주 한옥마을",
                "region": "전라북도 전주시",
                "reason": "한옥 거리, 전통 음식, 산책 코스를 함께 즐기기 좋습니다.",
                "one_day_course": ["전주 한옥마을", "경기전", "남부시장"],
                "food_keywords": ["전주 비빔밥", "전주 콩나물국밥"],
                "tips": ["주말에는 사람이 많으니 오전 방문을 추천합니다.", "도보 이동이 많아 편한 신발이 좋습니다."]
            },
            {
                "destination": "강릉 안목해변",
                "region": "강원도 강릉시",
                "reason": "바다 풍경과 카페거리를 함께 즐길 수 있는 여행지입니다.",
                "one_day_course": ["안목해변", "강릉 카페거리", "중앙시장"],
                "food_keywords": ["강릉 커피", "강릉 장칼국수"],
                "tips": ["바닷바람이 강할 수 있어 겉옷을 챙기세요.", "일몰 시간대 방문도 좋습니다."]
            },
            {
                "destination": "경주 황리단길",
                "region": "경상북도 경주시",
                "reason": "역사 유적과 감성적인 거리 구경을 함께 할 수 있습니다.",
                "one_day_course": ["황리단길", "첨성대", "동궁과 월지"],
                "food_keywords": ["경주 한식", "황리단길 맛집"],
                "tips": ["야경 명소가 많아 오후 늦게까지 일정 잡기 좋습니다.", "사진 찍기 좋은 장소가 많습니다."]
            }
        ]
    }

# =========================
# 메인 실행
# =========================
def main():
    parser = argparse.ArgumentParser(description="국내 여행 추천 CLI 프로그램")

    parser.add_argument(
        "-date",
        required=True,
        help="여행 날짜를 YYYY-MM-DD 형식으로 입력하세요. 예: 2026-08-20"
    )

    args = parser.parse_args()

    try:
        travel_date = validate_date(args.date)

        try:
            data = get_travel_recommendations(travel_date)
        except Exception:
            print("[알림] OpenAI 크레딧 부족 또는 오류로 인해 샘플 데이터를 사용합니다.")
            data = get_mock_recommendations(travel_date)

        data = add_restaurants_to_recommendations(data)

        markdown = create_markdown_report(data)
        save_results(data, markdown)

        print("")
        print("여행 추천 리포트 생성이 완료되었습니다!")

    except Exception as e:
        print("")
        print("[오류 발생]")
        print(e)


if __name__ == "__main__":
    main()