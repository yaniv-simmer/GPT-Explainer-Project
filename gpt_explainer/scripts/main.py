# # import argparse
# # import asyncio
# # import os
# # from pathlib import Path
# # from typing import Optional
# # from pptx_text_extractor import PptxParser
# # from gpt_integration import GPTIntegration
# # from async_requests import AsyncRequestsHandler

# # # Define constants
# # DESCRIPTION = 'Extract text from a presentation and get explanations from GPT-3.5'
# # PPTX_FILE_PATH_HELP = 'Path to the PowerPoint presentation file'
# # OPENAI_API_KEY_HELP = 'OpenAI API key for GPT-3.5. If not provided, the key will be taken from the environment variable OPENAI_API_KEY'

# # def parse_args() -> argparse.Namespace:
# #     """Parse command line arguments."""
#     # parser = argparse.ArgumentParser(description=DESCRIPTION)
#     # parser.add_argument('--pptx_file_path', required=True, help=PPTX_FILE_PATH_HELP)
#     # parser.add_argument('--OpenAI_api_key', required=False, help=OPENAI_API_KEY_HELP)
#     # return parser.parse_args()

# # async def main(api_key: Optional[str], presentation_file_path: str) -> None:
# #     """
# #     Main function to extract text from a presentation and get explanations from GPT-3.5.

# #     Usege:
# #       python main.py --pptx_file_path <pptx_file_path> [--OpenAI_api_key <api_key>]
# #     """
# #     presentation_path = Path(presentation_file_path)
# #     presentation_title = presentation_path.stem
# #     output_file_path = Path("output") / f"{presentation_title}.json"
    
# #     if api_key is None:
# #         api_key = os.getenv('OPENAI_API_KEY')
    
# #     try:
# #         pptx_parser = PptxParser(presentation_file_path)
# #     except FileNotFoundError as e:
# #         print(f"Error: {e}")
# #         return
# #     gpt_integration = GPTIntegration(api_key, presentation_title)
# #     async_requests_handler = AsyncRequestsHandler(gpt_integration, pptx_parser, output_file_path)
    
# #     await async_requests_handler.extract_all_text()

# # if __name__ == "__main__":
# #     args = parse_args()
# #     asyncio.run(main(args.OpenAI_api_key, args.pptx_file_path))










import argparse
import asyncio
import os
from pathlib import Path
from typing import Optional
from pptx_text_extractor import PptxParser
from gpt_integration import GPTIntegration
from async_requests import AsyncRequestsHandler
import subprocess

# UPLOADS_DIR = './uploads'
# OUTPUTS_DIR = 'outputs'

# # def parse_args() -> argparse.Namespace:
# #     """Parse command line arguments."""
# #     parser = argparse.ArgumentParser(description=DESCRIPTION)
# #     parser.add_argument('--pptx_file_path', required=True, help=PPTX_FILE_PATH_HELP)
# #     parser.add_argument('--OpenAI_api_key', required=False, help=OPENAI_API_KEY_HELP)
# #     return parser.parse_args()

# async def process_presentation_and_get_explanations(api_key: Optional[str], presentation_file_path: str) -> None:
    # """
    # Extract text from a presentation and get explanations from GPT-3.5.
    # Save the explanations to a JSON file.

    # Parameters:
    #     - api_key: OpenAI API key for GPT-3.5
    #     - presentation_file_path: Path to the PowerPoint presentation file
    # """
    # presentation_path = Path(presentation_file_path)
    # presentation_title = presentation_path.stem
    # output_file_path = Path(OUTPUTS_DIR) / f"{presentation_title}.json"
    
    # if api_key is None:
    #     api_key = os.getenv('OPENAI_API_KEY')
    
    # try:
    #     pptx_parser = PptxParser(presentation_file_path)
    # except FileNotFoundError as e:
    #     print(f"Error: {e}")
    #     return
    # gpt_integration = GPTIntegration(api_key, presentation_title)
    # async_requests_handler = AsyncRequestsHandler(gpt_integration, pptx_parser, output_file_path)
    
    # await async_requests_handler.extract_all_text()

