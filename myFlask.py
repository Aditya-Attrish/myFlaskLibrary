from wsgiref.simple_server import make_server
import webbrowser as web
from static_middlerware import StaticMiddleware

def render_tamplate(path):
	with open(f"./tamplates/{path}", 'r') as html:
		content = html.read()
	return content

class MyFlask:
    def __init__(self):
        self.routes = {}  # To store URL patterns and their handlers
    
    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def __call__(self, environ, start_response):
    	
    	app = StaticMiddleware(self.handle_request)
    	return app(environ, start_response)
    	
    def handle_request(self, environ, start_response):
        path = environ['PATH_INFO']
        if path in self.routes:
            status = '200 OK'
            response = self.routes[path]()
        else:
            status = '404 Not Found'
            response = "<h1>404 Not Found</h1>"
        
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response.encode('utf-8')]
    
    def run(self,host='localhost', port=8000):
        with make_server(host, port, self) as httpd:
            print(f"Serving on port {port}...")
            print(f"Visit http://localhost:{port} in your browser")
            web.open(f"http://{host}:{port}")
            httpd.serve_forever()

