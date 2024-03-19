import secrets
import threading
from flask import Flask, request, render_template_string, make_response
from playwright.sync_api import sync_playwright

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
flag_url = f"/{secrets.token_urlsafe(64)}"

flag = "CCSC{1f_1t_acc3pt5_1NpuT_1t_W!LL_b3_XSSed}"

submissions_dict = {}


@app.route('/')
def index():
    return render_template_string(open('index.html').read())


@app.route(flag_url)
def bot_endpoint():
    response = make_response("How did you find this?")
    response.set_cookie('flag', flag, httponly=False, secure=False)
    return response


@app.route('/report', methods=['POST'])
def navigate():
    report = request.form.get('report')
    report_lower = report.lower()
    attempt_code = secrets.token_urlsafe(8)
    if "script" in report_lower:
        return "No scripts allowed!"
    elif "onload" in report_lower:
        return "No onload allowed!"
    elif "onerror" in report_lower:
        return "No onerror allowed!"
    else:
        attempt_html = f"<h1>Report Submitted:</h1><br>{report}"
        submissions_dict[attempt_code] = attempt_html
        bot_thread = threading.Thread(target=run_bot, args=(attempt_code,))
        bot_thread.start()
        return attempt_html


@app.route('/xss/<unique_id>')
def xss_trigger_endpoint(unique_id):
    if unique_id in submissions_dict.keys():
        return make_response(submissions_dict[unique_id])
    else:
        return "No such submission"


def run_bot(submission_id):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f'http://localhost:5000{flag_url}')
            page.goto(f'http://localhost:5000/xss/{submission_id}')
            page.wait_for_timeout(3000)
            page.close()
            browser.close()
    except Exception as e:
        print(f'Exception occurred while checking submission: {e}')


if __name__ == '__main__':
    app.run()
