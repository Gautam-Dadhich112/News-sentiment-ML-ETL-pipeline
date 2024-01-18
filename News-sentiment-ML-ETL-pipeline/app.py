from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from news_api import news_fetch


app = Flask(__name__)

news_fetch()

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = 'sentiment_analysis'

mysql = MySQL(app)

def get_data(date, sentiment):
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT url FROM sentiments WHERE Date = '{date}' and Analysis = '{sentiment}' '''.format(date = date, sentiment = sentiment))
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/')
def get_info():
    return render_template('index.html')


@app.route('/getting_data', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        date = request.args.get('date')
        sentiments = request.args.get('sentiments')
        url = get_data(date, sentiments)
        return url

if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)