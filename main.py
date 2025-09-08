import os, sys
from latex_format import latex_builder, get_data
from generate_pdf.github import github_repo, FILE_PATH_IN_REPO
from generate_pdf import compile_latex_from_github


url = "https://latexonline.cc/data?target=pdf"

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user_data')
language = sys.argv[1] if len(sys.argv) > 1 else "en"
user_data, projects, profile_description = get_data(DATA_FOLDER, language)
file_data = latex_builder.build_tex(user_data, projects, profile_description)
with open("main.tex", "w", encoding='utf-8') as file:
    file.write(file_data)

github = github_repo()

github.upload_file("main.tex")

PDF_PATH = os.path.join(os.path.dirname(__file__), f"CV_{user_data.get('lastName','')}_{user_data.get('firstName','')}.pdf")

compile_latex_from_github(github.url, FILE_PATH_IN_REPO, PDF_PATH)

github.delete_file()
print(f"✅ PDF generated: {PDF_PATH}")
