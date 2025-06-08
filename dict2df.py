import pandas as pd
import numpy as np
from tabulate import tabulate
import print2pdf

# 저장된 Python 딕셔너리 데이터를 가져오기
import table_converted_python_dict
import table2_converted_python_dict
import table3_converted_python_dict
import table4_converted_python_dict

# 각 모듈에서 dict 속성을 가져와서 Python 딕셔너리로 저장
dict1 = table_converted_python_dict.dict
dict2 = table2_converted_python_dict.dict
dict3 = table3_converted_python_dict.dict
dict4 = table4_converted_python_dict.dict

# 각 dictionanry를 DataFrame으로 변환
df1 = pd.DataFrame.from_dict(dict1)
df2 = pd.DataFrame.from_dict(dict2)
df3 = pd.DataFrame.from_dict(dict3)
df4 = pd.DataFrame.from_dict(dict4)

# 특정 컬럼 삭제(inplace=True 원본에 반영)
df4.drop(columns=['SEQ_NO'], inplace=True, errors='ignore')

# 모든 dataframe을 하나로 합침(NaN 유지한 수직병합 - SQL의 UNION ALL과 동일)
# ignore_index=True 옵션을 사용하여 인덱스를 재설정
df = pd.concat([df1, df2, df3, df4], ignore_index=True)
# object 타입 열 안에 있는 None 값을 명시적으로 np.nan으로 통일
df = df.replace({None: np.nan})

# 컬럼 값 기준으로 정렬
# ignore_index=True 옵션을 사용하여 인덱스를 재설정
df_sorted = df.sort_values(by=['시스템 명칭','테이블 ID'], ascending=[True, True], ignore_index=True)

# 컬럼 출력 순서 재정의
new_column_order = ['시스템 명칭', '테이블 ID', '표준 테이블 명칭', '컬럼 IT 명칭', '컬럼 명칭', '표준 컬럼 명칭', '전체 ROW 개수']
df_reordered_sorted = df_sorted[new_column_order]
# 결과 일부 출력(tabulate)
table = tabulate(df_reordered_sorted[1500:1520], headers='keys', tablefmt='psql', numalign="left", showindex=False)
print(table)

# 최종 결과를 CSV 파일로 저장
df_reordered_sorted.to_csv('reordered_sorted_combined_data.csv', encoding='utf-8-sig')

# numpy array 로 변환
# nan 은 python 에 인식 가능한 None 으로 변경
arr = (df_reordered_sorted.replace({np.nan: None, np.inf: None})).to_numpy()
# 결과 일부 출력
print(arr[1500:1520])

# print to PDF file
print2pdf.printer(
    df_reordered_sorted,
    font_size=7,
    pdf_filename='tabulated_output.pdf',
    show_index=False,
    pagesize='A4',
    orientation='landscape',
    max_col_width=30,
    line_height=8
    )