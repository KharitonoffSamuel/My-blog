from transformers import pipeline
import sys
import re

# Initialise le pipeline de traduction
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

# Fichier à traduire
file = sys.argv[1]

# Lire le fichier
with open(file, "r", encoding="utf-8") as f:
    lines = f.readlines()

front_matter = []
content_lines = []
in_front_matter = False
front_matter_done = False

# Séparer le front matter et le contenu
for line in lines:
    if line.strip() == "---":
        if not in_front_matter:
            in_front_matter = True
        elif in_front_matter:
            front_matter_done = True
            in_front_matter = False
        front_matter.append(line)
    elif in_front_matter and not front_matter_done:
        front_matter.append(line)
    else:
        content_lines.append(line)

# Traduire uniquement le titre dans le front matter
new_front_matter = []
title_pattern = re.compile(r"^title:\s*['\"]?(.*?)['\"]?$")
for line in front_matter:
    match = title_pattern.match(line.strip())
    if match:
        original_title = match.group(1)
        translated_title = translator(original_title, max_length=200)[0]["translation_text"]
        new_line = f"title: '{translated_title}'\n"
        new_front_matter.append(new_line)
    else:
        new_front_matter.append(line)

# Fonction pour protéger les liens et balises Markdown
def mask_markdown(text):
    masks = {}
    pattern = r'(\[.*?\]\(.*?\)|\!\[.*?\]\(.*?\)|`[^`]+`|#+ )'
    def replacer(match):
        key = f"__MASK{len(masks)}__"
        masks[key] = match.group(0)
        return key
    masked_text = re.sub(pattern, replacer, text)
    return masked_text, masks

def unmask_markdown(text, masks):
    for key, val in masks.items():
        text = text.replace(key, val)
    return text

# Traduire le contenu Markdown en protégeant la structure
content_text = "".join(content_lines)
masked_content, masks = mask_markdown(content_text)
translated_masked_content = translator(masked_content, max_length=400)[0]["translation_text"]
final_content = unmask_markdown(translated_masked_content, masks)

# Écrire le fichier traduit
output_file = file.replace(".md", ".fr.md")
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(new_front_matter)
    f.write(final_content)

print(f"Translated file created: {output_file}")