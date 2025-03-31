import logging
from contextlib import redirect_stdout
from io import StringIO

import webview
from server import app

logger = logging.getLogger(__name__)

def run_flask():
    # 启动 Flask（不阻塞）
    import threading
    from werkzeug.serving import make_server

    class FlaskThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.server = make_server('127.0.0.1', 5000, app)
            self.ctx = app.app_context()
            self.ctx.push()

        def run(self):
            self.server.serve_forever()

        def shutdown(self):
            self.server.shutdown()

    flask_thread = FlaskThread()
    flask_thread.start()
    return flask_thread

if __name__ == '__main__':
    stream = StringIO()
    with redirect_stdout(stream):
        flask_thread = run_flask()
        window = webview.create_window('Jotline', 'http://127.0.0.1:5000', width=1000, height=1000)
        webview.start(icon='static/icon.png')
        flask_thread.shutdown()
