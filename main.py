from flask import Flask, session, redirect, url_for, escape, request, render_template
from wikitrends import WikiTrends

app = Flask(__name__)
hotword = ''
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['query'] = request.form['query']
        return redirect(url_for('search'))
    else:
        return render_template('index.html')

@app.route('/s', methods=['GET', 'POST'])
def search():
    wikientry = WikiTrends(session['query'], 10)
    if wikientry.validate_article():
        search_result = wikientry.get_hits('html')
        return render_template('results.html') + 'Search results from "%s" Wikipedia article:<br /><br />%s' % (escape(session['query']), search_result) + '</body>'
    return render_template('results.html') + 'No article "%s" found in Wikipedia' % (escape(session['query'])) + '</body>'

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(port=8080)
