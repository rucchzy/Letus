
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from datetime import datetime
import json
from PIL import Image

app = Flask(__name__)

#定义sqlalchemy数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sdfzg11b@localhost:3306/testdb?charset=utf8'


from app.models.model import db
from app.models.user import User,Plan,Sportscategory,Lesson,Ltlist,Trainer,Stadium,Stlist,Attend,Uplist
from app.models.user import Uldiscuss,Friend,Question,Feedback,Exhibition,Discuss,Room,Match,Urlist,Utdiscuss


#test函数
@app.route('/test')
def test():
	result = []
	p = {}
	p['score']=999999999
	p['coin']=99999999
	p['job']='主席'
	result.append(p)
	return(json.dumps(result,ensure_ascii = False))


#胡赟豪范竞之成卓兰部分


#1.搜索运动类型
@app.route('/searchsportscategory' ,methods=['GET','POST'])
def searchsportscategory():
	if request.method == 'POST':
		sc_name = request.form.get('sports_category')
		sports_category = Sportscategory.query.filter_by(sc_name = sc_name).first()
		result = []
		p = {}
		p['sc_id']=sports_category.sc_id
		p['sc_name'] = sports_category.sc_name
		p['sc_description'] = sports_category.sc_description
		p['sc_pic']	= sports_category.sc_pic
		result.append(p)
		return(json.dumps(result,ensure_ascii = False))


#2四个脚标点击约课程，返回团体课课程大类及相应图片
@app.route('/appointlesson')
def appointlesson():
	appoint_lesson=Sportscategory.query.all()
	result=[]
	for sportscategory in appoint_lesson:
		p={}
		p['sc_id']=sportscategory.sc_id
		p['sc_name']=sportscategory.sc_name
		p['sc_description']=sportscategory.sc_description
		p['sc_pic']=sportscategory.sc_pic
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#3点击大类，将该类运动的全部课程返回
@app.route('/sportslesson/<int:sc_id>')
def sportslesson(sc_id):
	lesson_detail=Lesson.query.filter_by(sc_id=sc_id).all()
	sc_info=Sportscategory.query.filter_by(sc_id=sc_id).first()
	result=[]
	p={}
	p['sc_name']=sc_info.sc_name
	result.append(p)
	for lesson in lesson_detail:
		s_id=lesson.s_id
		stadium_info=Stadium.query.filter_by(s_id=s_id).first()
		p={}
		p['s_name']=stadium_info.s_name
		p['l_id']=lesson.l_id
		p['l_name']=lesson.l_name
		p['l_price']=lesson.l_price
		p['l_description']=lesson.l_description
		p['l_status']=lesson.l_status
		p['l_pic']=lesson.l_pic
		p['l_credit']=lesson.l_credit
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#4.对返回的课程进行搜索
@app.route('/searchlesson' ,methods = ['GET', 'POST'])
def searchlesson():
	if request.method == 'POST':
		keyword = request.form.get('l_name')
		result = []
		for i in range(0,len(result3)):
			if result3[i]['l_name'].find(keyword) != -1:
				p = {}
				p['l_id'] = result3[i]['l_id']
				p['l_name'] = result3[i]['l_name']
				p['l_price'] = result3[i]['l_price']
				p['l_description'] = result3[i]['l_description']
				p['l_status'] = result3[i]['l_status']
				p['l_pic'] = result3[i]['l_pic']
				p['l_credit'] = result3[i]['l_credit']
				result.append(p)
		return(json.dumps(result,ensure_ascii = False))


#5团体课界面点击课程，返回课程详细信息
@app.route('/lessondetail/<int:l_id>')
def lessondetail(l_id):
	lesson=Lesson.query.filter_by(l_id=l_id).first()
	sc_id=lesson.sc_id
	sc_info=Sportscategory.query.filter_by(sc_id=sc_id).first()
	s_id=lesson.s_id
	t_id=lesson.t_id
	s_info=Stadium.query.filter_by(s_id=s_id).first()
	t_info=Trainer.query.filter_by(t_id=t_id).first()
	result=[]
	p={}
	p['t_name']=t_info.t_name
	p['sc_name']=sc_info.sc_name
	p['l_id']=lesson.l_id
	p['l_name']=lesson.l_name
	p['s_name']=s_info.s_name
	p['s_address']=s_info.s_address
	p['s_contact']=s_info.s_contact
	p['l_price']=lesson.l_price
	p['l_description']=lesson.l_description
	p['l_pic']=lesson.l_pic
	p['l_credit']=lesson.l_credit
	result.append(p)
	discuss_info=Uldiscuss.query.filter_by(l_id=l_id).all()
	for discuss in discuss_info:
		p={}
		u_id=discuss.u_id
		user_info=User.query.filter_by(u_id=u_id).first()
		p['u_name']=user_info.u_name
		p['u_pic']=user_info.u_pic
		p['ul_content']=discuss.ul_content
		p['ul_credit']=discuss.ul_credit
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#6发表团体课评论
@app.route('/lessondiscuss',methods=['GET','POST'])
def lessondiscusss():
	if request.method=='POST':
		ul_content=request.form.get('ul_content')
		u_id=request.form.get('u_id')
		l_id=request.form.get('l_id')
		ul_credit=int(request.form.get('ul_credit'))*100
		lessondiscuss=Uldiscuss(ul_content,u_id,l_id,datetime.now(),ul_credit)
		db.session.add(lessondiscuss)
		db.session.commit()
		#计算新的评分值
		discuss_count=Uldiscuss.query.filter_by(l_id=l_id).count()
		lesson_info=Lesson.query.filter_by(l_id=l_id).first()
		credit=lesson_info.l_credit
		newcredit=((discuss_count-1)*credit+ul_credit)/discuss_count
		lesson_info.l_credit=newcredit
		db.session.commit()
		result=[]
		p={}
		p['status']='success'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))
