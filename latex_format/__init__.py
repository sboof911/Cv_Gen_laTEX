import os, json

def get_data(data_folder, language="en"):
    PROFILE_DESCRIPTION_PATH = os.path.join(data_folder, f'{language}_Profile_description.txt')
    USER_DATA_PATH = os.path.join(data_folder, 'user_data.json')
    PROJECTS_PATH = os.path.join(data_folder, 'projects.json')

    if not os.path.exists(data_folder):
        raise Exception(f"{data_folder} folder not found.")

    if os.path.exists(PROFILE_DESCRIPTION_PATH):
        with open(PROFILE_DESCRIPTION_PATH, 'r', encoding='utf-8') as file:
            profile_description : dict = file.read()
    else:
        raise Exception(f"Profile description file for language '{language}' not found.")

    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r', encoding='utf-8') as file:
            user_data = json.load(file)
            if not user_data.get(language, None):
                raise Exception(f"Language '{language}' not found in user_data.json")
            user_data : dict = user_data[language]
    else:
        raise Exception("user_data.json file not found.")

    if os.path.exists(PROJECTS_PATH):
        with open(PROJECTS_PATH, 'r', encoding='utf-8') as file:
            projects = json.load(file)
            if not projects.get(language, None):
                raise Exception(f"Language '{language}' not found in projects.json")
            projects : dict = projects[language]
    else:
        raise Exception("projects.json file not found.")

    return user_data, projects, profile_description
