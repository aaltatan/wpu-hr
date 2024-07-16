import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

import logging


config = logging.basicConfig(
    filemode='a',
    filename='logger.log',
    format='[%(asctime)s] %(levelname)s | %(name)s => %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8',
    level=logging.INFO,
)

if __name__ == "__main__":
    
    env_file = Path().resolve() / '.env'
    load_dotenv(env_file)
    
    uvicorn.run(
        'core.asgi:application', 
        port=int(os.getenv('PORT')) or 5000, 
        log_config=config,
        access_log=True,
        host=os.getenv('HOST') or '127.0.0.1'
    )