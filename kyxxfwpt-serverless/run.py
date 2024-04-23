import sys
from base import app
import uvicorn

if __name__ == '__main__':
    # uvicorn.run("base:app", host=sys.argv[1], port=sys.argv[2])
    uvicorn.run("base:app")
    