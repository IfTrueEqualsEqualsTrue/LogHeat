import logging

from com_utils import start_emulation
from web_app import app


if __name__ == '__main__':
    start_emulation()
    app.run(debug=False)
