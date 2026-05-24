# -*- coding: utf-8 -*-
import sys, io, docx
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

src = r"C:/Users/ADMIN/Downloads/BAOCAODOANCOSO_NGUYENPHUCTHINH.docx"
dst = r"C:/Users/ADMIN/Downloads/BAOCAODOANCOSO_NGUYENPHUCTHINH_DACHINH.docx"

for label, path in [("GỐC", src), ("ĐÃ CHỈNH", dst)]:
    d = docx.Document(path)
    n_par = len(d.paragraphs)
    n_tbl = len(d.tables)
    n_img = 0
    for par in d.paragraphs:
        for run in par.runs:
            n_img += len(run._element.findall(
                ".//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline"
            ))
            n_img += len(run._element.findall(
                ".//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}anchor"
            ))
    headings = [p.text.strip() for p in d.paragraphs if p.style.name.startswith("Heading 1")]
    print(f"\n[{label}]")
    print(f"  Paragraphs : {n_par}")
    print(f"  Tables     : {n_tbl}")
    print(f"  Images     : {n_img}")
    print(f"  Heading 1  : {len(headings)}")
    for h in headings:
        print(f"    - {h}")
