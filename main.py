import server
import aws
import env
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def login():
    return render_template('index.html')


@app.route('/memory', methods=['POST', 'GET'])
def memory():
    '''
        ADD SERVERS HERE FOR MEMORY STATS
    '''
    data = []
    data.append(aws.memory('The Pitt', env.THEPITT_IMAGE_ID))

    return render_template('aws.html', data=data)


@app.route('/cpu')
def cpu():
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
