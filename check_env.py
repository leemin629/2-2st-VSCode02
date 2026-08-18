import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
kakao_key = os.getenv("KAKAO_REST_API_KEY")

print("OpenAI key loaded:", bool(openai_key))
print("Kakao key loaded:", bool(kakao_key))