import flask
import requests

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DASHBOARD_CONF', silent=True)

# Handlers ---------

@app.route('/')
def overview_zte(*args, **kwargs):
    ctx = {
        'metrc': 'commits',
        'metric_label': 'Commits'
    }
    return flask.render_template('zte-overview.html', **ctx)

@app.route('/api/<path:path>')
def cached_proxy(path):
    API_ROOT = 'http://stackalytics.com/'
    full_url = API_ROOT + flask.request.full_path
    r = requests.get(full_url)
    return flask.Response(
        r.text,
        status = r.status_code,
        content_type = r.headers['content-type']
    )

if __name__ == "__main__":
    app.run()
