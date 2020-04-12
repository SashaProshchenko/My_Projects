from app import app
from db_setup import init_db, db_session
from forms import ArticleSearchForm, ArticleForm
from flask import flash, render_template, request, redirect
from models import Article_Info, Article
from tables import Results

init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    search = ArticleSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Article Name':
            qry = db_session.query(Article_Info, Article).filter(
                Article.id == Article_Info.article_id).filter(
                    Article.name.contains(search_string))
            results = [item[0] for item in qry.all()]

        elif search.data['select'] == 'Release Year':
            qry = db_session.query(Article_Info).filter(
                Article_Info.release_date.contains(search_string))
            results = qry.all()

        elif search.data['select'] == 'Publisher':
            qry = db_session.query(Article_Info).filter(
                Article_Info.publisher.contains(search_string))
            results = qry.all()

        else:
            qry = db_session.query(Article_Info)
            results = qry.all()

    else:
        qry = db_session.query(Article_Info)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/new_article', methods=['GET', 'POST'])
def new_article():

    form = ArticleForm(request.form)

    if request.method == 'POST' and form.validate():
        article_info = Article_Info()
        save_changes(article_info, form, new=True)
        flash('Article added successfully!')
        return redirect('/')

    return render_template('new_article.html', form=form)


def save_changes(article_info, form, new=False):

    article = Article()
    article.name = form.article.data

    article_info.article = article
    article_info.url = form.url.data
    article_info.release_date = form.release_date.data
    article_info.publisher = form.publisher.data

    if new:
        db_session.add(article_info)
    db_session.commit()


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):

    qry = db_session.query(Article_Info).filter(
        Article_Info.id == id)
    article_info = qry.first()

    if article_info:
        form = ArticleForm(formdata=request.form, obj=article_info)
        if request.method == 'POST' and form.validate():
            save_changes(article_info, form)
            flash('Article information updated successfully!')
            return redirect('/')
        return render_template('edit_article.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

    qry = db_session.query(Article_Info).filter(
        Article_Info.id == id)
    article_info = qry.first()

    if article_info:
        form = ArticleForm(formdata=request.form, obj=article_info)
        if request.method == 'POST' and form.validate():
            db_session.delete(article_info)
            db_session.commit()
            flash('Article deleted successfully!')
            return redirect('/')
        return render_template('delete_article.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)


if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001)