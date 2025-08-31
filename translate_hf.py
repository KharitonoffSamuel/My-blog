from transformers import pipeline
import sys

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

file = sys.argv[1]

with open(file, "r") as f:
    text = f.read()

translated = translator(text, max_length=400)[0]["translation_text"]

output_file = file.replace(".md", ".fr.md")
with open(output_file, "w") as f:
    f.write(translated)

print(f"Translated file created: {output_file}")