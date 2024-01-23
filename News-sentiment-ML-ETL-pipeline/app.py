from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from news_api import news_fetch


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = 'sentiment_analysis'

mysql = MySQL(app)

def get_data(date, sentiment):
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT url FROM sentiments WHERE Date = '{date}' and Analysis = '{sentiment}' '''.format(date = date, sentiment = sentiment))
    results = cursor.fetchall()
    return results


@app.route('/', methods=["GET", "POST"])
def get_info():
    if(request.method == "GET"):
        return render_template('index.html')
    topic = request.form.get('topic')
    news_fetch(topic)
    date = request.form.get('date')
    sentiments = request.form.get('sentiments')
    urls = get_data(date, sentiments)
    return render_template('second.html', urls = urls)

if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)