#6备用代码
# @app.route('/lessondiscuss',methods='POST')
# def lessondiscuss():
# 	data=json.loads(request.form.get('data'))
# 	ul_content=data['ul_content']
# 	u_id=data['u_id']
# 	l_id=data['l_id']
# 	ul_credit=data['ul_credit']
# 	lessondiscuss=Uldiscuss(ul_content,u_id,l_id,datetime.now(),ul_credit)
# 	db.session.add(lessondiscuss)
# 	db.session.commit()


#7点击私教，返回私教个人信息及图片
@app.route('/appointtrainer')
def appointtrainer():
	appoint_trainer=Trainer.query.all()
	result=[]
	for trainer in appoint_trainer:
		p={}
		t_id=trainer.t_id
		p['t_id']=trainer.t_id
		p['t_pic']=trainer.t_pic
		p['t_name']=trainer.t_name
		p['t_sex']=trainer.t_sex
		p['t_year']=trainer.t_year		
		p['t_rank']=trainer.t_rank
		stadium = Stlist.query.filter_by(t_id = t_id).first()
		s_id = stadium.s_id
		stadiumname=Stadium.query.filter_by(s_id = s_id).first()
		p['s_name']=stadiumname.s_name
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#8.对返回的教练进行搜索
@app.route('/searchtrainer' ,methods = ['GET','POET'])
def searchtrainer():
	if request.method=='POST':
		t_name = request.form.get('t_name')
		result = []
		for i in range(0, len(result7)):
			if result7[i]['t_name'] == t_name:
				p = {}
				p['t_id'] = result7[i]['t_id']
				p['t_name'] = result7[i]['t_name']
				p['t_sex'] = result7[i]['t_sex']
				p['t_year'] = result7[i]['t_year']
				p['t_pic'] = result7[i]['t_pic']
				p['t_rank'] = result7[i]['t_rank']
				p['s_name'] = result7[i]['s_name']
				result.append(p)
		return(json.dumps(result,ensure_ascii = False))


#9私教界面点击教练返回教练详细信息
@app.route('/trainerdetail/<int:t_id>')
def trainerdetail(t_id):
	trainer=Trainer.query.filter_by(t_id=t_id).first()
	st_info=Stlist.query.filter_by(t_id=t_id).first()
	s_id=st_info.s_id
	stadium_info=Stadium.query.filter_by(s_id=s_id).first()
	result=[]
	p={}
	p['t_id']=trainer.t_id
	p['t_name']=trainer.t_name
	p['t_sex']=trainer.t_sex
	p['t_year']=trainer.t_year
	p['t_pic']=trainer.t_pic
	p['t_rank']=trainer.t_rank
	p['t_credit']=trainer.t_credit
	p['t_sportstype']=trainer.t_sportstype
	p['t_intro']=trainer.t_intro
	p['s_name']=stadium_info.s_name
	p['s_address']=stadium_info.s_address
	p['s_contact']=stadium_info.s_contact
	result.append(p)
	discuss_info=Utdiscuss.query.filter_by(t_id=t_id).all()
	for discuss in discuss_info:
		p={}
		u_id=discuss.u_id
		user_info=User.query.filter_by(u_id=u_id).first()
		p['u_name']=user_info.u_name
		p['u_pic']=user_info.u_pic
		p['ut_content']=discuss.ut_content
		p['ut_credit']=discuss.ut_credit
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#10发表对私教评论
@app.route('/trainerdiscuss',methods=['GET','POST'])
def trainerdiscusss():
	if request.method=='POST':
		ut_content=request.form.get('ut_content')
		u_id=request.form.get('u_id')
		t_id=request.form.get('t_id')
		ut_credit=int(request.form.get('ut_credit'))*100
		trainerdiscuss=Utdiscuss(ut_content,u_id,t_id,datetime.now(),ut_credit)
		db.session.add(trainerdiscuss)
		db.session.commit()
		#计算新的评分值
		discuss_count=Utdiscuss.query.filter_by(t_id=t_id).count()
		trainer_info=Trainer.query.filter_by(t_id=t_id).first()
		print(discuss_count)
		print('\n')
		credit=trainer_info.t_credit
		newcredit=((discuss_count-1)*credit+ut_credit)/discuss_count
		trainer_info.t_credit=newcredit
		db.session.commit()
		result=[]
		p={}
		p['status']='success'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))


#11点击社区中的问答，进入问答界面，返回问题及回答摘要
@app.route('/qanda')
def qanda():
	q_a=Question.query.all()
	global result11
	result11=[]
	for questionanswer in q_a:
		p={}
		p['q_id']=questionanswer.q_id
		p['q_content']=questionanswer.q_content
		p['q_samenum']=questionanswer.q_samenum
		p['q_readnum']=questionanswer.q_readnum
		p['q_feedbacknum']=questionanswer.q_feedbacknum
		feedback_info=Feedback.query.filter_by(q_id=questionanswer.q_id).first()
		if feedback_info is None:
			p['f_id']=None
			p['f_content']=None
		else:
			flength=len(feedback_info.f_content)
			p['f_id']=feedback_info.f_id
			if flength>90:
				p['f_content']=feedback_info.f_content[:90]
			else:
				p['f_content']=feedback_info.f_content
		result11.append(p)
	return(json.dumps(result11,ensure_ascii=False))


