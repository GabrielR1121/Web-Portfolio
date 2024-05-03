from website import create_app
from website.config.config import get_config

"""
This is the web portfolio of Gabriel E. Rodriguez Garcia
"""
app = create_app()


if __name__ == "__main__":
    app_config = get_config()
    app.run(host=app_config.HOST, port=app_config.PORT, debug=app_config.DEBUG)
