import json
import typing as t

import xlsxwriter

from jayson import main as jayson_main
from validator import Endpoint

# Create a new Excel file and add a worksheet.
items: t.Dict[str, Endpoint] = jayson_main()
print(items)

workbook = xlsxwriter.Workbook("api_info.xlsx")
api_numbering = 5
for key, value in items.items():
    worksheet = workbook.add_worksheet(name=key[-31:])
    api_numbering += 1

    worksheet.set_column("A:E", 20)

    bold_white = workbook.add_format(
        {"bold": True, "font_color": "#FFFFFF", "bg_color": "#4472c4", "border": 1}
    )

    bold_black = workbook.add_format(
        {"bold": True, "font_color": "#000000", "bg_color": "#deeaf6", "border": 1}
    )
    bold = workbook.add_format({"bold": True, "font_color": "#000000", "border": 1})
    normal = workbook.add_format({"font_color": "#000000", "border": 1})

    merge_format = workbook.add_format(
        {
            "align": "left",
            "valign": "vcenter",
            "font_color": "#000000",
            "border": 1,
            "text_wrap": True,
        }
    )

    bg_yellow = workbook.add_format(
        {
            "align": "left",
            "valign": "vcenter",
            "font_color": "#000000",
            "bg_color": "#fef2ca",
            "border": 1,
            "bold": True,
        }
    )

    empty_with_border = workbook.add_format({"border": 1})

    for row in range(0, 4):
        for col in range(0, 4):
            worksheet.write_blank(row, col, "", empty_with_border)

    # Write some data headers.
    worksheet.write("A1", "APINo", bold_white)
    worksheet.write(
        "B1",
        ("API-0" if api_numbering >= 10 else "API-00") + str(api_numbering),
        normal,
    )
    worksheet.write("A2", "機能概要", bold_white)
    worksheet.write("A3", "パス", bold_white)
    worksheet.write("B3", value.url, normal)
    worksheet.write("A4", "更新日", bold_white)
    worksheet.write("B4", "2023.08.04", normal)
    worksheet.write("C4", "更新者", bold_white)
    worksheet.write("D4", "Baljinnyam", normal)

    worksheet.merge_range(f"A6:G6", "入力", bg_yellow)

    worksheet.write("A7", "メソッド", bold)
    worksheet.write("A8", "リクエストヘッダ", bold)
    worksheet.write("A10", "リクエスト", bold)
    worksheet.write("A11", "パラメータ", bold)

    worksheet.write("B9", "authorization", normal)
    worksheet.write("C9", "ログイントークン", normal)
    worksheet.write("D9", "◯", normal)

    worksheet.write("A8", "パラメータ名", bold_black)
    worksheet.write("B8", "説明", bold_black)
    worksheet.write("C8", "必須", bold_black)
    worksheet.write("D8", "型", bold_black)
    worksheet.write("E8", "書式", bold_black)
    worksheet.write("F8", "値域", bold_black)
    worksheet.write("G8", "備考", bold_black)

    worksheet.write("A10", "パラメータ名", bold_black)
    worksheet.write("B10", "説明", bold_black)
    worksheet.write("C10", "必須", bold_black)
    worksheet.write("D10", "型", bold_black)
    worksheet.write("E10", "書式", bold_black)
    worksheet.write("F10", "値域", bold_black)
    worksheet.write("G10", "備考", bold_black)

    # logic goes here
    row_num = 11
    iterator = 0
    for i, body in enumerate(value.body):
        worksheet.write(f"A{i+row_num+1}", "", normal)
        worksheet.write(f"B{i+row_num}", body.param_name, normal)
        worksheet.write(f"C{i+row_num}", body.description, normal)
        worksheet.write(f"D{i+row_num}", "◯" if body.required else "", normal)
        worksheet.write(f"E{i+row_num}", body.type, normal)
        worksheet.write(f"F{i+row_num}", body.value_range, normal)
        worksheet.write(f"G{i+row_num}", body.note, normal)
        iterator += 1
    row_num += iterator + 2
    worksheet.merge_range(f"A{row_num-1}:G{row_num-1}", "入力サンプル", bg_yellow)

    if value.request:
        row_height = value.request.count("\n")

        worksheet.set_row(
            row_num - 1, 15 * (row_height + 2)
        )  # 15 is a default height for a row

        # Use merge_range method to merge cells
        worksheet.merge_range(f"A{row_num}:G{row_num}", value.request, merge_format)
        row_num += 2
    # title translateion : OUTPUT
    worksheet.merge_range(f"A{row_num-1}:G{row_num-1}", "出力", bg_yellow)
    worksheet.write("A" + str(row_num), "レスポンス", bold_black)
    row_num += 1
    worksheet.write("A" + str(row_num), "ヘッダ", bold_black)
    row_num += 1
    worksheet.write("A" + str(row_num), "レスポンス", bold_black)
    worksheet.write("A" + str(row_num + 1), "ボディ", bold_black)

    worksheet.merge_range(f"B{row_num}:D{row_num}", "項目", bold_black)
    worksheet.write("E" + str(row_num), "説明", bold_black)
    worksheet.write("F" + str(row_num), "必須", bold_black)
    worksheet.write("G" + str(row_num), "型", bold_black)
    worksheet.write("H" + str(row_num), "書式", bold_black)
    worksheet.write("I" + str(row_num), "値域", bold_black)
    worksheet.write("J" + str(row_num), "備考", bold_black)

    if value.response:
        response_dict = json.loads(value.response)
        row_num += 1

        for key, _value in response_dict.items():
            worksheet.write("A" + str(row_num + 1), "", normal)
            worksheet.merge_range(f"B{row_num}:D{row_num}", key, normal)
            typeofvalue = type(_value)
            worksheet.write("E" + str(row_num), "", normal)
            worksheet.write("F" + str(row_num), "", normal)
            worksheet.write("G" + str(row_num), (typeofvalue.__name__), normal)
            worksheet.write("H" + str(row_num), "", normal)
            worksheet.write("I" + str(row_num), "", normal)
            worksheet.write("J" + str(row_num), "", normal)
            row_num += 1

        row_num += 1

        row_height = value.response.count("\n")

        worksheet.set_row(
            row_num - 1, 15 * (row_height + 2)
        )  # 15 is a default height for a row

        # Use merge_range method to merge cells
        worksheet.merge_range(f"A{row_num}:G{row_num}", value.response, merge_format)
        row_num += 2
    # Close the workbook.
workbook.close()
