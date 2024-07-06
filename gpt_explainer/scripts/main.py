import asyncio
import logging
import os
from pathlib import Path
import requests
from pptx_text_extractor import PptxParser
from gpt_integration import GPTIntegration
from async_requests import AsyncRequestsHandler
from typing import Optional

CONFIG_URL = 'http://localhost:5000/shared_dir'


LOG_FILE = Path(__file__).parent.parent.parent.resolve() / 'web_app' / 'logs' /'gpt_explainer_logs'/ 'explainer.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PresentationProcessor:
    '''
    PresentationProcessor class is responsible for processing presentations and getting explanations.
    '''
    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.outputs_folder, self.uploads_folder = self._fetch_directories()
        self.processed_files = set()

    @staticmethod
    def _fetch_directories():
        '''Fetches the directories for outputs and uploads from the configuration URL.'''
        response = requests.get(CONFIG_URL)
        if response.status_code != 200:
            raise Exception(f"Error fetching configuration: {response.text}")
        data = response.json()
        return Path(data['outputs_dir']), Path(data['uploads_dir'])

    async def process_presentation_and_get_explanations(self, presentation_file_path: str) -> None:
        '''Processes a presentation and gets explanations for the text in the presentation.'''
        presentation_path = Path(presentation_file_path)
        presentation_title = presentation_path.stem
        output_file_path = self.outputs_folder / f"{presentation_title}.json"

        try:
            pptx_parser = PptxParser(presentation_file_path)
            gpt_integration = GPTIntegration(self.api_key, presentation_title)
            async_requests_handler = AsyncRequestsHandler(gpt_integration, pptx_parser, output_file_path)
            await async_requests_handler.extract_all_text()
        except FileNotFoundError as e:
            logging.error(f"Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error processing {presentation_file_path}: {e}")

    async def check_uploads_folder(self) -> None:
        '''Checks the uploads folder for new presentations and processes them.'''
        while True:
            if self.uploads_folder.exists() and self.uploads_folder.is_dir():
                for pptx_file in self.uploads_folder.glob('*.pptx'):
                    if pptx_file.stem not in self.processed_files:
                        logging.info(f"Processing file: {pptx_file}")
                        print(f"Processing file: {pptx_file}")
                        try:
                            asyncio.create_task(self.process_presentation_and_get_explanations(str(pptx_file.resolve())))
                            logging.debug(f"Scheduled processing for: {pptx_file}")
                            print(f"Scheduled processing for: {pptx_file}")
                            self.processed_files.add(pptx_file.stem)
                        except Exception as e:
                            logging.error(f"Error processing {pptx_file}: {e}")
            else:
                logging.warning(f"Upload directory {self.uploads_folder} does not exist or is not a directory.")
            await asyncio.sleep(10)

if __name__ == "__main__":
    processor = PresentationProcessor(api_key=None)
    asyncio.run(processor.check_uploads_folder())