import base64
from flask import Flask, send_file, request
from scrapyd_api import ScrapydAPI

app = Flask(__name__)
scrapyd = ScrapydAPI('http://localhost:6800')
project = 'dailyteedeals'


@app.route("/status/<job_id>")
def status(job_id):
    """
    Get the job status for a single job.

    Args:
      job_id: Job ID

    Returns:
      'invalid', 'running', 'pending' or 'finished'.
    """
    status = scrapyd.job_status(project, job_id)
    if status == '':
        status = 'invalid'

    return status

@app.route("/download/<job_id>")
def download(job_id):
    """
    Download the feed for a single job.

    Args:
      job_id: Job ID

    Returns:
      Item feed for job in JSONLines / .jl format.
      If the job hasn't finished, it will return a 404.

    """
    if scrapyd.job_status(project, job_id) != 'finished':
        return 'Job not finished', 404

    finished = scrapyd.list_jobs(project)['finished']
    spider = next((item['spider'] for item in finished if item["id"] == job_id))
    filepath = "../items/%s/%s/%s.jl" % (project, spider, job_id)
    return send_file(filepath, mimetype='application/x-jsonlines')

@app.route("/schedule", methods=['POST'])
def schedule():
    """
    Schedule a spider to start scraping.

    Returns:
      Job ID

    """
    spider = request.form['spider']
    return scrapyd.schedule(project, spider)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6900, processes=20)
