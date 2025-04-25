import datetime
import json

from flask import Flask, request, render_template_string
import werkzeug.exceptions

app = Flask(__name__)

all_methods = 'POST PUT GET HEAD DELETE PATCH OPTIONS'.split()
fruits = 'banana apple blueberry'.split()

form_html = """
<a onclick="window.location = window.location">GET</a>
<form>
    <select name="fruit">
        {% for fruit in fruits %}
            <option value="{{fruit}}">{{fruit}}</option>
        {% endfor %}
    </select>
    <textarea name="textarea_data" value="textarea_value"></textarea>
    <input type="button" value="POST" onclick="this.form.method = 'POST'; this.form.submit()">
</form>
"""


@app.route('/', defaults={'path': ''}, methods=all_methods)
@app.route('/<path:path>', methods=all_methods)
def get_root(path: str):
    contents = []
    contents.append(f"Method: {request.method}")
    contents.append(f'Requested path: {path}')
    contents.append(f"Query string: {request.query_string}")
    contents.append(f"Headers: {json.dumps(dict(request.headers), indent=4)}")
    contents.append(f"IP Address: {request.remote_addr}")

    contents.append(f"Body: {request.get_data().decode('utf-8')}")
    contents.append(f"Form: {request.form}")
    contents.append(f"Cookies: {request.cookies}")

    contents.append(f"Content type: {request.content_type}")
    contents.append(f"Content Length: {request.content_length}")
    contents.append(f"User Agent: {request.user_agent.string}")
    contents.append(f"Server time: {datetime.datetime.now()}")

    try:
        contents.append(f"JSON: {request.json}")
    except werkzeug.exceptions.UnsupportedMediaType:
        pass

    for content in contents:
        print(content)

    form_str = render_template_string(form_html, fruits=fruits)
    contents.insert(0, form_str)

    return f'<!DOCTYPE html><html><pre><code>{"\n".join(contents)}</code></pre></html>'



