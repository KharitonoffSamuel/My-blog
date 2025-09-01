import sys
import os
from transformers import pipeline
import re

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

def mask_markdown(text):
    masks = {}
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

def chunk_text(text, max_chunk_size=400):
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
    print(f"[INFO] File input : {file}")
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python translate_hf.py <file_or_folder>")
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        if not path.endswith(".fr.md"):
            translate_file(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".md") and not f.endswith(".fr.md"):
                    translate_file(os.path.join(root, f))
    else:
        print(f"[ERROR] Path not found: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()