
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
	name = StringField('真实姓名', validators=[Length(0, 64)])
	location = StringField('位置', validators=[Length(0, 64)])
	about_me = TextAreaField('自我介绍')
	submit = SubmitField('保存')

class EditProfileAdminForm(FlaskForm):
	email = StringField('邮箱地址', validators=[DataRequired(), Length(1, 64), Email()])
	username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名由字母,数字,下划线,或.组成')])
	confirmed = BooleanField('确认')
	role = SelectField('角色', coerce=int)
	name = StringField('真是姓名', validators=[Length(0, 64)])
	location = StringField('住址', validators=[Length(0, 64)])
	about_me = TextAreaField('自我介绍')
	submit = SubmitField('保存')


	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已经被注册')

	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已经被注册')

class PostForm(FlaskForm):
	body = PageDownField('你要写的文章?', validators=[DataRequired()])
	submit = SubmitField('提交')

#定义评论表单
class CommentForm(FlaskForm):
	body = StringField('添加评论', validators=[DataRequired()])
	submit = SubmitField('提交')