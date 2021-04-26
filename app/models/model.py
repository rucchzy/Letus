#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-22 14:09:34
# @Author  : liulichao (liulichao@ruc.edu.cn)
# @Link    : http://www.liulichao.com
# @Version : $Id$

import sys
from flask_sqlalchemy import SQLAlchemy
from ..router import app

db = SQLAlchemy(app)





class CRUD():

	def add(self, resource):
		db.session.add(resource)
		return db.session.commit()   

	def update(self):
		return db.session.commit()

	def delete(self, resource):
		db.session.delete(resource)
		return db.session.commit()
