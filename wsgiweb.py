from gevent.pywsgi import WSGIServer
from ai_web import app
http_server = WSGIServer(('0.0.0.0', 80), app)
http_server.serve_forever()
