import os
from jinja2 import Template

IMAGES_ROOT = './galleries/images'
OUTPUT_DIR = './galleries/pages'  # Where to save the generated HTML files
LOG_FILE = './scripts/logs/generate_galleries.log'

def log(message):
    with open(LOG_FILE, 'a') as logfile:
        logfile.write(message + '\n')

GALLERY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ project_name|title }} Gallery</title>
    <link rel="stylesheet" href="../../styles.css">
</head>
<body>
    <!-- Navigation -->
    <nav>
        <ul class="nav-links">
            <li><a href="../../index.html#about">Home</a></li>
            <li><a href="../../index.html#cosplay">Cosplay</a></li>
            <li><a href="../../#miniatures">Miniatures</a></li>
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
    log(f"Searching for projects in {images_root}...")
    for project in os.listdir(images_root):
        proj_path = os.path.join(images_root, project)
        # Skip files like .DS_Store
        if not os.path.isdir(proj_path):
            continue
        projects.append(('', project, proj_path))
    return projects

def get_images(project_path):
    log(f"Getting images from {project_path}...")
    return [
        os.path.relpath(os.path.join(project_path, f), OUTPUT_DIR)
        for f in sorted(os.listdir(project_path))
        if os.path.isfile(os.path.join(project_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

def main():
    # Clear previous log
    with open(LOG_FILE, 'w') as logf:
        logf.write("Gallery generation log\n")

    log("Looking for images in: " + os.path.abspath(IMAGES_ROOT))
    log("Exists? " + str(os.path.exists(IMAGES_ROOT)))
    log("Contents: " + (str(os.listdir(IMAGES_ROOT)) if os.path.exists(IMAGES_ROOT) else "Not found"))

    template = Template(GALLERY_TEMPLATE)
    projects = find_projects(IMAGES_ROOT)
    log(f"...Found {len(projects)} projects.")
    for category, project, proj_path in projects:
        images = get_images(proj_path)
        log(f"...Found {len(images)} images in {project}.")
        html = template.render(project_name=project, images=images)
        output_file = os.path.join(OUTPUT_DIR, f"{project}.html")
        with open(output_file, 'w') as f:
            f.write(html)
        log(f"Generated {output_file}")
        
    print(f"generated log file: {LOG_FILE}")

if __name__ == '__main__':
    main()