from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///ml_articles.db', echo=True)
Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Article: {}>".format(self.name)


class Article_Info(Base):

    __tablename__ = "articles_info"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    release_date = Column(String)
    publisher = Column(String)
    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", backref=backref(
        "articles_info", order_by=id))


Base.metadata.create_all(engine)