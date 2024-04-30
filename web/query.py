from google.cloud import bigquery
from flask import escape, jsonify

def query_bigquery(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'query' in request_json:
        query = request_json['query']
    elif request_args and 'query' in request_args:
        query = request_args['query']
    else:
        return 'Please provide a BigQuery SQL query in the request.', 400

    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()

    rows = [dict(row.items()) for row in results]
    return jsonify(rows)