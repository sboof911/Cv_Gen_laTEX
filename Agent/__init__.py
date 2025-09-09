from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = str(os.getenv("OPENROUTER_API_KEY"))
santitized_lang = str(os.getenv("SUPPORTED_LANGUAGES")).replace("[","").replace("]","").replace("'","").replace('"',"").split(",")
SUPPORTED_LANGUAGES = [lang.strip() for lang in santitized_lang]

class Agent:
    def __init__(self, llm_model="tngtech/deepseek-r1t2-chimera:free"):
        self.llm_model = llm_model
        self.model = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY)

    def get_response(self, prompt: str) -> str:
        response = self.model.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        ).choices[0].message.content

        return response

    def get_projects_for_job(self, job_description: str, projects: list) -> dict:
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'projects.txt')
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        except FileNotFoundError:
            raise Exception(f"Prompt file not found: {prompt_path}")
        prompt = prompt.format(
            JOB_DESCRIPTION=job_description,
            PROJECTS=projects
        )
        response = self.get_response(prompt)
        return response

    def get_structured_job_description(self, job_description: str) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'job_description.txt')
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        except FileNotFoundError:
            raise Exception(f"Prompt file not found: {prompt_path}")
        prompt = prompt.format(
            JOB_DESCRIPTION=job_description
        )
        structured_description = self.get_response(prompt)
        return structured_description

    def get_language_from_job_offer(self, job_description: str) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'language.txt')
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read()
        except FileNotFoundError:
            raise Exception(f"Prompt file not found: {prompt_path}")
        prompt = prompt.format(
            JOB_DESCRIPTION=job_description,
            SUPPORTED_LANGUAGES=", ".join(SUPPORTED_LANGUAGES)
        )
        language = self.get_response(prompt)

        return language
