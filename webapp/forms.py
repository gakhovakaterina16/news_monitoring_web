from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, SubmitField
from wtforms.validators import DataRequired


class dtcoorForm(FlaskForm):
    dt_start = DateTimeField("Дата и время начала мониторинга:",
                             validators=[DataRequired(message=None)])
    dt_finish = DateTimeField("Дата и время завершения мониторинга:",
                              validators=[DataRequired(message=None)])
    latitude = StringField("Широта:",
                           validators=[DataRequired(message=None)])
    longitude = StringField("Долгота:",
                            validators=[DataRequired(message=None)])
    submit = SubmitField("Отправить")
