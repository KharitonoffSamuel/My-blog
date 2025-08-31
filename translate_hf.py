from transformers import pipeline
import sys
import re
import os

# Initialise le pipeline de traduction
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

# Récupérer le chemin racine depuis l'argument
root_path = sys.argv[1]

# Fonction pour parcourir récursivement tous les fichiers .md
def get_md_files(path):
    md_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

# Fonction pour protéger liens, images et titres Markdown
def mask_markdown(text):
    masks = {}
    # On protège les liens, images, titres Markdown et code inline
    pattern = r'(\[.*?\]\(.*?\)|\!\[.*?\]\(.*?\)|`[^`]+`|^#+ )'
    def replacer(match):
        key = f"__MASK{len(masks)}__"
        masks[key] = match.group(0)
        return key
    masked_text = re.sub(pattern, replacer, text, flags=re.MULTILINE)
    return masked_text, masks

def unmask_markdown(text, masks):
    for key, val in masks.items():
        text = text.replace(key, val)
    return text

# Fonction principale pour traduire un fichier
def translate_file(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    front_matter = []
    content_lines = []
    in_front_matter = False
    front_matter_done = False

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

    # Traduire uniquement le titre du front matter
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

    # Traduire le contenu Markdown en protégeant liens, images et titres
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

# Parcourir tous les fichiers Markdown sous le chemin racine
md_files = get_md_files(root_path)
for md_file in md_files:
    # Ignorer les fichiers déjà traduits
    if not md_file.endswith(".fr.md"):
        translate_file(md_file)