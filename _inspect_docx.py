# -*- coding: utf-8 -*-
import sys, io, json, docx

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

p = r"C:/Users/ADMIN/Downloads/BAOCAODOANCOSO_NGUYENPHUCTHINH.docx"
d = docx.Document(p)

print(f"Tổng số paragraph: {len(d.paragraphs)}")
print(f"Tổng số bảng: {len(d.tables)}")
print("-" * 80)

for i, par in enumerate(d.paragraphs):
    style = par.style.name
    txt = par.text.strip()
    if not txt and not style.startswith("Heading"):
        continue
    if style.startswith("Heading") or style.startswith("Title") or len(txt) < 200:
        print(f"{i:4d} | {style:20s} | {txt[:160]}")
