import os
from mimetypes import guess_type

class StaticMiddleware:
    def __init__(self, app, static_url='/static', static_folder='static'):
        self.app = app
        self.static_url = static_url
        self.static_folder = static_folder
    
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        
        # Check if this is a static file request
        if path.startswith(self.static_url):
            # Convert URL path to filesystem path
            relative_path = path[len(self.static_url):].lstrip('/')
            file_path = os.path.join(self.static_folder, relative_path)
            
            # Security check to prevent directory traversal
            file_path = os.path.abspath(file_path)
            if not file_path.startswith(os.path.abspath(self.static_folder)):
                start_response('403 Forbidden', [('Content-type', 'text/plain')])
                return [b'403 Forbidden']
            
            # Check if file exists
            if os.path.isfile(file_path):
                # Determine MIME type
                mime_type, _ = guess_type(file_path)
                mime_type = mime_type or 'application/octet-stream'
                
                # Read and serve the file
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                
                start_response('200 OK', [
                    ('Content-type', mime_type),
                    ('Content-length', str(len(file_content)))
                ])
                return [file_content]
            else:
                start_response('404 Not Found', [('Content-type', 'text/plain')])
                return [b'404 Not Found']
        
        # Not a static file request, pass to the app
        return self.app(environ, start_response)