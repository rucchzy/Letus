#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-22 01:23:13
# @Author  : liulichao (liulichao@ruc.edu.cn)
# @Link    : http://www.liulichao.com
# @Version : $Id$

import os
from app.router import app

app.secret_key = os.urandom(24)
app.run(host = '0.0.0.0', port = 8000, debug = True)

#在服务器启动后声明静态路由
url_for('static', filename='style.css')