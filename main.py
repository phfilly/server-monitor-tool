import server
import aws
import env
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def login():
    return render_template('index.html')


@app.route('/memory', methods=['POST', 'GET'])
def read():
    server_data = []
    if request.method == 'POST':
        server_data.append(server.connectBastion())
        return render_template('read.html', data=server_data)
    else:
        return render_template('index.html')


@app.route('/cpu')
def metrics():
    '''
        ADD SERVERS HERE FOR CPU STATS
    '''

    data = []
    data.append(aws.metrics('The Pitt', env.THEPITT_ID))
    data.append(aws.metrics('The Tower', env.THETOWER_ID))
    data.append(aws.metrics('The Portal', env.THEPORTAL_ID))
    data.append(aws.metrics('Reporting', env.REPORTING_ID))
    return render_template('aws.html', data=data)


if __name__ == '__main__':
    login()
