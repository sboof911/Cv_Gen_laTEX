import requests

def compile_latex_from_github(git_repo_url, main_tex_file="main.tex", pdf_output_path="output.pdf"):
    api_url = (
        "https://latexonline.cc/compile"
        f"?git={git_repo_url}"
        f"&target={main_tex_file}"
    )

    response = requests.get(api_url)

    if response.status_code == 200 and response.headers.get("Content-Type") == "application/pdf":
        with open(pdf_output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ PDF saved as {pdf_output_path}")
    else:
        print(f"❌ Failed to compile PDF: {response.status_code}")
        print(response.text)
