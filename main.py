import aws
import env
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/memory', methods=['POST', 'GET'])
def memory():
    '''
        ADD SERVERS HERE FOR MEMORY STATS
    '''
    data = []
    data.append(aws.memory('The Pitt', env.THEPITT_IMAGE_ID))
    data.append(aws.memory('The Tower', env.THETOWER_IMAGE_ID))
    data.append(aws.memory('The Portal', env.THEPORTAL_IMAGE_ID))

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
    app.run(debug=True, host='0.0.0.0', port=7000)
