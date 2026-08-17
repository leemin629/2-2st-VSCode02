from datetime import datetime
from pathlib import Path


def create_results_folder():
    """
    results 폴더가 없으면 생성하는 함수
    """
    results_path = Path("results")
    results_path.mkdir(exist_ok=True)
    return results_path


def input_date(message):
    """
    YYYY-MM-DD 형식의 날짜를 입력받고 검증하는 함수
    """
    while True:
        date_text = input(message)

        try:
            date = datetime.strptime(date_text, "%Y-%m-%d")
            return date
        except ValueError:
            print("날짜 형식이 올바르지 않습니다. 예: 2025-01-15")


def main():
    print("여행 추천 프로그램을 시작합니다.")
    print("-" * 30)

    destination = input("여행지를 입력하세요: ")
    purpose = input("여행 목적을 입력하세요 예) 맛집, 자연, 역사, 휴식: ")

    start_date = input_date("여행 시작일을 입력하세요 예) 2025-01-15: ")

    while True:
        end_date = input_date("여행 종료일을 입력하세요 예) 2025-01-17: ")

        if end_date >= start_date:
            break

        print("종료일은 시작일보다 빠를 수 없습니다.")

    results_path = create_results_folder()

    print()
    print("입력 정보 확인")
    print("-" * 30)
    print(f"여행지: {destination}")
    print(f"여행 목적: {purpose}")
    print(f"시작일: {start_date.strftime('%Y-%m-%d')}")
    print(f"종료일: {end_date.strftime('%Y-%m-%d')}")
    print(f"결과 저장 폴더: {results_path}")

    print()
    print("1차 기능 실행이 완료되었습니다.")


if __name__ == "__main__":
    main()