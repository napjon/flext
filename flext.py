import os
import importlib.util
from pathlib import Path
from typing import Optional
from flask import Flask, request

class Flext:
    def __init__(
        self,
        app: Flask,
        api_dir: str = 'api',
        prefix: str = '/api',
        debug: bool = False
    ):
        self.flask_app = app  # Store the original Flask app
        self.api_dir = api_dir
        self.prefix = prefix
        self.debug = debug
        
        self._register_routes()
        
    def _register_routes(self):
        """Crawl API directory and register routes"""
        api_path = os.path.join(self.flask_app.root_path, self.api_dir)
        print("app path", self.flask_app.root_path)
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # api_path = os.path.join(base_dir, self.api_dir)
        print("api path", api_path)
        
        for path in Path(api_path).rglob('*.py'):
            # Get relative path components
            rel_path = os.path.relpath(path, api_path)
            dir_path = os.path.dirname(rel_path)
            file_name = os.path.basename(rel_path)
            
            # Skip if not a method file
            if file_name not in {'get.py', 'post.py', 'put.py', 'delete.py', 'patch.py'}:
                continue
                
            # Map file to HTTP method
            method = file_name.split('.')[0].upper()
                
            # Construct route path
            route_path = f"{self.prefix}/{dir_path}"
            if route_path.endswith('.'):
                route_path = route_path[:-1]
                
            if self.debug:
                print(f"Registering route: {route_path} [{method}]")
            
            # Import the module
            spec = importlib.util.spec_from_file_location(
                f"{self.api_dir}.{dir_path}.{file_name[:-3]}", 
                str(path)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            def create_endpoint(handler):
                def endpoint(*args, **kwargs):
                    return handler(request)
                return endpoint
            
            # Add route to Flask app
            self.flask_app.add_url_rule(
                route_path,
                f"{dir_path}_{file_name[:-3]}",
                create_endpoint(module.main),
                methods=[method]
            )

    @property
    def app(self):
        """Return the Flask app instance"""
        return self.flask_app