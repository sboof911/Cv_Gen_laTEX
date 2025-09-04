from typing import Dict, List

from pylatex import Document, Center, Package, NoEscape
from pylatexenc.latexencode import unicode_to_latex


def build_tex(user_data: Dict, projects: List[Dict], profile_description: str) -> str:
    """Build a LaTeX document string from data using pylatex/pylatexenc when available.

    This returns the full .tex content as a string.
    """
    def safe(s: str) -> str:
        return unicode_to_latex(s or "", non_ascii_only=False)

    doc = Document(documentclass='article', document_options='a4paper,11pt')
    doc.packages.append(Package('geometry', options='margin=1in'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('titlesec'))
    doc.packages.append(Package('needspace'))
    doc.packages.append(Package('hyperref', options='hidelinks'))

    # add titlesec formatting and custom command
    doc.preamble.append(NoEscape(r'\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]'))
    doc.preamble.append(NoEscape(r'\newcommand{\cvitem}[2]{\noindent\textbf{#1} \quad #2 \par}'))

    with doc.create(Center()) as center:
        center.append(NoEscape(r'{\Huge \textbf{' + safe(user_data.get('lastName','').upper()) + ' ' + safe(user_data.get('firstName','')) + r'}}\\[0.3em]'))
        center.append(NoEscape(safe(user_data.get('title','')) + r'\\[0.3em]'))
        # email clickable, label escaped
        center.append(NoEscape(r'\href{mailto:' + user_data.get('email','') + r'}{' + safe(user_data.get('email','')) + r'}'))
        center.append(NoEscape(r' \quad ' + safe(user_data.get('phone','')) + r' \quad '))
        center.append(NoEscape(r'\href{' + user_data.get('linkedin','') + r'}{LinkedIn} \quad '))
        center.append(NoEscape(r'\href{' + user_data.get('github','') + r'}{GitHub}'))

    
    # Profile
    doc.append(NoEscape(r'\section*{Profile}'))
    
    def edit_description(text: str) -> str:
        # Remove leading/trailing whitespace and replace newlines with LaTeX line breaks
        return text.strip().replace('\n', r'\newline ')
    doc.append(NoEscape(edit_description(safe(profile_description))))

    # Education
    doc.append(NoEscape(r'\section*{Education}'))
    educations = user_data.get('education', [])
    educations.sort(key=lambda x: x.get('from_year', 0), reverse=True)
    for ed in educations:
        dates = safe(ed.get('from_year','')) + '--' + safe(ed.get('to_year',''))
        desc = safe(ed.get('degree','')) + ' in ' + safe(ed.get('field','')) + ', ' + safe(ed.get('institution',''))
        # place the date in a fixed-width box and the description in a top-aligned minipage so
        # the description wraps and stays fully justified while the date remains at left
        label_width = '3.5cm'
        tex = (
            r'\noindent\makebox[' + label_width + r'][l]{\textbf{' + dates + r'}}'
            + r'\begin{minipage}[t]{\dimexpr\linewidth-' + label_width + r'\relax}'
            + desc
            + r'\end{minipage}\par'
        )
        doc.append(NoEscape(tex))

    # Professional Experience
    profs = user_data.get('professional_experience', [])
    if profs:
        doc.append(NoEscape(r'\section*{Professional Experience}'))
        for ex in profs:
            doc.append(NoEscape(r'\textbf{' + safe(ex.get('title','')) + ', ' + safe(ex.get('company','')) + '} \\hfill ' + safe(ex.get('from','')) + ' -- ' + safe(ex.get('to',''))))
            descriptions = ex.get('descriptions', []) or []
            if descriptions:
                doc.append(NoEscape(r'\begin{itemize}[leftmargin=*]'))
                
                for d in descriptions:
                    doc.append(NoEscape(r'\item ' + safe(d)))
                doc.append(NoEscape(r'\end{itemize}'))

    # Projects
    for section in projects:
        doc.append(NoEscape(r'\section*{' + safe(section.get('section','')) + '}'))
        for project in section.get('projects', []):
            title = safe(project.get('title',''))
            link = project.get('link','')
            descriptions = project.get('descriptions', [])
            linktool = safe(project.get('linkTool','Github'))
            doc.append(NoEscape(rf'\needspace{{{len(descriptions)}\baselineskip}}'))
            if link:
                doc.append(NoEscape(rf'\noindent \textbf{{{title}}} - \href{{{link}}}{{{linktool}}}'))
            else:
                doc.append(NoEscape(rf'\noindent \textbf{{{title}}}'))
            doc.append(NoEscape(r'\begin{itemize}[leftmargin=2em,label={},parsep=0pt,topsep=1em]'))
            for desc in descriptions:
                doc.append(NoEscape(rf'\item {safe(desc)}'))
            doc.append(NoEscape(r'\end{itemize}'))

    # Skills
    skills = user_data.get('skills', []) or []
    if skills:
        doc.append(NoEscape(r'\section*{Skills}'))

        doc.append(NoEscape(r'\begin{itemize}[leftmargin=*]'))

        for skill in skills:
            doc.append(NoEscape(rf'\item \textbf{{{safe(skill.get('title',''))}}}: {safe(', '.join(skill.get('keywords', [])))}'))
        doc.append(NoEscape(r'\end{itemize}'))


    # Languages
    doc.append(NoEscape(r'\section*{Languages}'))
    langs = [safe(f"{l.get('lang','')} ({l.get('level','')})") for l in user_data.get('languages', [])]
    for i, L in enumerate(langs):
        doc.append(NoEscape(L))
        doc.append('\n')

    # Hobbies
    doc.append(NoEscape(r'\section*{Hobbies}'))
    hobbies = [safe(f"{hobbie}") for hobbie in user_data.get('Hobbies', [])]
    for i, hobbie in enumerate(hobbies):
        doc.append(NoEscape(hobbie))
        doc.append('\n')

    return doc.dumps()
