from website import create_app
from website.config import config

"""
This is the web portfolio of Gabriel E. Rodriguez Garcia
"""
app = create_app()


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
