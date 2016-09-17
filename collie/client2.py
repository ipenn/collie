# -*- coding: utf-8 -*-
# Created by wushuyi on 2016/9/9 0009.
from flask import Flask

app = Flask(__name__, static_url_path='')

app.config.update({
    'SEND_FILE_MAX_AGE_DEFAULT': 0
})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
