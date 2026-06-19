# -*- coding: utf-8 -*-
"""build_v3_test.py - Build thu BAOCAODOANCOSO_HOANCHINH (Chuong 1 + 2 only).

Phien ban tam, dung de kiem tra:
- Khong con em-dash trong noi dung sinh ra
- So trang uoc tinh tich luy
- Helpers tu _report_core hoat dong dung voi cac chuong v3
"""

import os
from docx import Document

import _report_core
from _report_core import (
    setup_doc_defaults, new_section,
    add_para, add_h1, add_page_break,
)
from _v3_chapter1 import build_chapter1
from _v3_chapter2 import build_chapter2
from _v3_chapter3 import build_chapter3
from _v3_chapter4 import build_chapter4


OUT_TEST = r"C:\Users\ADMIN\biometric-security-lab\BAOCAODOANCOSO_HOANCHINH_TEST.docx"


def build_cover_min(doc):
    add_para(doc, "BỘ GIÁO DỤC VÀ ĐÀO TẠO",
             size=13, bold=True, align='center', space_after=2)
    add_para(doc, "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ TP. HCM (HUTECH)",
             size=13, bold=True, align='center', space_after=2)
    add_para(doc, "KHOA CÔNG NGHỆ THÔNG TIN",
             size=13, bold=True, align='center', space_after=24)
    add_para(doc, "ĐỒ ÁN CƠ SỞ",
             size=24, bold=True, align='center', space_after=14)
    add_para(doc,
        "NGHIÊN CỨU TẤN CÔNG VÀO HỆ THỐNG\nXÁC THỰC SINH TRẮC HỌC",
        size=20, bold=True, align='center', space_after=24, line_spacing=1.3)
    add_para(doc, "Ngành: AN TOÀN THÔNG TIN",
             size=14, bold=True, align='center', space_after=22)
    add_para(doc, "Giảng viên hướng dẫn: ThS. Đặng Thị Thạch Thảo",
             size=13, align='center', space_after=4)
    add_para(doc, "Sinh viên thực hiện: Nguyễn Phúc Thịnh",
             size=13, align='center', space_after=4)
    add_para(doc, "MSSV: 2387700066    Lớp: 23DATA1",
             size=13, align='center', space_after=40)
    add_para(doc, "TP. Hồ Chí Minh, tháng 6 năm 2026",
             size=13, italic=True, align='center')


def main():
    print("[v3-test] Build BAOCAODOANCOSO_HOANCHINH_TEST.docx ...")
    doc = Document()
    setup_doc_defaults(doc)

    build_cover_min(doc)

    new_section(doc, fmt='decimal', start=1)
    build_chapter1(doc)
    build_chapter2(doc)
    build_chapter3(doc)
    build_chapter4(doc)

    doc.save(OUT_TEST)
    size_kb = os.path.getsize(OUT_TEST) / 1024
    paras = _report_core.PAGE_TRACKER["counter"]
    pages = max(1, paras // 35 + 1)
    print(f"[v3-test] saved: {OUT_TEST} ({size_kb:.1f} KB)")
    print(f"[v3-test] paragraph counter = {paras}, uoc tinh ~ {pages} trang")


if __name__ == "__main__":
    main()
