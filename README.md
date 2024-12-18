# Flext 🚀

A lightweight Flask extension that brings Next.js-style API routing to Flask applications. Organize your Flask APIs using file-based routing, just like Next.js!

## Features ✨

- 📁 File-based routing similar to Next.js
- 🔄 Automatic HTTP method detection from filenames
- 🔌 Simple integration with existing Flask apps
- 0️⃣ Zero additional dependencies beyond Flask
- 🎯 Convention over configuration
- 🔧 Easy to extend and customize

## Installation 📦

```bash
# Currently local installation
git clone https://github.com/napjon/flext
cd flext
pip install -e .
```

## Quick Start 🚀

1. Create your API structure:

```
your_app/
├── app.py
├── api/
│   ├── hello/
│   │   ├── get.py
│   │   └── post.py
```

2. Write your endpoint in `api/hello/get.py`:

```python
def main(request):
    return {"message": "Hello World!"}
```

3. Setup your Flask app (`app.py`):

```python
from flask import Flask
from flext import Flext

app = Flask(__name__)
app = Flext(app)

if __name__ == '__main__':
    app.run(debug=True)
```

That's it! Your API endpoints are now available at:
- `GET /api/hello`
- `POST /api/hello`

## API Endpoint Structure 📝

Each endpoint should have a `main` function that accepts a Flask request object:

```python
def main(request):
    """
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        Response: Any Flask-compatible response
    """
    return {"status": "success"}
```

## Supported HTTP Methods 🔄

Files are automatically mapped to HTTP methods:
- `get.py` → GET
- `post.py` → POST
- `put.py` → PUT
- `delete.py` → DELETE
- `patch.py` → PATCH

## Configuration ⚙️

Customize Flext behavior during initialization:

```python
app = Flext(
    app,
    api_dir='custom_api_dir',  # Default: 'api'
    prefix='/api/v1',          # Default: '/api'
    debug=True                 # Default: False
)
```

## Deployment 🌐

### Traditional Server

```bash
pip install gunicorn
gunicorn app:app
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]
```

### Cloud Functions (GCP)

Modify the entry point for Google Cloud Functions:

```python
# main.py
from flask import Flask
from flext import Flext

app = Flask(__name__)
app = Flext(app)

# For Cloud Functions
def entry_point(request):
    return app(request)
```

## Common Patterns 📋

### Error Handling

Create a global error handler:

```python
# api/_middleware.py
def handle_errors(app):
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {"error": "Internal server error"}, 500
```

### Request Validation

Validate incoming requests:

```python
# api/users/post.py
from flask import jsonify

def main(request):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
        
    data = request.get_json()
    required = ['napjon', 'email']
    
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
        
    return jsonify({"status": "user created"})
```

### Database Integration

Use Flask's application context:

```python
# api/users/get.py
from flask import current_app

def main(request):
    db = current_app.config['DB']
    users = db.query(...)
    return jsonify(users)
```

## Development Guide 🛠️

### Project Structure

```
flext/
├── flext.py           # Main library code
├── setup.py          # Package setup
├── requirements.txt  # Dependencies
└── tests/           # Test cases
```

### Running Tests

```bash
pip install pytest
pytest tests/
```

### Future Development Ideas 💡

1. **Middleware Support**
   - Add support for middleware files (e.g., `_middleware.py`)
   - Enable global and route-specific middleware

2. **API Documentation**
   - Automatic OpenAPI/Swagger documentation generation
   - Integration with Flask-RESTX

3. **Hot Reloading**
   - Implement hot reloading for API routes
   - Development server with auto-reload

4. **Type Hints**
   - Add comprehensive type hints
   - Runtime type checking

5. **Route Validation**
   - Schema validation support
   - Pydantic integration

6. **CLI Tool**
   - Scaffold new API endpoints
   - Generate boilerplate code

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/napjon/flext
cd flext

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest
```

## Support 💬

- 📝 [Documentation](https://github.com/napjon/flext/wiki)
- 🐛 [Issue Tracker](https://github.com/napjon/flext/issues)
- 💻 [Examples](https://github.com/napjon/flext/tree/main/examples)

## License 📄

MIT License - see [LICENSE](LICENSE) for details

## Acknowledgments 🙏

- Inspired by Next.js API routes
- Built on top of Flask
- Made with ❤️ by the community