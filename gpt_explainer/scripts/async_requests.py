import json
import os
import asyncio
from typing import List, Tuple
from gpt_integration import GPTIntegration
from pptx_text_extractor import PptxParser

class AsyncRequestsHandler:
    def __init__(self, gpt_integration: GPTIntegration, pptx_parser: PptxParser, output_file_path: str):
        self.gpt_integration = gpt_integration
        self.pptx_text_extractor = pptx_parser
        self.output_file_path = output_file_path
        self.explanations: List[Tuple[int, str]] = []

    async def extract_all_text(self):
        """Extracts all text from slides and saves the explanations to a JSON file."""
        slides_content_generator = self.pptx_text_extractor.generate_text_from_slides()
        tasks = [asyncio.create_task(self.gpt_integration.get_gpt_explanation(slide_content, slide_number))
                 for slide_number, slide_content in enumerate(slides_content_generator, start=1)
                 if not slide_content.startswith("Error processing slide")]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        self.explanations = [explanation for explanation in results if not isinstance(explanation, Exception)]
        self.save_explanation_to_json()

    def save_explanation_to_json(self):
        """Saves the explanations to a JSON file."""
        os.makedirs(os.path.dirname(self.output_file_path), exist_ok=True)

        data = {}
        if os.path.exists(self.output_file_path):
            with open(self.output_file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print("Error reading the JSON file.")

        data.update({explanation[0]: explanation[1] for explanation in self.explanations})

        with open(self.output_file_path, "w") as file:
            json.dump(data, file, indent=4)