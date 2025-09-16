#!/usr/bin/env python3
import os
import sys
import datetime
import shutil

# Configuration
CONTENT_DIR = "content/posts"
TEMPLATES_DIR = "post-templates"   # là où tu stockes tes templates (md + cover.svg)

def create_post(slug, template="generic"):
    # Récupérer la date courante
    today = datetime.date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")

    # Numéro d'ordre du post (00, 01, 02...) basé sur les dossiers déjà présents
    target_dir = os.path.join(CONTENT_DIR, year, month)
    os.makedirs(target_dir, exist_ok=True)

    existing = [d for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))]
    post_num = f"{len(existing):02d}"  # format "00", "01", "02"...
    post_dir = os.path.join(target_dir, f"{post_num}-{slug}")

    if os.path.exists(post_dir):
        print(f"❌ Error: Post {post_dir} already exists.")
        sys.exit(1)

    os.makedirs(post_dir)

    # Copier le template choisi
    template_md = os.path.join(TEMPLATES_DIR, f"{template}.md")
    template_cover = os.path.join(TEMPLATES_DIR, f"{template}-cover.svg")

    if not os.path.exists(template_md):
        print(f"❌ Error: Template {template_md} not found.")
        sys.exit(1)

    # Copier index.md
    target_md = os.path.join(post_dir, "index.md")
    shutil.copy(template_md, target_md)

    # Copier cover.svg (si existe)
    if os.path.exists(template_cover):
        target_cover = os.path.join(post_dir, "cover.svg")
        shutil.copy(template_cover, target_cover)

    print(f"✅ New post created: {target_md}")
    print(f"   Cover: {template_cover if os.path.exists(template_cover) else 'No cover'}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: new_post.py <slug> [template]")
        sys.exit(1)

    slug = sys.argv[1]
    template = sys.argv[2] if len(sys.argv) > 2 else "generic"

    create_post(slug, template)