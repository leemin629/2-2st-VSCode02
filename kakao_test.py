import os
import requests
from dotenv import load_dotenv

load_dotenv()

kakao_key = os.getenv("KAKAO_REST_API_KEY")

print("Kakao key loaded:", bool(kakao_key))
print("Kakao key length:", len(kakao_key) if kakao_key else 0)

url = "https://dapi.kakao.com/v2/local/search/keyword.json"

headers = {
    "Authorization": f"KakaoAK {kakao_key}"
}

params = {
    "query": "전주 한옥마을 맛집",
    "size": 3
}

response = requests.get(url, headers=headers, params=params)

print("status code:", response.status_code)
print(response.text[:1000])