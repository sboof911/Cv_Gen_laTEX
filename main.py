import os, sys
from latex_format import latex_builder
from generate_pdf.github import github_repo, FILE_PATH_IN_REPO
from generate_pdf import compile_latex_from_github
from Agent.agent import select_relevant_projects, prepare_cv_for_job
from dotenv import load_dotenv

load_dotenv()


DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user_data')
MAX_PROJECTS = int(os.getenv("MAX_PROJECTS", 3))
LATEX_FILE_PATH = "main.tex"

def select_best_projects(projects : dict, project_titles : dict):
    selected_projects = []
    for section in projects:
        selected_projects.append({
            "section": section["section"],
            "projects": []
        })
        stored_scores = []
        for project in section["projects"][:MAX_PROJECTS]:
            if project_titles.get(project["title"], None):
                score = project_titles[project["title"]]
                index = -1
                for stored_score in stored_scores:
                    if score > stored_score:
                        index = stored_scores.index(stored_score)
                        selected_projects[-1]["projects"].insert(index, project)
                        stored_scores.insert(index, score)
                        break
                if index == -1:
                    stored_scores.append(score)
                    selected_projects[-1]["projects"].append(project)

    indexs_remove = []
    for index, section in enumerate(selected_projects):
        if len(section["projects"]) == 0:
            indexs_remove.append(index)
    for index in reversed(indexs_remove):
        selected_projects.pop(index)
    return selected_projects

def get_info(language):
    user_data, projects, profile_description = prepare_cv_for_job(DATA_FOLDER, language)
    selected_projects = []
    for section in projects:
        selected_projects.append({
            "section": section["section"],
            "projects": []
        })
        scores = []
        for project in section["projects"]:
            input_score = input(f"Set the score for the project '{project['title']}' ")
            try:
                input_score = float(input_score)
            except ValueError:
                input_score = 0
            index = -1
            for score in scores:
                if input_score > score:
                    index = scores.index(score)
                    selected_projects[-1]["projects"].insert(index, project)
                    scores.insert(index, score)
                    break
            if index == -1:
                scores.append(input_score)
                selected_projects[-1]["projects"].append(project)

    indexs_remove = []
    for index, section in enumerate(selected_projects):
        if len(section["projects"]) == 0:
            indexs_remove.append(index)
    for index in reversed(indexs_remove):
        selected_projects.pop(index)
    return user_data, selected_projects, profile_description

url = "https://latexonline.cc/data?target=pdf"
AUTO = True if len(sys.argv) == 1 else False

if AUTO:
    with open("job_description.txt", "r", encoding="utf-8") as f:
        job_description = f.read()
    if not job_description.strip():
        raise ValueError("Job description file is empty. Please provide a valid job description.")
    project_titles, user_data, projects, profile_description = select_relevant_projects(job_description, DATA_FOLDER)
    selected_projects = select_best_projects(projects, project_titles)
else:
    user_data, selected_projects, profile_description = get_info(sys.argv[1])

print("Building LaTeX file...")
file_data = latex_builder.build_tex(user_data, selected_projects, profile_description)
with open(LATEX_FILE_PATH, "w", encoding='utf-8') as file:
    file.write(file_data)

github = github_repo()

github.upload_file(LATEX_FILE_PATH)
firstName = user_data.get('firstName','')
lastName = user_data.get('lastName','')
PDF_PATH = os.path.join(os.path.dirname(__file__), f"CV_{lastName}_{firstName}.pdf")

if compile_latex_from_github(github.url, FILE_PATH_IN_REPO, PDF_PATH):

    os.remove("main.tex")
    print("✅ Local LaTeX file removed.")
    github.delete_file()
    print(f"✅ PDF generated: {PDF_PATH}")