#12.搜索问答
@app.route('/searchqanda' ,methods = ['GET','POET'])
def searchqanda():
	if request.method=='POST':
		keyword = request.form.get('q_content')
		result = []
		for i in range(0, len(result11)):
			if result11[i]['q_content'].find(keyword) != -1:
				p = {}
				p['q_id'] = result11[i]['q_id']
				p['q_content'] = result11[i]['q_content']
				p['q_starttime'] = result11[i]['q_starttime']
				p['q_samenum'] = result11[i]['q_samenum']
				p['q_readnum'] = result11[i]['q_readnum']
				p['q_feedbacknum'] = result11[i]['q_feedbacknum']
				p['f_content'] = result11[i]['f_content']
				result.append(p)
		return(json.dumps(result,ensure_ascii = False))


#13点击某个问题，返回问题详情及所有回答摘要
@app.route('/questiondetail/<int:q_id>')
def questiondetail(q_id):
	question=Question.query.filter_by(q_id=q_id).first()
	newreadnum=question.q_readnum+1
	question.q_readnum=newreadnum
	db.session.commit()
	result=[]
	p={}
	p['q_content']=question.q_content
	p['q_detail']=question.q_detail
	p['q_starttime']=question.q_starttime.strftime("%Y-%m-%d %H:%M:%S")[0:10]
	p['q_samenum']=question.q_samenum
	p['q_readnum']=question.q_readnum
	p['q_feedbacknum']=question.q_feedbacknum
	result.append(p)
	feedback_info=Feedback.query.filter_by(q_id=q_id).all()
	for feedback in feedback_info:
		u_id=feedback.u_id
		user_info=User.query.filter_by(u_id=u_id).first()
		u_name=user_info.u_name
		u_pic=user_info.u_pic
		p={}
		p['u_id']=feedback.u_id
		p['u_name']=user_info.u_name
		p['u_pic']=user_info.u_pic
		p['f_id']=feedback.f_id
		flength=len(feedback.f_content)
		if flength>130:
			p['f_content']=feedback.f_content[:130]
		else:
			p['f_content']=feedback.f_content
		p['f_time']=feedback.f_time.strftime("%Y-%m-%d %H:%M:%S")[0:10]
		p['f_likenum']=feedback.f_likenum
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#14.同12

#问题界面点击同问
@app.route('/samequestion/<int:q_id>')
def samequestion(q_id):
	q_info=Question.query.filter_by(q_id=q_id).first()
	newnum=q_info.q_samenum+1
	q_info.q_samenum=newnum
	db.session.commit()
	result=[]
	p={}
	p['status']='success'
	result.append(p)
	return(json.dumps(result,ensure_ascii=False))

#15查看某条回答具体内容
@app.route('/feedbackdetail/<int:f_id>')
def feedbackdetail(f_id):
	feedback_detail=Feedback.query.filter_by(f_id=f_id).first()
	#查找对应用户表、问题表
	q_id=feedback_detail.q_id
	u_id=feedback_detail.u_id
	question_info=Question.query.filter_by(q_id=q_id).first()
	user_info=User.query.filter_by(u_id=u_id).first()
	#产生json数据
	result=[]
	p={}
	p['f_id']=f_id
	p['f_content']=feedback_detail.f_content
	p['f_likenum']=feedback_detail.f_likenum
	p['f_time']=feedback_detail.f_time.strftime("%Y-%m-%d %H:%M:%S")[0:10]
	p['u_pic']=user_info.u_pic
	p['u_name']=user_info.u_name
	p['q_content']=question_info.q_content
	result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#16对回答界面点赞
@app.route('/feedbacklike/<int:f_id>')
def feedbacklike(f_id):
	feedback_info=Feedback.query.filter_by(f_id=f_id).first()
	likenum=feedback_info.f_likenum
	newlikenum=likenum+1
	feedback_info.f_likenum=newlikenum
	db.session.commit()
	result=[]
	p={}
	p['status']='success'
	p['f_likenum']=newlikenum
	result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#17对问题添加回答
@app.route('/addfeedback',methods=['GET','POST'])
def addfeedback():
	if request.method=='POST':
		#获取回答的参数
		q_id=request.form.get('q_id')
		u_id=request.form.get('u_id')
		f_content=request.form.get('f_content')
		feedback=Feedback(q_id,u_id,f_content,0,datetime.now())
		#对问题表的回答数进行修改
		question_info=Question.query.filter_by(q_id=q_id).first()
		feedbacknum=question_info.q_feedbacknum
		newfeedbacknum=feedbacknum+1
		question_info.q_feedbacknum=newfeedbacknum
		db.session.add(feedback)
		db.session.commit()
		result=[]
		p={}
		p['status']='success'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))


#18添加问题
@app.route('/addquestion',methods=['GET','POST'])
def addquestion():
	if request.method=='POST':
		u_id=request.form.get('u_id')
		q_content=request.form.get('q_content')
		q_detail=request.form.get('q_detail')
		question=Question(u_id,datetime.now(),0,q_content,q_detail,0,0)
		db.session.add(question)	
		db.session.commit()
		result=[]
		p={}
		p['status']='success'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))



#常子翼张森学部分

#regiter1检查用户名是否存在
@app.route('/reg1check/<username>')
def reg1check(username):
	user_info=User.query.filter_by(u_name=username).first()
	result = []
	p={}
	if user_info is None:
		p['status']='success'
	else:
		p['status']='fail'
	result.append(p)
	return(json.dumps(result,ensure_ascii=False))


