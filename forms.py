from wtforms import Form, StringField, SelectField

class ArticleSearchForm(Form):
    choices = [('Article name', 'Article Name'),
               ('Release Year', 'Release Year'),
               ('Publisher', 'Publisher')]
    select = SelectField('Search article:', choices=choices)
    search = StringField('')


class ArticleForm(Form):

    article = StringField('Article name')
    url = StringField('URL')
    release_date = StringField('Release Year')
    publisher = StringField('Publisher')
