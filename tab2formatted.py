import pandas as pd
import csv
import json
import os

"""
TAB으로 구분된 여러 파일을 CSV, JSON, Python dict(.py)로 일괄 변환하는 배치 스크립트.
jobfilelist.txt 내 파일들을 순차적으로 변환함.
TAB으로 구분된 파일을 CSV로 변환하고, CSV를 JSON, Python dict(.py)로 변환하는 스크립트입니다.
1. TAB으로 구분된 파일을 읽어들입니다.
2. 각 셀에서 콤마를 제거하고, 그것이 숫자인 경우 소수점 이하가 0이면 정수로 변환하여 저장함.
3. 변환된 데이터를 CSV 파일로 저장합니다.
4. CSV 파일을 formatted JSON 파일로 변환합니다.
5. CSV 파일을 Python dict 형태로 변환하여 .py 파일로 저장합니다.
"""

def convert_commas(value):
    if isinstance(value, str) and value.replace(',', '').isdigit():
        return float(value.replace(',', ''))
    return value

def format_numbers(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value

def csv_to_json(csv_filename, json_filename, indent=4):
    with open(csv_filename, 'r', encoding='utf-8') as csvf:
        reader = csv.DictReader(csvf)
        json_data = [row for row in reader]
    with open(json_filename, 'w', encoding='utf-8') as jsonf:
        json.dump(json_data, jsonf, indent=indent, ensure_ascii=False)
    print(f"{csv_filename} -> {json_filename} 변환 완료!")

def csv_to_python_dict(csv_filename, py_filename):
    df = pd.read_csv(csv_filename, dtype=str)
    dict_list = df.to_dict(orient='records')
    with open(py_filename, 'w', encoding='utf-8') as pyf:
        pyf.write('dict = \\\n[\n')
        for row in dict_list:
            pyf.write(f"    {row},\n")
        pyf.write(']\n')
    print(f"{csv_filename} -> {py_filename} 변환 완료!")

def tab_to_csv_json_pydict(tab_file):
    base, _ = os.path.splitext(tab_file)
    csv_file = f"{base}_converted.csv"
    json_file = f"{base}_converted_json_formatted.json"
    python_dict_file = f"{base}_converted_python_dict.py"
    # TAB 파일 읽기
    df = pd.read_csv(tab_file, sep='\t', dtype=str)
    df = df.map(convert_commas)
    df = df.map(format_numbers)
    df.to_csv(csv_file, index=False)
    csv_to_json(csv_file, json_file)
    csv_to_python_dict(csv_file, python_dict_file)

def batch_process(jobfilelist_path):
    with open(jobfilelist_path, 'r', encoding='utf-8') as f:
        files = [line.strip() for line in f if line.strip()]
    for tab_file in files:
        if os.path.exists(tab_file):
            print(f"처리 시작: {tab_file}")
            try:
                tab_to_csv_json_pydict(tab_file)
            except Exception as e:
                print(f"파일 처리 중 오류 발생: {tab_file} ({e})")
        else:
            print(f"파일 없음: {tab_file}")

if __name__ == "__main__":
    jobfilelist = "jobfilelist.txt"
    batch_process(jobfilelist)