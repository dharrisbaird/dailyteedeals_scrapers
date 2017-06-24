import base64
from flask import Flask, send_file, render_template
from scrapyd_api import ScrapydAPI
from utils import gzipped

app = Flask(__name__)
scrapyd = ScrapydAPI('http://localhost:6800')
project = 'dailyteedeals'


@app.route("/status/<job_id>")
def status(job_id):
    return scrapyd.job_status(project, job_id)

@app.route("/download/<job_id>")
@gzipped
def download(job_id):
    if scrapyd.job_status(project, job_id) != 'finished':
        return 'Job not finished', 404

    finished = scrapyd.list_jobs(project)['finished']
    spider = next((item['spider'] for item in finished if item["id"] == job_id))
    filepath = "../items/%s/%s/%s.jl" % (project, spider, job_id)
    return send_file(filepath, mimetype='application/x-jsonlines')

@app.route("/schedule/<spider>")
def schedule(spider):
    return scrapyd.schedule(project, spider)

@app.route('/')
def routes():
  routes = []
  for rule in app.url_map.iter_rules():
    if "GET" in rule.methods:
      url = rule.rule
      routes.append(url)
  return render_template('routes.html', routes=routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6900, processes=20)
