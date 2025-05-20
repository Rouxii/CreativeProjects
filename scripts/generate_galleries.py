import os
from jinja2 import Template

IMAGES_ROOT = './galleries/images'
OUTPUT_DIR = './galleries/pages'  # Where to save the generated HTML files

GALLERY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name|title }} Gallery</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Navigation -->
    <nav>
        <ul class="nav-links">
            <li><a href="./index.html#about">Home</a></li>
            <li><a href="./index.html#cosplay">Cosplay</a></li>
            <li><a href="#miniatures">Miniatures</a></li>
            <!-- <li><a href="#pottery">Pottery</a></li>
            <li><a href="#espresso">Espresso</a></li> -->
        </ul>
    </nav>
    <h1>{{ project_name|title }} Gallery</h1>
    <div class="gallery">
    {% for img in images %}
        <div class="gallery-item">
            <img src="{{ img }}" alt="{{ project_name }} image" class="gallery-img">
        </div>
    {% endfor %}
    </div>
    <p><a href="index.html">Back to main page</a></p>
    <!-- Footer -->
    <footer>
        <div class="container footer-content">
            <p>© 2025 a Rui Makes Stuff production</p>
            <a href="https://www.instagram.com/ruimakesstuff/" target="_blank" class="instagram-link">insta</a>
        </div>
    </footer>
</body>
</html>
"""

def find_projects(images_root):
    projects = []
    for category in os.listdir(images_root):
        cat_path = os.path.join(images_root, category)
        if os.path.isdir(cat_path):
            for project in os.listdir(cat_path):
                proj_path = os.path.join(cat_path, project)
                if os.path.isdir(proj_path):
                    projects.append((category, project, proj_path))
    return projects

def get_images(project_path):
    return [
        os.path.relpath(os.path.join(project_path, f))
        for f in sorted(os.listdir(project_path))
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

def main():
    template = Template(GALLERY_TEMPLATE)
    projects = find_projects(IMAGES_ROOT)
    for category, project, proj_path in projects:
        images = get_images(proj_path)
        html = template.render(project_name=project, images=images)
        output_file = os.path.join(OUTPUT_DIR, f"{project}.html")
        with open(output_file, 'w') as f:
            f.write(html)
        print(f"Generated {output_file}")

if __name__ == '__main__':
    main()