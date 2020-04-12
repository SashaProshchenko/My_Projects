from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('Id', show=False)
    article = Col('Article')
    url = Col('URL')
    release_date = Col('Release Date')
    publisher = Col('Publisher')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))