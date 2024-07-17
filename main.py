from dotenv import load_dotenv
load_dotenv()

import os
from src.main import app


if __name__ == '__main__':
    import uvicorn

    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    dev = int(os.getenv("DEV"))

    uvicorn.run(
        app="main:app",
        host=host,
        port=port,
    )