#注册写入数据库
@app.route('/register', methods = ['GET','POST'])
def register():
	if request.method == 'POST':		
		u_name = request.form.get('username')
		u_pwd = request.form.get('password')
		u_truename = request.form.get('name')
		u_sex = request.form.get('gender')
		u_idcard = request.form.get('identity')
		u_birthdate = request.form.get('birthdate')	
		u_job = request.form.get('job')
		u_position = request.form.get('position')
		u_question = request.form.get('pwd_question')
		u_answer = request.form.get('pwd_answer')
		user = User(u_name, u_pwd, 100, 0, '', u_truename, u_sex, u_idcard, u_birthdate, u_job, u_position, datetime.now(), u_question, u_answer, 0)
		result = []	
		p = {}
		p['status'] = 'success'
		result.append(p)
		db.session.add(user)
		db.session.commit()
		return(json.dumps(result,ensure_ascii=False))

#登录函数
@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		u_name = request.form.get('username')
		users = User.query.filter_by(u_name = u_name).first()
		result = []
		if users is None:
			p = {}
			p['status'] = 'fail_user_nonexist'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))
		else:
			u_pwd = request.form.get('password')
			if users.u_name == u_name and users.u_pwd == u_pwd:
				p = {}
				p['u_name'] = u_name
				p['u_id'] = users.u_id
				p['status'] = 'success'
				result.append(p)
				return(json.dumps(result,ensure_ascii=False))
			else:
				p = {}
				p['status'] = 'fail_password'
				result.append(p)
				return(json.dumps(result,ensure_ascii=False))


@app.route('/get_question/<int:u_id>', methods = ['GET','POST'])#点击修改密码，显示密保问题
def get_question(u_id):
	if request.method == 'POST':
		users = User.query.filter_by(u_name = u_name).first()
		u_id = users.u_id
		u_question = users.u_question
		result = []
		p = {}
		if users is None:			
			p['status'] = 'fail_user_nonexist'
			return(json.dumps(result,ensure_ascii=False))
		else:
			p['u_question'] = u_question
			p['status'] = 'success'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))

@app.route('/compare/<int:u_id>', methods = ['GET','POST'])#获取用户填写的答案，并判断是否正确
def compare(u_id):
	if request.method == 'POST':
		users = User.query.filter_by(u_id = u_id).first()
		u_answer = users.u_answer
		u_answer_get = request.form.get('u_answer')
		result = []
		p = {}
		if u_answer == u_answer_get:
			p['status'] = 'success'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))
		else:
			p['status'] = 'fail_answer'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))

@app.route('/change_pwd/<int:u_id>', methods = ['GET','POST'])#获取用户新输入的密码，并修改数据库
def change_pwd(u_id):
	u_new_pwd = request.form.get('u_new_pwd')
	result = []
	p = {}
	users.u_pwd=u_new_pwd
	db.session.commit()
	p['status'] = 'success'
	result.append(p)
	return(json.dumps(result,ensure_ascii=False))

@app.route('/create_plan/<int:u_id>', methods = ['GET','POST'])#创建计划
def create_plan(u_id):
	if request.method == 'POST':
		sc_id = request.form.get('sc_id')
		p_name = request.form.get('p_name')
		p_description = request.form.get('p_description')
		p_starttime = request.form.get('p_starttime')
		p_endtime = request.form.get('p_endtime')
		p_maxnum = request.form.get('p_maxnum')
		p_type = request.form.get('p_type')
		p_nownum = 1
		plan = Plan(sc_id, p_name, p_description, p_starttime, p_endtime, p_maxnum, p_nownum, p_type, datetime.now())
		uplist = Uplist(p_id, u_id, 1, datetime.now(), 0)
		plans = Plan.query.filter_by(p_name = p_name).first()
		result = []
		if plans is None:
			p = {}
			p['status'] = 'success'
			result.append(p)
			db.session.add(plan)
			db.session.add(uplist)
			db.session.commit()
			return(json.dumps(result,ensure_ascii=False))
		else:
			p = {}
			p['status'] = 'fail_plan_exist'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))

@app.route('/search_plan', methods = ['GET','POST'])#查询计划（暂时支持按计划名称查找）
def search_plan():
	if request.method == 'POST':
		p_name = request.form.get('p_name')
		plans = Plan.query.filter_by(p_name = p_name).all()
		result = []
		if plans is None:
			p = {}
			p['status'] = 'fail_plan_nonexist'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))
		else:
			for plan in plans:
				p={}
				p['p_name'] = plan.p_name
				p['p_description'] = plan.p_description
				p['p_starttime'] = plan.p_starttime
				p['p_endtime'] = plan.p_endtime
				p['p_maxnum'] = plan.p_maxnum
				p['p_nownum'] = plan.p_nownum
				p['p_createtime'] = plan.p_createtime
				p['status'] = 'success'
				result.append(p)
				return(json.dumps(result,ensure_ascii=False))

@app.route('/join_plan/<int:u_id>/<int:p_id>', methods = ['GET','POST'])#参加计划
def join_plan(u_id,p_id):
	if request.method == 'POST':
		plans = Plan.query.filter_by(p_id = p_id).first()
		users = User.query.filter_by(u_id = u_id).first()
		uplist = Uplist(p_id, u_id, 0, datetime.now(), 0)
		p_maxnum = plans.p_maxnum
		p_nownum = plans.p_nownum
		result = []
		if p_nownum == p_maxnum:
			p = {}
			p['status'] = 'fail_plan_maxnum'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))
		else:
			p_nownum = p_nownum + 1
			plans.p_nownum=p_nownum
			db.session.add(uplist)
			db.session.commit()
			p = {}
			p['status'] = 'success'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))

