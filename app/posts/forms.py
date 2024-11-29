from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

CATEGORIES = [("Tech", "Tech"), ("News", "News"), ("CRM", "CRM")]  # Категорії для вибору

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Active Post")  # Чекбокс для активності поста
    publish_date = DateTimeLocalField(
        "Publish Date", 
        format="%Y-%m-%dT%H:%M",
        default=dt.now(),  # Дата за замовчуванням
        validators=[DataRequired()],
    )
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField("Add Post")
