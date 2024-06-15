from typing import Generator, List
from pptx import Presentation


class PptxParser:
    """
    A class used to parse PPTX files and extract text from slides.
    """

    def __init__(self, file_path: str):
        """
        Initialize PptxParser with a PPTX file.

        Parameters:
            file_path (str): The path to the PPTX file.
        """
        self.presentation = Presentation(file_path)

    def extract_text_from_single_slide(self, slide) -> str:
        """
        Extracts and returns all text from a single slide.

        Parameters:
            slide: A slide object from a PPTX file.

        Returns:
            str: A string representing the text from the slide.
        """
        return '\n'.join([shape.text for shape in slide.shapes if hasattr(shape, "text")])

    def generate_text_from_slides(self) -> Generator[str, None, None]:
        """
        Extracts and yields all text from the slides in a PPTX file.

        Yields:
            str: A string representing the text from a slide.        
        """
        for slide in self.presentation.slides:
            slide_text = self.extract_text_from_single_slide(slide)
            if slide_text:
                yield slide_text

