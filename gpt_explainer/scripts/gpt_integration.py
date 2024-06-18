import openai
import os
import asyncio
import json


PROMPT_USER_CONTENT_TEMPLATE = """
f"This text is from a PowerPoint file titled '{}'(from slide number {})(dont include the title in your response), of a PowerPoint presentation. "
f"The slide contains the following content: {}. "
Please provide a detailed yet easy-to-understand explanation of the main points and concepts covered in this slide. 
Ensure the explanation is suitable for someone new to the material.
for example if the slide content is:
"Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll. It involves the conversion of carbon dioxide and water into glucose and oxygen."
your response could be:
"
Photosynthesis process: Photosynthesis is a vital process for plants and some other organisms, allowing them to produce food using sunlight.
Role of chlorophyll: Chlorophyll, the green pigment in plants, helps in capturing sunlight.
Conversion of substances: During photosynthesis, plants convert carbon dioxide and water into glucose, which is used as food, and oxygen, which is released into the air."
"""

PROMPT_SYSTEM_ROLE = f"""You are an expert educator specializing in making complex topics easy to understand. 
Your goal is to provide detailed yet easy-to-understand text, explaning the content of a given PowerPoint slide.
the text you provide will be used to help students understand the material better.
"""



class GPTIntegration:
    def __init__(self, api_key, presentation_title, organization='org-K7cOPp2AJvDDYNsBn8Vs8U1u', project='Default project'):
        openai.organization = organization
        openai.project = project      
        openai.api_key = api_key
        self.presentation_title = presentation_title
        


    def asynchronous_api_call(self, text, slide_number):
        return openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo", # im assuming the assingment requires gpt-3.5 because its old ..
                messages=[
                    {"role": "system",
                      "content": PROMPT_SYSTEM_ROLE},
                    {"role": "user",
                      "content": (PROMPT_USER_CONTENT_TEMPLATE.format(self.presentation_title, slide_number , text))}
                ],
                max_tokens=10000,
                temperature= 0.7,
                timeout = 500 # made this long just in case the response takes a while for any reason
            )
        
        

    async def get_gpt_explanation(self, text, slide_number):
        """
        Function to get explanation from GPT-3.5 for a given text.
        """
        print(f"start {slide_number}")
        print()

        try:
            response = await self.asynchronous_api_call( text, slide_number)
            # TODO
            print( f"{slide_number} isssss done responce\n:\n\n")

            return [slide_number, response.choices[0].message.content]
        except Exception as e:
            print( f"{slide_number}is done ERROR")
            raise Exception(f"Failed to get explanation from GPT: {e}")
        

        


            
