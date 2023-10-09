import sys
import time
start = time.time()
if '--time=1' in sys.argv:
    print("Loading wikipediaFuncs.py...", end="\t")

import os
import wikipedia
import wikipediaapi
import json

dirname = os.path.dirname(__file__)

api = wikipediaapi.Wikipedia('SchoolScienceFestModel (4n0nym0us1147@gmail.com)', 'en')
with open(os.path.join(dirname, "jsons/knowledge_base.json"), "r", encoding="utf-8") as fl:
    knowledge_base = json.load(fl)


def get_wiki_content_api(disease: str, cat: str = 'summary', summaryLen: int = 5):
    search = wikipedia.search(disease)[0]
    page = api.page(search)
    sections = page.sections

    if 'precaution' in cat:
        searchLi = ['precaution', 'prevention']
    elif 'cause' in cat:
        searchLi = ['cause']
    elif 'symptom' in cat:
        searchLi = ['sign', 'symptom']
    elif 'treatment' in cat:
        searchLi = ['treatment', 'vaccine', 'management']
    else:
        return ". ".join(page.summary.split(". ")[:summaryLen]) + "."

    for find in searchLi:
        for section in sections:
            if find in section.title.lower():
                if section.text != "":
                    return section.text
                else:
                    txt = ""
                    for subsection in page.section_by_title(section.title).sections:
                        if subsection.text == "":
                            for subsubseciton in page.section_by_title(subsection.title).sections:
                                txt += subsubseciton.title + "\n" + subsubseciton.text + "\n"
                            txt += "\n\n"

                    if txt == "" and cat == 'precaution':
                        subsection = [sub for sub in page.section_by_title('Treatment').sections if
                                      sub.title == 'Conservative']
                        txt = subsection[0].text
                    # print(txt)
                    return txt


def get_content(name_disease: str, cat: str):
    for disease in knowledge_base['diseases']:
        for name in disease['name']:
            if name_disease.lower() in name.lower():
                return disease[cat]
    else:
        content = get_wiki_content_api(name_disease, cat).split(". ")
        return content


end = time.time()
if '--time=1' in sys.argv:
    print(f"Loaded wikipediaFuncs.py in {round(end-start)/10}s")
