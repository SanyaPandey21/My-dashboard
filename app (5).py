from flask import Flask, jsonify, render_template, request
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="dashboard_db",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/api/insights', methods=['GET'])
def get_insights():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    filters = {
        'end_year': request.args.get('end_year'),
        'intensity': request.args.get('intensity'),
        'sector': request.args.get('sector'),
        'topic': request.args.get('topic'),
        'region': request.args.get('region'),
        'start_year': request.args.get('start_year'),
        'impact': request.args.get('impact'),
        'added': request.args.get('added'),
        'published': request.args.get('published'),
        'country': request.args.get('country'),
        'relevance': request.args.get('relevance'),
        'pestle': request.args.get('pestle'),
        'source': request.args.get('source'),
        'likelihood': request.args.get('likelihood')
    }
    
    query = 'SELECT * FROM insights WHERE TRUE'
    params = []
    
    for key, value in filters.items():
        if value:
            query += f' AND {key} = %s'
            params.append(value)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/api/filters', methods=['GET'])
def get_filters():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    queries = {
        'end_years': 'SELECT DISTINCT end_year FROM insights WHERE end_year IS NOT NULL ORDER BY end_year',
        'intensities': 'SELECT DISTINCT intensity FROM insights WHERE intensity IS NOT NULL ORDER BY intensity',
        'sectors': 'SELECT DISTINCT sector FROM insights WHERE sector IS NOT NULL ORDER BY sector',
        'topics': 'SELECT DISTINCT topic FROM insights WHERE topic IS NOT NULL ORDER BY topic',
        'regions': 'SELECT DISTINCT region FROM insights WHERE region IS NOT NULL ORDER BY region',
        'start_years': 'SELECT DISTINCT start_year FROM insights WHERE start_year IS NOT NULL ORDER BY start_year',
        'impacts': 'SELECT DISTINCT impact FROM insights WHERE impact IS NOT NULL ORDER BY impact',
        'added_dates': 'SELECT DISTINCT added FROM insights WHERE added IS NOT NULL ORDER BY added',
        'published_dates': 'SELECT DISTINCT published FROM insights WHERE published IS NOT NULL ORDER BY published',
        'countries': 'SELECT DISTINCT country FROM insights WHERE country IS NOT NULL ORDER BY country',
        'relevances': 'SELECT DISTINCT relevance FROM insights WHERE relevance IS NOT NULL ORDER BY relevance',
        'pestles': 'SELECT DISTINCT pestle FROM insights WHERE pestle IS NOT NULL ORDER BY pestle',
        'sources': 'SELECT DISTINCT source FROM insights WHERE source IS NOT NULL ORDER BY source',
        'likelihoods': 'SELECT DISTINCT likelihood FROM insights WHERE likelihood IS NOT NULL ORDER BY likelihood'
    }
    
    filters = {}
    
    for key, query in queries.items():
        cursor.execute(query)
        filters[key] = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    
    return jsonify(filters)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
