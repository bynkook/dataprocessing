import pandas as pd
import csv
import json

"""
TAB으로 구분된 파일을 CSV로 변환하고, CSV를 JSON으로 변환하는 스크립트입니다.
이 스크립트는 다음 단계를 수행합니다:
    1. TAB으로 구분된 파일을 읽어들입니다.
    2. 각 셀에서 콤마를 제거하고 그것이 숫자인 경우 소수점 이하가 0이면 정수로 변환하여 저장함.
    3. 변환된 데이터를 CSV 파일로 저장합니다.
    4. CSV 파일을 formatted JSON 파일로 변환합니다.
"""

tab_file = "ChangeVOClaimList.txt"
csv_file = "ChangeVOClaimList_converted.csv"
json_file = "ChangeVOClaimList_converted_json_formatted.json"


def convert_commas(value):
    '''모든 셀을 검사하여 천단위 콤마가 있는 숫자를 변환'''
    if isinstance(value, str) and value.replace(',', '').isdigit():  # 천단위 콤마 제거 후 숫자인지 확인
        return float(value.replace(',', ''))  # 숫자로 변환
    return value  # 숫자가 아니면 그대로 유지

def format_numbers(value):
    '''소수점이 있는 숫자 중에서 .0으로 끝나는 경우 정수로 변환'''
    if isinstance(value, float) and value.is_integer():  # float 값이 정수인지 확인
        return int(value)  # 정수로 변환
    return value  # 그대로 유지

def csv_to_json(csv_filename, json_filename, indent=4):
    '''CSV 파일을 JSON 파일로 변환 (formatted)'''
    with open(csv_filename, 'r', encoding='utf-8') as csvf:
        reader = csv.DictReader(csvf)  # CSV의 각 행을 딕셔너리로 변환
        json_data = [row for row in reader]  # 리스트로 저장

    with open(json_filename, 'w', encoding='utf-8') as jsonf:
        json.dump(json_data, jsonf, indent=indent, ensure_ascii=False)  # 보기 좋은 JSON 저장
    print(f"{csv_filename} -> {json_filename} 변환 완료!")


# 파일 읽기 (TAB으로 구분된 데이터)
df = pd.read_csv(tab_file, sep='\t', dtype=str)  # 모든 데이터를 문자열로 읽음
df = df.map(convert_commas) # 천단위 콤마 제거후 숫자인지 확인
df = df.map(format_numbers) # 소수점 이하 0이면 정수로 변환하여 출력
# CSV 파일로 저장
df.to_csv(csv_file, index=False)
# JSON 파일로 저장
csv_to_json(csv_file, json_file)