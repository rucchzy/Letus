
from .model import db
from datetime import datetime
from ..router import app

class User(db.Model):        #用户表
	# 表的名字:
	__tablename__ = 'user'

	# 表的结构:
	u_id = db.Column(db.Integer,primary_key=True)
	u_name = db.Column(db.String(55))
	u_pwd = db.Column(db.String(55))
	u_credit = db.Column(db.Integer)
	u_coin = db.Column(db.Integer)
	u_pic = db.Column(db.String(1000))
	u_truename = db.Column(db.String(55))
	u_sex = db.Column(db.String(20))
	u_idcard = db.Column(db.String(55))
	u_birthdate = db.Column(db.DateTime(),default = (datetime.now()))
	u_job = db.Column(db.String(100))
	u_position = db.Column(db.String(1000))
	u_creationtime = db.Column(db.DateTime(),default = (datetime.now()))
	u_question = db.Column(db.String(1000))
	u_answer = db.Column(db.String(1000))
	u_gradetime = db.Column(db.Integer,default = 0)


	def __init__(self,u_name,u_pwd,u_credit,u_coin,u_pic,u_truename,u_sex,u_idcard,u_birthdate,u_job,u_position,u_creationtime,u_question,u_answer,u_gradetime):
		self.u_name = u_name
		self.u_pwd = u_pwd
		self.u_credit = u_credit
		self.u_coin = u_coin
		self.u_pic = u_pic
		self.u_truename = u_truename
		self.u_sex = u_sex
		self.u_idcard = u_idcard
		self.u_birthdate = u_birthdate
		self.u_job = u_job
		self.u_position = u_position
		self.u_creationtime = u_creationtime
		self.u_question = u_question
		self.u_answer = u_answer
		self.u_gradetime = u_gradetime
		#如果数据库表不存在，创建这张表
		db.create_all()

class Plan(db.Model):       #计划
	__tablename__ = 'plan'
	p_id=db.Column(db.Integer,primary_key=True)
	sc_id=db.Column(db.Integer)
	p_name=db.Column(db.String(55))
	p_description=db.Column(db.String(1000))
	p_starttime=db.Column(db.DateTime(),default=(datetime.now()))
	p_endtime=db.Column(db.DateTime(),default=(datetime.now()))
	p_maxnum=db.Column(db.Integer)
	p_nownum=db.Column(db.Integer)
	p_type=db.Column(db.Integer)
	p_createtime=db.Column(db.DateTime(),default=(datetime.now()))


	def __init__(self,sc_id,p_name,p_description,p_starttime,p_endtime,p_maxnum,p_nownum,p_type,p_createtime):
		self.sc_id=sc_id
		self.p_name=p_name
		self.p_description=p_description
		self.p_starttime=p_starttime
		self.p_endtime=p_endtime
		self.p_maxnum=p_maxnum
		self.p_nownum = p_nownum
		self.p_type=p_type
		self.p_createtime=p_createtime

		db.create_all()

class Sportscategory(db.Model):  #运动种类
	__tablename__='sportscategory'
	sc_id=db.Column(db.Integer,primary_key=True)
	sc_name=db.Column(db.String(55))
	sc_description=db.Column(db.String(1000))
	sc_pic=db.Column(db.String(1000))

	def __init__(self,sc_name,sc_description,sc_pic):
		
		self.sc_name=sc_name
		self.sc_description=sc_description
		self.sc_pic=sc_pic

		db.create_all()

class Lesson(db.Model):   #课程
	__tablename__='lesson'
	l_id=db.Column(db.Integer,primary_key=True)
	l_name=db.Column(db.String(55))
	s_id=db.Column(db.Integer)
	t_id=db.Column(db.Integer)
	l_price=db.Column(db.Integer)
	l_description=db.Column(db.String(1000))
	l_status=db.Column(db.String(1000))
	l_pic=db.Column(db.String(1000))
	l_credit=db.Column(db.Integer)
	sc_id=db.Column(db.Integer)

	def __init__(self,l_name,s_id,t_id,l_price,l_description,l_status,l_pic,l_credit,sc_id):
		
		self.l_name=l_name
		self.s_id=s_id
		self.t_id=t_id
		self.l_price=l_price
		self.l_description=l_description
		self.l_status=l_status
		self.l_pic=l_pic
		self.l_credit=l_credit
		self.sc_id=sc_id
		db.create_all()

class Ltlist(db.Model):   #课程教练表
	__tablename__='ltlist'
	lt_id=db.Column(db.Integer,primary_key=True)
	l_id=db.Column(db.Integer)
	t_id=db.Column(db.Integer)
	
	def __init__(self,l_id,t_id):
		self.l_id=l_id
		self.t_id=t_id
		db.create_all()

