from app.utils.constants import GEMINI_2_FLASH, GEMINI_1_FLASH
import google.generativeai as genai
from typing import Optional


class GeminiService:

    @staticmethod
    def generate_content(user_prompt: str, system_prompt: str,api_key: str,temperature: int) -> str:
        """
        Generate content using the Gemini model.
        :param user_prompt: The prompt to provide to the model.
        :param system_prompt: input the prompt to model how to behave while giving response
        :param api_key: api key for gemini
        :param temperature:
        :return: Generated text.
        """
        try:
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel(model_name=GEMINI_2_FLASH, system_instruction=system_prompt)

            response = model.generate_content(
                user_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=temperature,
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating content: {e}")
            raise Exception(f"Error occured while generatin content- {e}")
