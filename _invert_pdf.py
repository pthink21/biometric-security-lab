"""Convert dark slides to light theme but preserve original photos.
Strategy: invert the rendered page (handles bg + text + shapes),
then paste the ORIGINAL (un-inverted) embedded images back on top."""
import fitz
from PIL import Image, ImageOps
import io

SRC = r"D:\Blue and Black Modern Futuristic Biometrics Technology Presentation.pdf"
DST = r"D:\Biometrics_Presentation_LightMode.pdf"
DPI = 200

def invert_rgb(img: Image.Image) -> Image.Image:
    if img.mode != "RGB":
        img = img.convert("RGB")
    return ImageOps.invert(img)

def main():
    src = fitz.open(SRC)
    dst = fitz.open()
    zoom = DPI / 72.0
    mat = fitz.Matrix(zoom, zoom)
    n = len(src)
    print(f"[+] Pages: {n}")

    for i, page in enumerate(src):
        # 1) Render the whole page and invert -> light bg, dark text, accent flips
        pix = page.get_pixmap(matrix=mat, alpha=False)
        page_img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        canvas = invert_rgb(page_img)

        # 2) Restore original photos by pasting them back unmodified
        restored = 0
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                rects = page.get_image_rects(xref)
            except Exception:
                rects = []
            if not rects:
                continue
            try:
                base = src.extract_image(xref)
                orig = Image.open(io.BytesIO(base["image"]))
            except Exception:
                continue
            orig_rgb = orig.convert("RGB")
            for r in rects:
                x0 = max(0, int(round(r.x0 * zoom)))
                y0 = max(0, int(round(r.y0 * zoom)))
                x1 = min(canvas.width, int(round(r.x1 * zoom)))
                y1 = min(canvas.height, int(round(r.y1 * zoom)))
                w, h = x1 - x0, y1 - y0
                if w <= 0 or h <= 0:
                    continue
                resized = orig_rgb.resize((w, h), Image.LANCZOS)
                canvas.paste(resized, (x0, y0))
                restored += 1

        buf = io.BytesIO()
        canvas.save(buf, format="JPEG", quality=90)
        rect = page.rect
        new_page = dst.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=buf.getvalue())
        print(f"  - Page {i+1}/{n}: restored {restored} image(s)")

    dst.save(DST, deflate=True, garbage=4)
    dst.close()
    src.close()
    print(f"[+] Saved: {DST}")

if __name__ == "__main__":
    main()
