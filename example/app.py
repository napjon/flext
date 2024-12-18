import sys
sys.path.append('..')

from flask import Flask
from flext import Flext

app = Flask(__name__)
flext = Flext(app)  # Create Flext instance

if __name__ == '__main__':
    flext.app.run(debug=True)  # Use .app to get Flask instance