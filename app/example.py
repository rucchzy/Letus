



#register
@app.route('/register',methods=['GET','POST'])
def register():
	if request.method=='POST':
		username = request.form.get('username')
		name=request.form.get('name')
		password = request.form.get('password')
		birthdate=request.form.get('birthdate')
		user=User(username,name,password,birthdate,datetime.now())
		check=User.query.filter_by(username=username).first()
		if check is None:
			db.session.add(user)
			db.session.commit()
			user_info=User.query.filter_by(username=username).all()
			return render_template('users.html',users=user_info)
		else:
			return render_template('register.html', message='Username existed!')
	else:
		return render_template('register.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		user=User.query.filter_by(username=username).first()
		if user is None:
			return render_template('login.html',message='No such username!')
		else:
			if user.username==username and user.password==password:
				session['username'] = username
				return render_template('welcome.html',username=username)
			else:
				return render_template('login.html',message='Wrong password!')
	else:
		return render_template('login.html')

@app.route('/json')
def jsonTest():
	d = {'result':'success'};
	u = User("liulichao", "llc", "12345", "1111", "1111")
	return json.dumps(class_to_dict(u));

def class_to_dict(obj):
	'''把对象(支持单个对象、list、set)转换成字典'''
	is_list = obj.__class__ == [].__class__
	is_set = obj.__class__ == set().__class__
	if is_list or is_set:
		obj_arr = []
		for o in obj:
		#把Object对象转换成Dict对象
			d = {}
			d.update(o.__dict__)
			obj_arr.append(d)
		return obj_arr
	else:
		d = {}
		d.update(obj.__dict__)
		return d
