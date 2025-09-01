import sys
import os
from transformers import pipeline
import re

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

file = sys.argv[1]
print(f"[INFO] File input : {file}")

def mask_markdown(text):
    masks = {}
    pattern = r'(\[.*?\]\(.*?\)|\!\[.*?\]\(.*?\)|`[^`]+`|^#+ )'
    def replacer(match):
        key = f"__MASK{len(masks)}__"
        masks[key] = match.group(0)
        return key
    import re
    masked_text = re.sub(pattern, replacer, text, flags=re.MULTILINE)
    return masked_text, masks

def unmask_markdown(text, masks):
    for key, val in masks.items():
        text = text.replace(key, val)
    return text

def chunk_text(text, max_chunk_size=400):
    # Découpe en morceaux par phrases ou paragraphes
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_chunk_size:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "
    if current:
        chunks.append(current.strip())
    return chunks

def translate_file(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # --- Front matter
    front_matter = []
    content_lines = []
    in_front_matter = False
    done = False

    for line in lines:
        if line.strip() == "---":
            if not in_front_matter:
                in_front_matter = True
            elif in_front_matter:
                done = True
                in_front_matter = False
            front_matter.append(line)
        elif in_front_matter and not done:
            front_matter.append(line)
        else:
            content_lines.append(line)

    # Traduire seulement le titre
    new_front_matter = []
    title_pattern = re.compile(r"^title:\s*['\"]?(.*?)['\"]?$")
    for line in front_matter:
        match = title_pattern.match(line.strip())
        if match:
            original_title = match.group(1)
            translated_title = translator(original_title, max_length=200)[0]["translation_text"]
            new_front_matter.append(f"title: '{translated_title}'\n")
        else:
            new_front_matter.append(line)

    # Traduire le contenu par morceaux
    content_text = "".join(content_lines)
    masked, masks = mask_markdown(content_text)
    chunks = chunk_text(masked, max_chunk_size=400)

    translated_parts = []
    for c in chunks:
        translated = translator(c, max_length=400)[0]["translation_text"]
        translated_parts.append(translated)

    translated_masked = " ".join(translated_parts)
    final_content = unmask_markdown(translated_masked, masks)

    # Sauvegarde
    output_file = file.replace(".md", ".fr.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(new_front_matter)
        f.write(final_content)

    print(f"[INFO] Translated file created: {output_file}")