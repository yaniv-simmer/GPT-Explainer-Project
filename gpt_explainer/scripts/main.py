import argparse
import asyncio
import os
from pathlib import Path
from typing import Optional
from pptx_text_extractor import PptxParser
from gpt_integration import GPTIntegration
from async_requests import AsyncRequestsHandler

# Define constants
DESCRIPTION = 'Extract text from a presentation and get explanations from GPT-3.5'
PPTX_FILE_PATH_HELP = 'Path to the PowerPoint presentation file'
OPENAI_API_KEY_HELP = 'OpenAI API key for GPT-3.5. If not provided, the key will be taken from the environment variable OPENAI_API_KEY'

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--pptx_file_path', required=True, help=PPTX_FILE_PATH_HELP)
    parser.add_argument('--OpenAI_api_key', required=False, help=OPENAI_API_KEY_HELP)
    return parser.parse_args()

async def main(api_key: Optional[str], presentation_file_path: str) -> None:
    """Main function to extract text from a presentation and get explanations from GPT-3.5."""
    presentation_path = Path(presentation_file_path)
    presentation_title = presentation_path.stem
    output_file_path = Path("gpt_explainer/output") / f"{presentation_title}.json"
    
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

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.OpenAI_api_key, args.pptx_file_path))