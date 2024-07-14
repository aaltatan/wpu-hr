import os
import logging
from pathlib import Path
from core.wsgi import application
from waitress import serve
from dotenv import load_dotenv


logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    
    BASE_DIR = Path().resolve()
    load_dotenv(BASE_DIR / '.env')
    
    port = int(os.getenv('PORT'))
    host = os.getenv('HOST')
    
    serve(application, host=host, port=port)
