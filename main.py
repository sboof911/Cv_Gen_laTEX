import os, sys
from latex_format import latex_builder, get_data
import requests


url = "https://latexonline.cc/compile"

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user_data')
language = sys.argv[1] if len(sys.argv) > 1 else "en"
user_data, projects, profile_description = get_data(DATA_FOLDER, language)
file_data = latex_builder.build_tex(user_data, projects, profile_description)
with open("output.tex", "w", encoding='utf-8') as file:
    file.write(file_data)



PDF_PATH = os.path.join(os.path.dirname(__file__), f"CV_{user_data.get('lastName','')}_{user_data.get('firstName','')}.pdf")



# # latexonline expects either raw text param or base64; existing approach encodes
# tex_bytes = file_data.encode('utf-8')
# b64_encoded = base64.b64encode(tex_bytes).decode("utf-8")
# safe_text = urllib.parse.quote_plus(b64_encoded)

# data = {"text": safe_text}
# response = requests.get(url, params=data)

# if response.status_code == 200:
#     with open(PDF_PATH, "wb") as pdf:
#         pdf.write(response.content)
#     print(f"✅ PDF saved as {PDF_PATH}")
# else:
#     print(f"❌ Failed: {response.status_code}\n{response.text}")
