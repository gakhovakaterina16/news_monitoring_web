from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, SubmitField
from wtforms.validators import DataRequired

class dtcoorForm(FlaskForm):
    dt_start = DateTimeField("Дата и время начала мониторинга:", validators=[DataRequired()])
    dt_finish = DateTimeField("Дата и время завершения мониторинга:", validators=[DataRequired()])
    latitude = StringField("Широта:", validators=[DataRequired()])
    longitude = StringField("Долгота:", validators=[DataRequired()])
    submit = SubmitField("Отправить")