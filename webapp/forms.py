from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField
from wtforms.validators import DataRequired

class dtForm(FlaskForm):
    dt_start = DateTimeField("Дата и время начала мониторинга:", validators=[DataRequired()])
    dt_finish = DateTimeField("Дата и время завершения мониторинга:", validators=[DataRequired()])
    submit = SubmitField("Отправить")