@app.route('/quit_plan/<int:u_id>/<int:p_id>', methods = ['GET','POST'])#退出计划
def quit_plan(u_id,p_id):
	if request.method == 'POST':
		plans = Plan.query.filter_by(p_id = p_id).first()
		uplists = Uplist.query.filter_by(p_id = p_id, u_id = u_id).first()
		p_maxnum = plans.p_maxnum
		p_nownum = plans.p_nownum
		result = []
		if p_nownum == 0:
			db.session.delete(plans)
			db.session.delete(uplists)
			db.session.commit()
		else:
			p_nownum = p_nownum - 1
			plans.p_nownum=p_nownum
			db.session.delete(uplists)
			db.session.commit()
		p = {}
		p['status'] = 'success'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/in_plan/<int:p_id>', methods = ['GET', 'POST'])#查看谁在运动计划中
def in_plan(p_id):
	if request.method == 'POST':
		uplists = Uplist.query.filter_by(p_id = p_id).all()
		result = []
		for uplist in uplists:
			u_id = uplist.u_id
			user = User.query.filter_by(u_id).first()
			p = {}
			p['u_name'] = user.u_name
			p['status'] = 'success'
			result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/view_plan/<int:p_id>', methods = ['GET', 'POST'])#查看计划详细信息
def view_plan(p_id):
	if request.method == 'POST':
		plan = Plan.query.filter_by(p_id = p_id).first()
		result = []
		p = {}
		p['p_name'] = plan.p_name
		p['p_description'] = plan.p_description
		p['p_starttime'] = plan.p_starttime
		p['p_endtime'] = plan.p_endtime
		p['p_maxnum'] = plan.p_maxnum
		p['p_nownum'] = plan.p_nownum
		p['p_createtime'] = plan.p_createtime
		p['status'] = 'success'
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))



UPLOAD_FOLDER=r'D:/大三上/Python/LETUS/flask/app/static/user_image'  #上传图片
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif'])  
  
def allowed_file(filename):  
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS  
 
@app.route('/upload_file/<int:u_id>',methods = ['GET','POST'])  
def upload_file(u_id):
	if request.method == 'POST':
		users = User.query.filter_by(u_id = u_id).all()
		u_name = users.u_name
		file = request.files['file']
		result = []
		if file and allowed_file(file.filename):
			picname = u_name + '_' + file.filename
			file.save(os.path.join(UPLOAD_FOLDER,picname))#实际存储的路径为：UPLOAD_FOLDER\u_name_file.filename
			u_pic = '../../image/user_image/'+picname#数据库中记录为：../../image/user_image/u_name_file.filename
			users.u_pic=u_pic
			db.session.commit()
			p = {}
			p['status'] = 'success'
			result.append(p)
			return(json.dumps(result,ensure_ascii=False))
		p = {}
		p['status'] = 'fail_file'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/me/<int:u_id>', methods = ['GET','POST'])#显示我的信息
def me(u_id):
	if request.method == 'POST':
		users = User.query.filter_by(u_id = u_id).first()
		u_name = users.u_name
		u_credit = users.u_credit
		u_coin = users.u_coin
		u_pic = users.u_pic
		u_job = users.u_job
		u_position = users.u_position
		result = []
		p = {}
		p['u_name'] = u_name
		p['u_credit'] = u_credit
		p['u_coin'] = u_coin
		p['u_pic'] = u_pic
		p['u_job'] = u_job
		p['u_position'] = u_position
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/friend/<int:u_id>', methods = ['GET','POST'])#显示我的好友
def friend(u_id):
	if request.method == 'POST':
		friends = Friend.query.filter_by(u_id = u_id).all()
		result = []
		for friend in friends:
			u_id2 = friends.u_id2
			users = User.query.filter_by(u_id = u_id2).first()
			p = {}
			p['u_name'] = users.u_name
			p['u_pic'] = users.u_pic
			p['f_time'] = friend.f_time
			result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/my_plan/<int:u_id>', methods = ['GET','POST'])#显示我的健身计划
def my_plan(u_id):
	if request.method == 'POST':
		uplists = Uplist.query.filter_by(u_id = u_id).all()
		result = []
		for uplist in uplists:
			p_id = uplist.p_id
			plan = Plan.query.filter_by(p_id = p_id).first()
			p = {}
			p['p_id'] = p_id
			p['p_name'] = plan.p_name
			p['p_description'] = plan.p_description
			p['p_starttime'] = plan.p_starttime
			p['p_endtime'] = plan.p_endtime
			p['p_maxnum'] = plan.p_maxnum
			p['p_nownum'] = plan.p_nownum
			p['p_createtime'] = plan.p_createtime
			p['status'] = 'success'
			result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/make_friends/<int:u_id>/<int:u_id2>', methods = ['GET', 'POST'])#添加好友
def make_friends(u_id,u_id2):
	if request.method == 'POST':
		u_id = u_id
		u_id2 = u_id2
		friend1 = Friend(u_id,u_id2,datetime.now())
		friend2 = Friend(u_id2,u_id,datetime.now())
		db.session.add(friend1)
		db.session.add(friend2)
		db.session.commit()
		result = []
		p = {}
		p['status'] = 'success'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/delete_friendship/<int:u_id>/<int:u_id2>', methods = ['GET', 'POST'])#s删除好友
