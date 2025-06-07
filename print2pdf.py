import os
import pandas as pd
from tabulate import tabulate
from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def truncate_cell_values(df: pd.DataFrame, max_width: int) -> pd.DataFrame:
    """
    DataFrame의 각 셀 값을 문자열로 변환한 뒤, 지정된 최대 너비(max_width)를 초과하는 경우 말줄임표(…)로 잘라 반환.

    Parameters:
        df (pd.DataFrame): 입력 데이터프레임
        max_width (int): 셀 최대 출력 길이 (문자 수)

    Returns:
        pd.DataFrame: 문자열 길이가 제한된 DataFrame
    """
    def truncate(x):
        x_str = str(x)
        return x_str if len(x_str) <= max_width else x_str[:max_width - 1] + '…'

    return df.astype(str).apply(lambda col: col.map(truncate))


def printer(
    df: pd.DataFrame,
    font_size: int = 9,
    pdf_filename: str = "output.pdf",
    show_index: bool = False,
    pagesize: str = 'A4',
    orientation: str = 'portrait',
    max_col_width: int = 30
) -> None:
    """
    Pandas DataFrame을 tabulate 형식으로 PDF로 출력 (페이지마다 헤더 반복 출력 포함)

    Parameters:
        df (pd.DataFrame): 출력할 테이블 데이터
        font_size (int): 출력 폰트 크기 (기본: 9)
        pdf_filename (str): 저장될 PDF 파일 경로
        show_index (bool): 인덱스를 PDF에 포함할지 여부
        pagesize (str): 페이지 크기 ('A4', 'LETTER' 지원)
        orientation (str): 'portrait' 또는 'landscape'
        max_col_width (int): 각 셀의 최대 문자열 길이

    Raises:
        FileNotFoundError: 지정된 폰트 파일이 존재하지 않을 경우
        ValueError: 지원하지 않는 pagesize 또는 orientation 입력 시
    """

    # 사용자 폰트 설정 (D2Coding 기준)
    font_path = "C:/Users/BKHOME/AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc"
    font_name = "D2Coding"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    else:
        raise FileNotFoundError(f"지정한 폰트 경로를 찾을 수 없습니다: {font_path}")

    # 페이지 크기 설정
    size_dict = {'A4': A4, 'LETTER': LETTER}
    pagesize_upper = pagesize.strip().upper()
    orientation_lower = orientation.strip().lower()

    if pagesize_upper not in size_dict:
        raise ValueError(f"지원되지 않는 페이지 크기: '{pagesize}'. 'A4' 또는 'LETTER'만 지원됩니다.")
    if orientation_lower not in ['portrait', 'landscape']:
        raise ValueError(f"지원되지 않는 방향: '{orientation}'. 'portrait' 또는 'landscape'만 지원됩니다.")

    base_size = size_dict[pagesize_upper]
    page_size = landscape(base_size) if orientation_lower == 'landscape' else portrait(base_size)

    # 셀 내용 길이 제한 적용
    df_limited = truncate_cell_values(df, max_width=max_col_width)

    # tabulate 텍스트 생성
    table_text = tabulate(df_limited, headers="keys", tablefmt="psql", showindex=show_index, numalign="left")
    lines = table_text.splitlines()
    header_lines = lines[:3]
    data_lines = lines[3:]

    # PDF 캔버스 생성
    c = canvas.Canvas(pdf_filename, pagesize=page_size)
    width, height = page_size
    margin_x, margin_y = 40, 40
    line_height = font_size + 3

    c.setFont(font_name, font_size)
    y = height - margin_y

    # 페이지 상단에 헤더 3줄 출력
    def draw_header():
        nonlocal y
        for hline in header_lines:
            c.drawString(margin_x, y, hline)
            y -= line_height

    draw_header()

    # 본문 출력 (줄 단위)
    for line in data_lines:
        if y < margin_y + line_height:
            c.showPage()
            c.setFont(font_name, font_size)
            y = height - margin_y
            draw_header()
        c.drawString(margin_x, y, line)
        y -= line_height

    c.save()
    print(f"✅ PDF 저장 완료: {pdf_filename}")
