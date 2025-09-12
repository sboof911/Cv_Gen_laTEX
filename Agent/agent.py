from .data_extractor import extract_data
from . import Agent, SUPPORTED_LANGUAGES
import json

agent = Agent()

def prepare_cv_for_job(data_folder: str, language : str) -> dict:
    if not language in SUPPORTED_LANGUAGES:
        raise Exception(f"Language '{language}' not supported. Supported languages are {SUPPORTED_LANGUAGES}.")
    return extract_data(data_folder, language)

def structure_job_description(job_description: str) -> str:
    return agent.get_structured_job_description(job_description)

def get_language_from_job_offer(job_description: str) -> str:
    language =  agent.get_language_from_job_offer(job_description).strip()
    if not language in SUPPORTED_LANGUAGES:
        print(f"⚠️ Detected language '{language}' is not supported. Defaulting to 'en'. Supported languages are {SUPPORTED_LANGUAGES}.")
        language = "en"
    return language

def select_perfect_projects(job_description: str, projects: list) -> dict:
    projects_titles = agent.get_projects_for_job(job_description, projects)
    projects_titles = projects_titles[projects_titles.find("{"): projects_titles.rfind("}") + 1]
    try:
        projects_titles = json.loads(projects_titles)
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse the response as JSON: {e} \nResponse was: {projects_titles}")
    return projects_titles

def select_relevant_projects(job_description: str, data_folder: str):
    print("Structuring job description...")
    job_description = structure_job_description(job_description)
    print("Extracting user data and projects...")
    language = get_language_from_job_offer(job_description)
    user_data, projects, profile_description = prepare_cv_for_job(data_folder, language)
    print("Selecting relevant projects...")
    projects_titles = select_perfect_projects(job_description, projects)

    return projects_titles, user_data, projects, profile_description