def delete_friendship(u_id,u_id2):
	if request.method == 'POST':
		friend1 = Friend.query.filter_by(u_id = u_id, u_id2 = u_id2).first()
		friend2 = Friend.query.filter_by(u_id = u_id2, u_id2 = u_id).first()
		db.session.delete(friend1)
		db.session.delete(friend2)
		db.session.commit()
		result = []
		p = {}
		p['status'] = 'success'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))

@app.route('/is_friend/<int:u_id>/<int:u_id2>', methods = ['GET', 'POST'])#判断两人是否为好友
def is_friend(u_id,u_id2):
	if request.method == 'POST':
		friend = Friend.query.filter_by(u_id = u_id, u_id2 = u_id2).first()
		result = []
		p = {}
		if friend is None:
			p['status'] = 'not_friend'
		else:
			p['status'] = 'is_friend'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))




#戴尚方罗景旸部分


def find_roomthing(r_id):
	useroom = Room.query.filter_by(r_id=r_id).first()
	return useroom

def find_scthing_id(sc_id):
	usesc = Sportscategory.query.filter_by(sc_id=sc_id).first()
	return usesc

def find_scthing_name(sc_name):
	usesc = Sportscategory.query.filter_by(sc_name=sc_name).first()
	return usesc

def find_userthing(u_id):
	useuser = User.query.filter_by(u_id=u_id).first()
	return useuser

def find_urlistthing(ur_id):
	useurlist = Urlist.query.filter_by(ur_id=ur_id).first()
	return useurlist

#开始弹出用户评分
@app.route('/tempsearch/<int:u_id>')
def tempsearch(u_id):
	urlist_list = Urlist.query.filter_by(u_id=u_id).all()
	
	userlist = []
	for urlist in urlist_list:
		r_id = urlist.r_id
		urtables = Urlist.query.filter_by(r_id=r_id).all()
		for urtable in urtables:
			if urtable.u_id != u_id:
				sc_id = find_roomthing(r_id).sc_id
				sc_name = find_scthing_id(sc_id).sc_name
				r_starttime = find_roomthing(r_id).r_starttime
				p = {}
				p['u_id']=urtable.u_id 
				p['sc_id']=sc_id
				p['r_starttime']=r_starttime
				userlist.append(p)
		urlist.update({'ur_gradestatus':1})
		db.session.commit()
	return(json.dumps(userlist,ensure_ascii=False))

@app.route('/gocredit/<int:u_id>',methods=['GET','POST'])
def gocredit(u_id):
	if request.method=='POST':
		usertable = find_userthing(u_id)
		u_credit = usertable.u_credit
		u_gradetime = usertable.u_gradetime
		u_creditlist = request.form.get('u_creditlist')
		u_thistime = request.form.get('u_thistime') + u_gradetime
		allcredits = u_credit*u_gradetime
		for credits in u_creditlist:
			allcredits = allcredits + credits
		u_credit = allcredits/allcredits
		usertable.update({'u_credit':u_credit})
			usertable.update({'u_gradetime':u_thistime})
		db.session.commit()
		result = []
		p = {}
		p['status'] = 'success'
		result.append(p)
	return(json.dumps(result,ensure_ascii=False))
		

@app.route('/tempmatch/<int:u_id>'):
def tempmatch(u_id):
	matchtable = Match.query.filter_by(u_id=u_id).first()
	matchlist = []
	u_position = matchtable.u_position
	if matchtable.sc_id==null:
		sc_id = 1
	else:
		sc_id = matchtable.sc_id
	sc_name = find_scthing_id(sc_id).sc_name
	if matchtable.r_minnum==null:
		r_minnum = 2
	else:
		r_minnum = matchtable.r_minnum
	if matchtable.r_maxnum==null:
		r_maxnum = 10
	else:
		r_maxnum = matchtable.r_maxnum
	r_starttime = matchtable.r_starttime
	r_endtime = matchtable.r_endtime
	p = {}
	p['sc_name']=sc_name
	p['u_position']=u_position
	p['r_minnum']=r_minnum
	p['r_maxnum']=r_maxnum
	p['r_starttime']=r_starttime
	p['r_endtime']=r_endtime
	matchlist.append(p)
	return(json.dumps(matchlist,ensure_ascii=False))

#匹配信息的设置
@app.route('/matchinfo/<int:u_id>',methods=['GET','POST'])
def matchinfo(u_id):
	if request.method=='POST':
		usematch = Match.query.filter_by(u_id=u_id).first()
		#房间查询

		#房间信息修改
		sc_name = request.form.get('sc_name')
		sc_id = find_scthing_name(sc_name).sc_id
		u_position = request.form.get('u_position')#前端操作一下
		r_maxnum = request.form.get('r_maxnum')
		r_minnum = request.form.get('r_minnum')
		r_starttime = request.form.get('r_starttime')
		r_endtime = request.form.get('r_endtime')
		usematch.update({'sc_id':sc_id})
		usematch.update({'u_position':u_position})
		usematch.update({'r_maxnum':r_maxnum})
		usematch.update({'r_minnum':r_minnum})
		usematch.update({'r_starttime':r_starttime})
		usematch.update({'r_endtime':r_endtime})
		db.session.commit()
		result = []
		p = {}
		p['status'] = 'success'
		result.append(p)
		return (json.dumps(result,ensure_ascii=False))


