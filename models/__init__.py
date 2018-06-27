from models.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

class User(Model):
	__table__ = 'user'

	id = StringField(primary_key=True, column_type='varchar(50)')
	credit = IntegerField()
	lastdate = StringField(column_type='date')
	daynum = IntegerField()