class Trainer(db.Model):    #教练
	__tablename__='trainer'
	t_id=db.Column(db.Integer,primary_key=True)
	t_name=db.Column(db.String(55))
	t_sex=db.Column(db.String(10))
	t_year=db.Column(db.Integer)
	t_pic=db.Column(db.String(1000))
	t_rank=db.Column(db.String(55))
	t_intro=db.Column(db.String(1000))
	t_credit=db.Column(db.Integer)
	t_sportstype=db.Column(db.String(255))

	def __init__(self,t_name,t_sex,t_year,t_pic,t_rank,t_intro,t_credit,t_sportstype):
		self.t_name=t_name
		self.t_sex=t_sex
		self.t_year=t_year
		self.t_pic=t_pic
		self.t_rank=t_rank
		self.t_intro=t_intro
		self.t_credit=t_credit
		self.t_sportstype=t_sportstype
		db.create_all()

class Stadium(db.Model):   #运动场馆
	__tablename__='stadium'
	s_id=db.Column(db.Integer,primary_key=True)
	s_name=db.Column(db.String(55))
	s_address=db.Column(db.String(1000))
	s_contact=db.Column(db.String(1000))

	def __init__(self,s_name,s_address,s_contact):
		self.s_name=s_name
		self.s_address=s_address
		self.s_contact=s_contact
		db.create_all()

class Stlist(db.Model):   #教练场馆对应表
	__tablename__='stlist'
	st_id=db.Column(db.Integer,primary_key=True)
	t_id=db.Column(db.Integer)
	s_id=db.Column(db.Integer)

	def __init__(self,t_id,s_id):
		self.t_id=t_id
		self.s_id=s_id
		db.create_all()

class Attend(db.Model):   #用户运动打卡计划表
	__tablename__='attend'
	a_id=db.Column(db.Integer,primary_key=True)
	a_time=db.Column(db.DateTime(),default=(datetime.now()))
	up_id=db.Column(db.Integer)

	def __init__(self,a_time,up_id):
		self.a_time=a_time
		self.up_id=up_id
		db.create_all()

class Uplist(db.Model):  #用户运动计划表
	__tablename__='uplist'
	up_id=db.Column(db.Integer, primary_key=True)
	p_id = db.Column(db.Integer)
	u_id = db.Column(db.Integer)
	up_owner=db.Column(db.Integer)
	up_entertime=db.Column(db.DateTime(),default=(datetime.now()))
	u_attendnum=db.Column(db.Integer)

	def __init__(self, p_id, u_id, up_id, up_owner, up_entertime, u_attendnum):
		self.p_id = p_id
		self.u_id = u_id
		self.up_owner=up_owner
		self.up_entertime=up_entertime
		self.u_attendnum=u_attendnum
		db.create_all()

class Uldiscuss(db.Model):   #用户评论表
	__tablename__='uldiscuss'
	ul_id=db.Column(db.Integer,primary_key=True)
	ul_content=db.Column(db.String(1000))
	u_id=db.Column(db.Integer)
	l_id=db.Column(db.Integer)
	ul_time=db.Column(db.DateTime,default=(datetime.now()))
	ul_credit=db.Column(db.Integer)

	def __init__(self,ul_content,u_id,l_id,ul_time,ul_credit):
		self.ul_content=ul_content
		self.u_id=u_id
		self.l_id=l_id
		self.ul_time=ul_time
		self.ul_credit=ul_credit

		db.create_all()

class Utdiscuss(db.Model):   #用户评论表
	__tablename__='utdiscuss'
	ut_id=db.Column(db.Integer,primary_key=True)
	ut_content=db.Column(db.String(1000))
	u_id=db.Column(db.Integer)
	t_id=db.Column(db.Integer)
	ut_time=db.Column(db.DateTime,default=(datetime.now()))
	ut_credit=db.Column(db.Integer)

	def __init__(self,ut_content,u_id,t_id,ut_time,ut_credit):
		self.ut_content=ut_content
		self.u_id=u_id
		self.t_id=t_id
		self.ut_time=ut_time
		self.ut_credit=ut_credit

		db.create_all()

class Friend(db.Model):   #用户好友表
	__tablename__='friend'
	f_id=db.Column(db.Integer,primary_key=True)
	u_id=db.Column(db.Integer)
	u_id2=db.Column(db.Integer)
	f_time=db.Column(db.DateTime,default=(datetime.now()))

	def __init__(self,u_id,u_id2,f_time):
		self.u_id=u_id
		self.u_id2=u_id2
		self.f_time=f_time

		db.create_all()

class Question(db.Model):  #用户问答表
	__tablename__='question'
	q_id=db.Column(db.Integer,primary_key=True)
	u_id=db.Column(db.Integer)
	q_starttime=db.Column(db.DateTime,default=(datetime.now()))
	q_samenum=db.Column(db.Integer)
	q_content=db.Column(db.String(1000))
	q_detail=db.Column(db.String(1000))
	q_readnum=db.Column(db.Integer)
	q_feedbacknum=db.Column(db.Integer)

	def __init__(self,u_id,q_starttime,q_samenum,q_content,q_detail,q_readnum,q_feedbacknum):
		self.u_id=u_id
		self.q_starttime=q_starttime
		self.q_samenum=q_samenum
		self.q_content=q_content
		self.q_detail=q_detail
		self.q_readnum=q_readnum
		self.q_feedbacknum=q_feedbacknum

		db.create_all()

