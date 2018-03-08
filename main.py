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
    data.append(aws.memory('The Pitt', env.THEPITT_IMAGE_ID, 'c4.4xlarge'))
    data.append(aws.memory('The Tower', env.THETOWER_IMAGE_ID, 't2.large'))
    data.append(aws.memory('The Portal', env.THEPORTAL_IMAGE_ID, 't2.large'))
    data.append(aws.memory('Jade', env.JADE_IMAGE_ID, 'm4.xlarge', env.JADE_IP))
    data.append(aws.memory('Kitana', env.KITANA_IMAGE_ID, 'm4.xlarge', env.KITANA_IP))
    data.append(aws.memory('Sindel', env.SINDEL_IMAGE_ID, 'm4.xlarge', env.SINDEL_IP))

    return render_template('aws.html', data=data, pagename='/memory')


@app.route('/cpu')
def cpu():
    '''
        ADD SERVERS HERE FOR CPU STATS
    '''

    data = []
    data.append(aws.cpu('The Pitt', env.THEPITT_ID, 'c4.4xlarge'))
    data.append(aws.cpu('The Tower', env.THETOWER_ID, 't2.large'))
    data.append(aws.cpu('The Portal', env.THEPORTAL_ID, 't2.large'))
    data.append(aws.cpu('Reporting', env.REPORTING_ID, 'm5.large'))
    data.append(aws.cpu('Kitana(OrientDB)', env.KITANA_ID, 'm4.xlarge', env.KITANA_IP))
    data.append(aws.cpu('Jade(OrientDB)', env.JADE_ID, 'm4.xlarge', env.JADE_IP))
    data.append(aws.cpu('Sindel(OrientDB)', env.SINDEL_ID, 'm4.xlarge', env.SINDEL_IP))
    data.append(aws.databaseMemory('MySQL', env.MYSQLDB, 'db.m3.xlarge'))
    data.append(aws.redshift('Redshift', env.REDSHIFT, 'dc2.large'))
    return render_template('aws.html', data=data, pagename='/cpu')


@app.route('/datapipeline')
def pipeline():
    '''
        VIEW DATAPIPELINE FROM AWS
    '''
    data = aws.dataPipeline()
    return render_template('logs.html',
                           data=data,
                           tablename='Pipeline Logs',
                           pagename='/datapipeline')


@app.route('/scrape-server/<server>')
def server(server):
    '''
        VIEW TIME DATA OF A SCRAPE SERVER
    '''
    data = aws.read_logs(server)
    return render_template('scrapers.html',
                           data=data,
                           server=server,
                           tablename='Docker Logs',
                           pagename='/scrape-server/{}'.format(server))


@app.route('/scraper-graph/<scraper>')
def scraper_graph(scraper):
    '''
        VIEW TIME DATA OF A SCRAPER
    '''
    data = aws.retrieve_scraper_data(scraper)
    return render_template('scraper-graph.html',
                           data=data,
                           tablename='Docker Scraper Perfomance',
                           pagename='/scraper-graph/{}'.format(scraper))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
