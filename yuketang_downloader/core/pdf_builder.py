"""Thin wrapper around img2pdf for converting images to PDF."""

from pathlib import Path


def build_pdf(image_paths: list[str], output_path: str) -> None:
    """Convert an ordered list of PNG screenshots into a single PDF file.

    Args:
        image_paths: Ordered list of paths to PNG images.
        output_path: Destination path for the generated PDF.

    Raises:
        FileNotFoundError: If any image path doesn't exist.
        PermissionError: If the output path is not writable.
    """
    import img2pdf

    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))