#匹配界面点击创建房间，此时再次调用tempmatch，或是直接调用matchinfo中的信息，前端自己把握
@app.route('/roomcreate/<int:u_id>',methods=['GET','POST'])
def roomcreate(u_id):
	if request.method=='POST':
		#获得房间创建信息
		#获得历史信息又如何呢？
		r_status = 0
		sc_id = request.form.get('sc_id')
		r_maxnum = request.form.get('r_maxnum')
		r_minnum = request.form.get('r_minnum')
		r_starttime = request.form.get('r_starttime')
		r_endtime = request.form.get('r_endtime')
		r_position = request.form.get('r_position')
		r_description = request.form.get('r_description')
		r_private = request.form.get('r_private')
		r_fonder = u_id
		theroom = Room(r_status, r_maxnum, r_minnum, r_starttime, r_endtime, r_position, r_description, r_private, r_fonder)
		db.session.add(theroom)
		db.session.commit()
		#同步创建人在房间中的详情列表
		#ur_id = str(r_id)+'_'+str(u_id)
		r_id = Room.query.filter_by((r_fonder=u_id)&&(r_starttime=r_starttime)).first().r_id
		u_id = u_id
		ur_owner = True
		ur_entertime = datetime.now()
		ur_status = 0
		ur_gradestatus = False
		urlist = Urlist(r_id, u_id, ur_owner, ur_entertime, ur_status, ur_gradestatus)
		db.session.add(urlist)
		db.session.commit()
		result = []
		p = {}
		p['status'] = 'success'
		result.append(p)
		return (json.dumps(result,ensure_ascii=False))

#房间的显示信息问题
@app.route('/scroom/<int:r_id>')
def scroom(r_id):
	result = []
	useroom = find_roomthing(r_id)
	#useuser = find_userthing(u_id)
	r_position = useroom.r_position
	sc_id = useroom.sc_id
	sc_name = find_scthing_id(sc_id).sc_name
	r_starttime = useroom.r_starttime
	r_endtime = useroom.r_endtime
	r_description = useroom.r_description
	r_private = useroom.r_private
	r_fonder = useroom.r_fonder
	useurlist = Urlist.query.filter_by(r_id=r_id).all()
	alluser = {}
	for useur in useurlist:
		thisu_id = useur.u_id
		usethisu = find_userthing(thisu_id)
		thisu_name = usethisu.u_name
		thisu_pic = usethisu.u_pic
		thisu_credit = usethisu.u_credit
		userinfolist = [thisu_name,thisu_pwd,thisu_credit]
		alluser['thisu_id'] = userinfolist
	p = {}
	p['r_position'] = r_position
	p['sc_name'] = sc_name
	p['r_starttime'] = r_starttime
	p['r_endtime'] = r_endtime
	p['r_description'] = r_description
	p['r_private'] = r_private
	p['alluser'] = alluser
	result.append(p)
	return (json.dumps(result,ensure_ascii=False))


#邀请好友加入房间，浏览好友列表
@app.route('/roomfriends/<int:u_id>')
def roomfriends(u_id):
	result = []
	friendtable_list = Friend.query.filter_by(u_id=u_id).all()
	for friendtable in friendtable_list:
		fr_id = friendtable.u_id2
		fusertable = find_userthing(u_id2)
		fr_name = fusertable.u_name
		fr_pic = fusertable.u_pic
		p = {}
		p['fr_name'] = fr_name
		p['fr_pic'] = fr_pic
		result.append(p)
	return (json.dumps(result,ensure_ascii=False))

#用户加入房间
def enterrooms(u_id,r_id):
	u_id = u_id
	r_id = r_id
	ur_owner = False
	ur_entertime = datetime.now()
	ur_status = 0
	#user_info = User.query.filter_by(u_id=u_id).first()
	#ur_credit = user_info.u_credit
	#ur_gradefrequency = request.form.get('ur_gradefrequency')
	ur_gradestatus = False
	urlist = Urlist(r_id, u_id, ur_owner, ur_entertime, ur_readystatus, ur_gradestatus)
	db.session.add(urlist)
	db.session.commit()

def positionmatch(u_position,r_position):
	posrank = 0
	if abs(u_position - r_position) < 1:
		posrank = 1
		if abs(u_position - r_position) < 0.5:
			posrank = 2
			if abs(u_position - r_position) < 0.25:
				posrank = 3
	return posrank

def timematch(u_starttime,u_endtime,r_starttime,r_endtime):
	timerank = 0
	if abs(u_starttime - r_starttime) < 2:
		timerank = 1
		if abs(u_starttime - r_starttime) < 1:
			timerank = 2
	if abs(u_endtime- r_endtime) < 2:
		timerank = timerank + 0.5
		if abs(u_endtime- r_endtime) < 1:
			timerank = timerank + 0.5
	return timerank

def nummatch(u_maxnum,u_minnum,r_maxnum,r_minnum):
	numrank = 0
	if abs(u_minnum - r_minnum) < 3:
		numrank = 1
		if abs(u_minnum - r_minnum) < 1:
			numrank = 2
	if abs(u_maxnum- r_maxnum) < 5:
		numrank = numrank + 0.5
		if abs(u_maxnum- r_maxnum) < 3:
			numrank = numrank + 0.5
	return numrank



