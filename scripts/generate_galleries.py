import os
import json
import datetime
from jinja2 import Template

PROJECTS_ROOT = './projects/images'
GALLERY_PAGE_OUTPUT_DIR = './projects/pages'
GALLERY_TEMPLATE_PATH = "./scripts/templates/galleries.template.html"
INDEX_TEMPLATE_PATH = "./scripts/templates/index.template.html"
SECTION_MAP_PATH = './projects/section_map.json'

JSON_KEY_ROOT = 'KEY/key.json'
IMG_KEY_ROOT = 'KEY/key.jpg'

LOG_FILE = './scripts/logs/generate_galleries.log'

def log(message):
    with open(LOG_FILE, 'a') as logfile:
        logfile.write(str(message) + '\n')

def read_section_meta(section_map, project, proj_path):
    key_json = os.path.join(proj_path, JSON_KEY_ROOT)
    key_img = os.path.join(proj_path, IMG_KEY_ROOT)
    if os.path.isfile(key_json) and os.path.isfile(key_img):
        with open(key_json) as file:
            meta = json.load(file)
            
        ## define and fill section info per category of section
        section = meta.get("section", "unknown")
        section_info = {}
        section_info["section"] = section
        section_info["header"] = section_map.get(section, {}).get("header", "unknown")
        section_info["description"] = section_map.get(section, {}).get("description", "unknown")
        section_info["nav_title"] = section_map.get(section, {}).get("nav_title", "unknown")
        
        ## to add to list of projects for this section category
        entry = {
            "project_path": os.path.join(GALLERY_PAGE_OUTPUT_DIR, f"{project}.html"),
            "category": meta.get("section", ""),
            "key_img": key_img,
            "caption": meta.get("caption", ""),
            "title": meta.get("title", ""),
            "description": meta.get("description", "")
        }
    return section_info, entry

def parse_projects(section_map, projects_root):
    projects = []
    sections = {}
    log(f"parse_projects\nSearching for projects in {projects_root}...")
    log("--Contents: " + (str(os.listdir(PROJECTS_ROOT)) if os.path.exists(PROJECTS_ROOT) else "*** Not found"))
    for project in os.listdir(projects_root):
        proj_path = os.path.join(projects_root, project)
        
        if not os.path.isdir(proj_path):
            continue  # Skip files like .DS_Store
        
        section_info, project_entry = read_section_meta(section_map, project, proj_path)
        if section_info["section"] not in sections:
            sections[section_info["section"]] = {
                "header": section_info["header"],
                "description": section_info["description"],
                "nav_title": section_info["nav_title"],
                "projects": []
            }
        sections[section_info["section"]]["projects"].append(project_entry)
        projects.append((project, proj_path))
    return projects, sections

def get_images(section_map, project_path):
    log(f"Getting images from {project_path}...")
    return [
        os.path.relpath(os.path.join(project_path, f), GALLERY_PAGE_OUTPUT_DIR)
        for f in sorted(os.listdir(project_path))
        if os.path.isfile(os.path.join(project_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

# generate individual gallery image pages
def generate_gallery_pages(template, projects, section_map):
    log(f"generate_gallery_pages\n...Found {len(projects)} projects.")
    log(projects)
    for project, proj_path in projects:
        images = get_images(section_map, proj_path)
        log(f"...Found {len(images)} images in {project}.")
        html = template.render(project_name=project, images=images)
        output_file = os.path.join(GALLERY_PAGE_OUTPUT_DIR, f"{project}.html")
        with open(output_file, 'w') as file:
            file.write(html)
        log(f"...Generated {output_file}")

# generate sections for index page
def generate_main_index(template, sections):
    log(f"generate_main_index\n...Found {len(sections)} sections.")
    sections_to_publish = ["cosplay", "miniatures", "bts", "coming"]
    sections_for_template = {}
    
    for target in sections_to_publish:
        if target in sections:
            section = sections[target]
            sections_for_template[target] = {
                "header": section.get("header", ""),
                "description": section.get("description", ""),
                "nav_title": section.get("nav_title", ""),
                "projects": section.get("projects", [])
            }

    for key, value in sections_for_template.items():
        log(f"-- {key}: {value}")
    
    html = template.render(sections = sections_for_template)
    with open("index.html", "w") as file:
        file.write(html)
    log("Generated html: index.html")

def main():
    # Clear previous log
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'w') as logf:
        logf.write(f"Gallery generation log    [{timestamp}]\n")
        
    with open(SECTION_MAP_PATH) as file:
        section_map = json.load(file)

    projects, sections = parse_projects(section_map, PROJECTS_ROOT)
    
    # generate the galery pages:
    with open(GALLERY_TEMPLATE_PATH) as file:
      gallery_template = Template(file.read())
    generate_gallery_pages(gallery_template, projects, section_map)        

    #generate the main index page
    with open(INDEX_TEMPLATE_PATH) as file:
        index_tempate = Template(file.read())
    generate_main_index(index_tempate, sections)

    print(f"Generated log file: {LOG_FILE}")

    
if __name__ == '__main__':
    main()
