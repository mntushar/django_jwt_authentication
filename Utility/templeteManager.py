import os

from django.conf import settings


class TemplateManager:
    @staticmethod
    def get_script() -> str:
        js_directory = os.path.join(settings.BASE_DIR, 'static/custom_webpack_conf_2/js/')

        # List all JavaScript files in the directory
        js_files = [f for f in os.listdir(js_directory) if f.endswith('.js')]

        # Generate <script> tags with relative paths for each JS file
        script_tags = ''.join(
            f'<script src="/static/custom_webpack_conf_2/js/{js_file}"></script>'
            for js_file in js_files
        )

        return script_tags