"""Build the spatial-pickup group note while preserving source pages 1--2."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parent
SOURCE_PAGE_1 = ROOT / "source_page_1.pdf"
SOURCE_PAGE_2 = ROOT / "source_page_2.pdf"
EXTENSION = ROOT / "build" / "group_meeting_spatial_pickup_extension.pdf"
OUTPUT = ROOT / "group_meeting_pay_or_search_spatial_wpbe.pdf"


def main() -> None:
    source_page_1 = PdfReader(SOURCE_PAGE_1)
    source_page_2 = PdfReader(SOURCE_PAGE_2)
    extension = PdfReader(EXTENSION)
    if len(source_page_1.pages) != 1 or len(source_page_2.pages) != 1:
        raise ValueError("Each preserved source PDF must contain exactly one page.")
    if len(extension.pages) != 3:
        raise ValueError("The replacement extension must contain exactly three pages.")

    writer = PdfWriter()
    writer.add_page(source_page_1.pages[0])
    writer.add_page(source_page_2.pages[0])
    for page in extension.pages:
        writer.add_page(page)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("wb") as stream:
        writer.write(stream)

    print(OUTPUT)


if __name__ == "__main__":
    main()