#用户随机匹配
@app.route('/randamjoin/<int:u_id>')
def randomjoin(u_id):
	match_info = Match.query.filter_by(u_id=u_id).first()
	sc_id = match_info.sc_id
	u_position = match_info.u_position
	u_maxnum = match_info.r_maxnum 
	u_minnum = match_info.r_minnum
	u_starttime = match_info.r_starttime 
	u_endtime = match_info.r_endtime
	#以上同创建房间初始时的操作
	all_rooms = Room.query.filter_by(r_status=0).all()
	findroom_id = -1
	allroom_dict = {}
	getrank = 0
	findit = False
	#开始随机匹配流程
	#这段代码力图兼顾其实用性和敏捷性
	for theroom in all_rooms:
		rsc_id = theroom.sc_id
		r_position = theroom.r_position
		r_starttime = theroom.r_starttime
		r_endtime = theroom.r_endtime
		r_maxnum = theroom.r_maxnum
		r_minnum = theroom.r_minnum
		if sc_id==theroom.sc_id:
			theroomrank = 0
			theroomrank = theroomrank + positionmatch(u_position,r_position)
			theroomrank = theroomrank + timematch(u_starttime,u_endtime,r_starttime,r_endtime)
			theroomrank = theroomrank + nummatch(u_maxnum,u_minnum,r_maxnum,r_minnum)
		if theroomrank >= 7:
			findroom_id = theroom.r_id
			findit = True
			break
		if theroomrank > 3:
			allroom_dict[str(theroom.r_id)] = theroomrank
	if !(findit):
		for key in allroom_dict.keys():
			if allroom_dict[key] > getrank:
				findroom_id = key
				getrank = allroom_dict[key]
	
	#创建新的urlist
	r_id = findroom_id
	u_id = u_id
	ur_owner = True
	ur_entertime = datetime.now()
	ur_status = 0
	ur_gradestatus = False
	urlist = Urlist(r_id, u_id, ur_owner, ur_entertime, ur_status, ur_gradestatus)
	db.session.add(urlist)
	db.session.commit()
	
	result = []
	p = {}
	p['r_id'] = findroom_id
	result.append(p)
	return (json.dumps(result,ensure_ascii=False))

#房间内聊天，这一部分不需要数据库操作

#用户退出房间，以及这个函数的调用？
@app.route('/exitroom/<int:ur_id>')
def exitroom(ur_id):
	urlist_info = find_urlistthing(ur_id)
	ur_status = urlist_info.ur_status
	urlist_info.update({'ur_status':-1})
	db.session.commit()
	result = []
	p = {}
	p['status'] = 'success'
	return (json.dumps(result,ensure_ascii=False))


#这个函数要在哪里调用呢？
def start_game(r_id):
	room_info = find_roomthing(r_id)
	urlist_info = Urlist.query.filter_by(r_id=r_id).all()
	r_maxnum = room_info.r_maxnum
	r_minnum = room_info.r_minnum
	oknum = 0
	usernum = len(urlist_info)
	for us_info in urlist_info:
		if us_info.ur_status==1:
			oknum = oknum + 1
	if usernum>r_minnum:
		if oknum==usernum:
			return True
		elif ((oknum>r_minnum) && (usernum==r_maxnum)):
			return True
	return False

#活动进行界面
@app.route('/gaming/<int:r_id>')
def gaming():
	if start_game(r_id):
		#还是用原来的房间界面吧？


UPLOAD_FOLDER_ENC=r'D:\大三上\Python\LETUS\flask\app\static\exhibition_content'  #上传话
UPLOAD_FOLDER_ENI=r'D:\大三上\Python\LETUS\flask\app\static\exhibition_image'  #上传图片
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif'])  
  
def allowed_file(filename):  
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#用户分享
@app.route('/sharing/<int:u_id>',methods = ['GET','POST'])
def sharing(u_id):
	if request.method == 'POST':
		e_time = datetime.now()
		file = request.files['file']
		picture = request.pictures['picture'] #????
		result = []
		if file and allowed_file(file.filename):
			cnotentname = u_id + '的' + file.filename
			file.save(os.path.join(UPLOAD_FOLDER_ENC,cnotentname))
			e_content = os.path.join(UPLOAD_FOLDER_ENC,cnotentname)
			if picture and allowed_file(picture.filename):
				picname = u_id + '的' + file.filename
				file.save(os.path.join(UPLOAD_FOLDER_ENI,picname))
				e_pic = os.path.join(UPLOAD_FOLDER_ENI,picname)
				e_likenum = 0
				exhibition = Exhibition(e_time,e_content,e_pic,u_id,e_likenum)
				db.session.add(exhibition)
				db.session.commit()
				p = {}
				p['status'] = 'success'
				result.append(p)
				return(json.dumps(result,ensure_ascii=False))
		p = {}
		p['status'] = 'fail_file'
		result.append(p)
		return(json.dumps(result,ensure_ascii=False))


#用户朋友圈
@app.route('/friendzone/<int:u_id>')
def friendzone(u_id):
	result = []
	friendtable_list = Friend.query.filter_by(u_id=u_id).all()
	friendidlist = []
	for friendtable in friendtable_list:
		useu_id = friendtable.u_id2
		useexhibition = Exhibition.query.filter_by(u_id=useu_id).first()
		#讨论决定这块显示不考虑时间远近，一切从简
		useuser = find_userthing(useu_id)
		useu_name = useuser.u_name
		useu_pic = useuser.u_pic
		usee_time = useexhibition.e_time
		usee_content = useexhibition.e_content
		usee_pic = useexhibition.e_pic
		usee_likenum = useexhibition.e_likenum
		p = {}
		p['u_name'] = useu_name
		p['u_pic'] = useu_pic
		p['e_time'] = usee_time
		p['e_content'] = usee_content
		p['e_pic'] = usee_pic
		p['e_likenum'] = usee_likenum
		result.append(p)
	return (json.dumps(result,ensure_ascii=False))