class Feedback(db.Model):  #用户回答表
	__tablename__='feedback'
	f_id=db.Column(db.Integer,primary_key=True)
	q_id=db.Column(db.Integer)
	u_id=db.Column(db.Integer)
	f_content=db.Column(db.String(3000))
	f_likenum=db.Column(db.Integer)
	f_time=db.Column(db.DateTime(),default=(datetime.now()))

	def __init__(self,q_id,u_id,f_content,f_likenum,f_time):
		self.q_id=q_id
		self.u_id=u_id
		self.f_content=f_content
		self.f_likenum=f_likenum
		self.f_time=f_time

		db.create_all()

class Exhibition(db.Model):  #分享列表
	e_id=db.Column(db.Integer,primary_key=True)
	e_time=db.Column(db.DateTime,default=(datetime.now()))
	e_content=db.Column(db.String(1000))
	u_id=db.Column(db.Integer)
	e_likenum=db.Column(db.Integer)
	e_discussnum=db.Column(db.Integer)
	e_readnum=db.Column(db.Integer)
	e_pic=db.Column(db.String(1000))

	def __init__(self,e_time,e_content,u_id,e_likenum,e_discussnum,e_readnum,e_pic):
		self.e_time=e_time
		self.e_content=e_content
		self.u_id=u_id
		self.e_likenum=e_likenum
		self.e_discussnum=e_discussnum
		self.e_readnum=e_readnum
		self.e_pic=e_pic

		db.create_all()

class Discuss(db.Model):  #分享评论表
	__tablename__='discuss'
	d_id=db.Column(db.Integer,primary_key=True)
	d_content=db.Column(db.String(1000))
	e_id=db.Column(db.Integer)
	u_id=db.Column(db.Integer)
	d_time=db.Column(db.DateTime,default=(datetime.now()))

	def __init__(self,d_content,e_id,u_id,d_time):
		self.d_content=d_content
		self.e_id=e_id
		self.u_id=u_id
		self.d_time=d_time

		db.create_all()

class Room(db.Model):   #房间
	__tablename__='room'
	r_id=db.Column(db.Integer,primary_key=True)
	u_id=db.Column(db.Integer)
	r_status=db.Column(db.Integer)
	sc_id=db.Column(db.Integer)
	r_maxnum=db.Column(db.Integer)
	r_minnum=db.Column(db.Integer)
	r_starttime=db.Column(db.DateTime,default=(datetime.now()))
	r_endtime=db.Column(db.DateTime,default=(datetime.now()))
	r_position=db.Column(db.Integer)
	r_description=db.Column(db.String(1000))
	r_private=db.Column(db.Boolean)

	def __init__(self,u_id,r_status,sc_id,r_maxnum,r_minnum,r_starttime,r_endtime,r_position,r_description,r_private):
		self.u_id=u_id
		self.r_status=r_status
		self.sc_id=sc_id
		self.r_maxnum=r_maxnum
		self.r_minnum=r_minnum
		self.r_starttime=r_starttime
		self.r_endtime=r_endtime
		self.r_position=r_position
		self.r_description=r_description
		self.r_private=r_private

		db.create_all()

class Match(db.Model):
	__tablename__='match'
	m_id=db.Column(db.Integer,primary_key=True)
	u_id=db.Column(db.Integer)
	u_position=db.Column(db.String(1000))
	r_maxnum=db.Column(db.Integer)
	r_minnum=db.Column(db.Integer)
	r_starttime=db.Column(db.DateTime,default=(datetime.now()))
	r_endtime=db.Column(db.DateTime,default=(datetime.now()))
	sc_id=db.Column(db.Integer)

	def __init__(self,u_id,u_position,r_maxnum,r_minnum,r_starttime,r_endtime,sc_id):
		self.u_id=u_id
		self.u_position=u_position
		self.r_maxnum=r_maxnum
		self.r_minnum=r_minnum
		self.r_starttime=r_starttime
		self.r_endtime=r_endtime
		self.sc_id=sc_id

		db.create_all()

class Urlist(db.Model):
	__tablename__='urlist'
	ur_id=db.Column(db.Integer,primary_key=True)
	r_id=db.Column(db.Integer)
	u_id=db.Column(db.Integer)
	ur_owner=db.Column(db.Boolean)
	ur_entertime=db.Column(db.DateTime,default=(datetime.now()))
	ur_status=db.Column(db.Integer)
	ur_gradestatus=db.Column(db.Boolean)

	def __init__(self,r_id,u_id,ur_owner,ur_entertime,ur_status,ur_credit,ur_gradefrequency,ur_gradestatus):
		self.r_id=r_id
		self.u_id=u_id
		self.ur_owner=ur_owner
		self.ur_entertime=ur_entertime
		self.ur_status=ur_status
		self.ur_gradestatus=ur_gradestatus

		db.create_all()

