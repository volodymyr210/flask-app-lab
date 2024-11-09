from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Is Active")
    publish_date = DateField("Publication Date", format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField("Category", choices=[
        ('technology', 'Technology'),
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField("Add Post")
