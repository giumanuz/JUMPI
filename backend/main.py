import os

from app import create_app
from app.config import Config
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5123))
    Config.create_temp_dirs()
    app.run(debug=debug, host=host, port=port)
