__author__ = 'Tamir'


HTML_FILE_TEMPLATE = """ <a href="/file_request/%s">
                            <div class="img-single">
                            <img src="static/document_file_icon_2.png">
                            <h3>%s</h3>
                            </div></a>"""

print HTML_FILE_TEMPLATE.replace("%s", "lol.txt")