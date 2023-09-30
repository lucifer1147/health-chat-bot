import json
with open("jsons/knowledge_base.json", "r", encoding="utf-8") as fl:
    knowledge_base = json.load(fl)

tags = ['about', 'precaution', 'symptoms', 'treatments']

for disease in knowledge_base['diseases']:
    for tag in tags:
        content = disease[tag][0]
        contentLi = []
        for line in content.splitlines():
            contentLi.extend(line.split(". "))

        disease[tag] = contentLi

with open("jsons/knowledge_base_final.json", "w", encoding="utf-8") as fl:
    json.dump(knowledge_base, fl)

