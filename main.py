from website import create_app
from website.config.config import get_config
import os

"""
This is the web portfolio of Gabriel E. Rodriguez Garcia
"""
app = create_app()


if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app_config = get_config()
    app.run(host=app_config.HOST, port=app_config.PORT, debug=app_config.DEBUG)
