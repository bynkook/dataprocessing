import os
import pandas as pd
from tabulate import tabulate
from reportlab.lib.pagesizes import A4, LETTER, landscape, portrait
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import win32print
import win32api


def truncate_cell_values(df: pd.DataFrame, max_width: int) -> pd.DataFrame:
    """
    각 셀 문자열을 max_width로 제한하고 말줄임표 처리.

    Parameters:
        df (pd.DataFrame): 원본 데이터프레임
        max_width (int): 출력 최대 글자 수

    Returns:
        pd.DataFrame: 각 셀이 잘린 문자열을 포함한 DataFrame
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
    max_col_width: int = 30,
    target_printer: str = "clawPDF",
    line_height: int | None = None
) -> None:
    """
    Pandas DataFrame을 tabulate 텍스트 테이블로 PDF 출력 + 지정 프린터로 전송

    Parameters:
        df (pd.DataFrame): 출력할 데이터프레임
        font_size (int): PDF에 사용할 폰트 크기
        pdf_filename (str): 생성할 PDF 파일 경로
        show_index (bool): 인덱스 출력 여부
        pagesize (str): 'A4' 또는 'LETTER'
        orientation (str): 'portrait' 또는 'landscape'
        max_col_width (int): 각 셀 최대 출력 폭
        target_printer (str): 출력할 프린터 이름
        line_height (int | None): 한 줄당 줄 간격 (기본: font_size + 2)

    Raises:
        FileNotFoundError: 지정된 폰트 경로 없음
        ValueError: 프린터 이름이 시스템에 존재하지 않을 경우
    """

    # [1] 폰트 설정
    font_path = "C:/Users/BKHOME/AppData/Local/Microsoft/Windows/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc"
    font_name = "D2Coding"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    else:
        raise FileNotFoundError(f"지정한 폰트 경로를 찾을 수 없습니다: {font_path}")

    # [2] 페이지 설정
    size_dict = {'A4': A4, 'LETTER': LETTER}
    pagesize_upper = pagesize.strip().upper()
    orientation_lower = orientation.strip().lower()
    if pagesize_upper not in size_dict:
        raise ValueError(f"지원되지 않는 페이지 크기: '{pagesize}'. 'A4' 또는 'LETTER'만 허용됩니다.")
    if orientation_lower not in ['portrait', 'landscape']:
        raise ValueError(f"지원되지 않는 방향: '{orientation}'. 'portrait' 또는 'landscape'만 허용됩니다.")

    base_size = size_dict[pagesize_upper]
    page_size = landscape(base_size) if orientation_lower == 'landscape' else portrait(base_size)

    # [3] 줄 높이 설정 (지정 없으면 기본값)
    line_height = line_height if line_height is not None else font_size + 2

    # [4] 데이터 문자열 폭 제한 적용
    df_limited = truncate_cell_values(df, max_width=max_col_width)
    table_text = tabulate(df_limited, headers="keys", tablefmt="psql", showindex=show_index, numalign="left")
    lines = table_text.splitlines()
    header_lines = lines[:3]
    data_lines = lines[3:]

    # [5] PDF 생성
    c = canvas.Canvas(pdf_filename, pagesize=page_size)
    width, height = page_size
    margin_x, margin_y = 40, 40
    c.setFont(font_name, font_size)
    y = height - margin_y

    def draw_header():
        nonlocal y
        for hline in header_lines:
            c.drawString(margin_x, y, hline)
            y -= line_height

    draw_header()
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

    # [6] 프린터 검사 및 출력
    printers = [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
    if target_printer not in printers:
        raise ValueError(f"지정한 출력 프린터 '{target_printer}'가 시스템에 존재하지 않습니다.")

    original_printer = win32print.GetDefaultPrinter()
    print(f"[INFO] 원래 기본 프린터: {original_printer}")
    print(f"[INFO] 임시 출력용 프린터: {target_printer}")

    try:
        win32print.SetDefaultPrinter(target_printer)
        win32api.ShellExecute(0, "print", pdf_filename, None, ".", 0)
        print("[INFO] 출력 명령 전송 완료.")
    finally:
        win32print.SetDefaultPrinter(original_printer)
        print(f"[INFO] 기본 프린터 복원됨: {original_printer}")