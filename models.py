from app import db

class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return "{}".format(self.name)

class Article_Info(db.Model):

    __tablename__ = "articles_info"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    release_date = db.Column(db.String)
    publisher = db.Column(db.String)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    article = db.relationship("Article", backref=db.backref(
        "articles_info", order_by=id), lazy=True)
