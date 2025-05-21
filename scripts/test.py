import os
from jinja2 import Template

GALLERY_TEMPLATE_PATH = "./scripts/templates/galleries.template.html"
INDEX_TEMPLATE_PATH = "./scripts/templates/index.template.html"
LOG_FILE = './scripts/logs/generate_galleries.log'


if __name__ == '__main__':
    print("Exists? " + str(os.path.exists(GALLERY_TEMPLATE_PATH)))
        # Load the template from file
        
    with open(GALLERY_TEMPLATE_PATH) as f:
        template = Template(f.read())
    print(template)
    