# async def check_uploads_folder(api_key: Optional[str]) -> None:
#     """
#     Check the './uploads' folder for new files and process them if found.
#     """
#     processed_files = set()
    
#     while True:
#         uploads_path = Path(UPLOADS_DIR)
#         if uploads_path.exists() and uploads_path.is_dir():
#             for pptx_file in uploads_path.glob('*.pptx'):
#                 if pptx_file.name not in processed_files:
#                     print(f"\nProcessing file: {pptx_file}\n")
#                     pptxFilePath = Path(str(pptx_file))
#                     pptxFilePath = pptxFilePath.resolve()
#                     await process_presentation_and_get_explanations(api_key, str(pptxFilePath))
#                     print(f"\nrunning at backroun and coninue the loop: {pptxFilePath}\n")
#                     processed_files.add(pptx_file.name)
#         else:
#             print(f"Upload directory {UPLOADS_DIR} does not exist or is not a directory.")
        
#         await asyncio.sleep(15)

# if __name__ == "__main__":
#     #args = parse_args()
#     api_key = os.getenv('OPENAI_API_KEY')
#     asyncio.run(check_uploads_folder(api_key))



# # def main():
# #     parser = argparse.ArgumentParser(description="Extract text from a PPTX file.")
# #     parser.add_argument('--pptx_file_path', type=str, required=True, help='Path to the PPTX file')
# #     args = parser.parse_args()

# #     pptx_file_path = args.pptx_file_path

# #     print(f"Debug: Provided file path: {pptx_file_path}")

# #     if not os.path.isfile(pptx_file_path):
# #         print(f"Error: File not found: {pptx_file_path}")
# #         return

# #     text = extract_text_from_pptx(pptx_file_path)
# #     print(text)

# # if __name__ == '__main__':
# #     main()




# # from pptx import Presentation
# # o = r'C:\Users\simme\Desktop\Academic\Year 2\סמסטר דדדדדדדדדד\רשתות\מצגות הרצאות\Chapter_6_5-6.pptx'
# # p = Presentation(o)
# # print(p)







import asyncio
import logging
import os
from pathlib import Path
import json
from typing import Optional

UPLOADS_DIR = './uploads'
OUTPUTS_DIR = 'outputs'
LOG_FILE = 'explainer.log'

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def process_presentation_and_get_explanations(api_key: Optional[str], presentation_file_path: str) -> None:
    """
    Extract text from a presentation and get explanations from GPT-3.5.
    Save the explanations to a JSON file.

    Parameters:
        - api_key: OpenAI API key for GPT-3.5
        - presentation_file_path: Path to the PowerPoint presentation file
    """
    presentation_path = Path(presentation_file_path)
    presentation_title = presentation_path.stem
    output_file_path = Path(OUTPUTS_DIR) / f"{presentation_title}.json"
    
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        pptx_parser = PptxParser(presentation_file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    gpt_integration = GPTIntegration(api_key, presentation_title)
    async_requests_handler = AsyncRequestsHandler(gpt_integration, pptx_parser, output_file_path)
    
    await async_requests_handler.extract_all_text()

async def check_uploads_folder(api_key: Optional[str]) -> None:
    processed_files = set()

    while True:
        uploads_path = Path(UPLOADS_DIR)
        outputs_path = Path(OUTPUTS_DIR)
        outputs_path.mkdir(exist_ok=True)

        if uploads_path.exists() and uploads_path.is_dir():
            for pptx_file in uploads_path.glob('*.pptx'):
                if pptx_file.stem not in processed_files:
                    logging.info(f"Processing file: {pptx_file}")
                    print(f"Processing file: {pptx_file}")
                    try:
                        explanation = await process_presentation_and_get_explanations(api_key, str(pptx_file.resolve()))

                        logging.info(f"Processed and saved explanation for: {pptx_file}")
                        print(f"Processed and saved explanation for: {pptx_file}")
                        processed_files.add(pptx_file.stem)
                    except Exception as e:
                        logging.error(f"Error processing {pptx_file}: {e}")
        else:
            logging.warning(f"Upload directory {UPLOADS_DIR} does not exist or is not a directory.")
        
        await asyncio.sleep(10)

if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    asyncio.run(check_uploads_folder(api_key))