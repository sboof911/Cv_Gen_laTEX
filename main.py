import os, sys, json, requests
language = sys.argv[1] if len(sys.argv) > 1 else "en"


DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'user_data')
PROFILE_DESCRIPTION_PATH = os.path.join(DATA_FOLDER, f'{language}_Profile_description.txt')
USER_DATA_PATH = os.path.join(DATA_FOLDER, 'user_data.json')
PROJECTS_PATH = os.path.join(DATA_FOLDER, 'projects.json')

if os.path.exists(PROFILE_DESCRIPTION_PATH):
    with open(PROFILE_DESCRIPTION_PATH, 'r', encoding='utf-8') as file:
        profile_description = file.read()
else:
    raise Exception(f"Profile description file for language '{language}' not found.")

if os.path.exists(USER_DATA_PATH):
    with open(USER_DATA_PATH, 'r', encoding='utf-8') as file:
        user_data = json.load(file)
        if not user_data.get(language, None):
            raise Exception(f"Language '{language}' not found in user_data.json")
        user_data = user_data[language]
else:
    raise Exception("user_data.json file not found.")

if os.path.exists(PROJECTS_PATH):
    with open(PROJECTS_PATH, 'r', encoding='utf-8') as file:
        projects = json.load(file)
        if not projects.get(language, None):
            raise Exception(f"Language '{language}' not found in projects.json")
        projects = projects[language]
else:
    raise Exception("projects.json file not found.")

## Header
HEADER = r"""\documentclass[a4paper,11pt]{article}

% Packages
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}

% Section formatting
\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]

% Custom command for entries
\newcommand{\cvitem}[2]{\textbf{#1} \hfill #2 \\}

%------------------ DOCUMENT ------------------%
\begin{document}"""
file_data = HEADER

## User Information
USER_INFO = fr"""
\begin{{center}}
    {{\Huge \textbf{{{user_data.get("lastName", "")} {user_data.get("firstName", "")}}}}} \\[0.3em]
    {user_data.get("title", "")} \\[0.3em]
    \href{{mailto:{user_data.get("email", "")}}}{{{user_data.get("email", "")}}} \quad +212 608 60 3440 \quad
    \href{{{user_data.get("linkedin", "")}}}{{LinkedIn}} \quad
    \href{{{user_data.get("github", "")}}}{{GitHub}}
\end{{center}}
"""
file_data += USER_INFO

## Profil Description
PROFIL_DESCRIPTION = fr"""
% Profile
\section*{{Profile}}
{profile_description}

"""
file_data += PROFIL_DESCRIPTION


## Education

education = r"""
\section*{Education}
"""
educations = user_data.get("education", [])
educations.sort(key=lambda x: x.get("from_year", 0), reverse=True)
for data in educations:
    education += fr"""
\cvitem{{{data.get("from_year")}--{data.get("to_year")}}}{{{data.get("degree")} in {data.get("field")}, {data.get("institution")}}}"""
file_data += education

## Professional Experience

pro_experience = r"""

\section*{Professional Experience}
"""
experiences = user_data.get("professional_experience", [])
for data in experiences:
    pro_experience += fr"""
\textbf{{{data.get("title")}, {data.get("company")}}} \hfill {data.get("from")} -- {data.get("to")}
\begin{{itemize}}[leftmargin=*]
    {"\n    ".join([f"\\item {description}" for description in data.get("descriptions", [])])}
\end{{itemize}}

"""
file_data += pro_experience

## Projects

for section in projects:
    file_data += fr"""
\section*{{{section.get("section")}}}
"""
    for project in section.get("projects", []):
        file_data += fr"""
\textbf{{{project.get("title")}}}{f" - \\href{{{project.get("link", "")}}}{{{project.get("linkTool", "Github")}}}" if project.get("link") else ""} \\   
"""
        file_data += "\\\\\n".join([fr"\hspace*{{2em}}{description}" for description in project.get("descriptions", [])]) + "\\\\"
    
## Skills
skills = fr"""

\section*{{Skills}}
\begin{{itemize}}[leftmargin=*]
    \item \textbf{"\n    \\item \\textbf".join([f"{{{skill.get("title")}:}} {", ".join(skill.get("keywords"))}" for skill in user_data.get("skills", [])])}
\end{{itemize}}
"""
file_data += skills

## Languages
languages = fr"""
\section*{{Languages}}
{" \\\\\n".join(f"{language.get("lang", "")} ({language.get("level", "")})" for language in user_data.get("languages", []))}
"""
file_data += languages

## Hobies
hobbies = fr"""
\section*{{Hobbies}}
{", ".join(user_data.get("Hobbies"))}
"""
file_data += hobbies

## End Document
file_data += r"""
\end{document}
"""


PDF_PATH = os.path.join(os.path.dirname(__file__), f'CV_{user_data.get("lastName", "")}_{user_data.get("firstName", "")}.pdf')
url = "https://latexonline.cc/compile"

data = {"text": file_data}
response = requests.get(url, params=data)

if response.status_code == 200:
    with open(PDF_PATH, "wb") as pdf:
        pdf.write(response.content)
    print(f"✅ PDF saved as {PDF_PATH}")
else:
    print(f"❌ Failed: {response.status_code}\n{response.text}")
