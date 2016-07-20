import flask
import requests
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DASHBOARD_CONF', silent=True)

# Handlers ---------

@app.route('/')
def zte_overview():
    # We don't handle complex request locally
    if flask.request.args:
        return cached_proxy()

    ctx = {
        'metrc': 'commits',
        'metric_label': 'Commits'
    }
    return flask.render_template('zte-overview.html', **ctx)

@app.route('/<path:dummy>')
def catch_all(dummy):
    return cached_proxy()

def cached_proxy():
    UPSTREAM = 'http://stackalytics.com/'
    full_url = UPSTREAM + flask.request.full_path
    r = cache.get(full_url)
    if r is None:
        r = requests.get(full_url)
        cache.set(full_url, r, timeout = 60 * 60)

    return flask.Response(
        r.text,
        status = r.status_code,
        content_type = r.headers['content-type']
    )

if __name__ == "__main__":
    app.run()
