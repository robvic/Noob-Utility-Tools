from google.cloud import bigquery

request = {
    "player":"pena de galinha"
}

def query_table(player_name):
    project_id = 'noob-utility-tools'
    dataset = 'tibiantisinfo'
    table = 'logins'
    table_id = f'{project_id}.{dataset}.{table}'

    sa_path = './configs/noob-utility-tools-1c2633471287.json'
    client = bigquery.Client().from_service_account_json(sa_path)

    query = f"""
    SELECT searched, result, SUM(score) AS score
    FROM(
    SELECT t1.name AS searched, t2.name AS result, 1 AS score
    FROM `tibiantisinfo.logins` AS t1
    LEFT JOIN `tibiantisinfo.logins` AS t2
    ON t1.login=t2.logout
    WHERE t1.name = "{player_name}" -- Nome do Player
    UNION ALL
    SELECT t1.name AS searched, t2.name AS result, 1 AS score
    FROM `tibiantisinfo.logins` AS t1
    LEFT JOIN `tibiantisinfo.logins` AS t2
    ON t1.logout=t2.login
    WHERE t1.name = "{player_name}" -- Nome do Player
    )
    GROUP BY searched, result
    ORDER BY score DESC
    LIMIT 1;
    """

    results = client.query(query)
    for row in results:
        if row is not None:
            result = f"Identificado como {row.result} com score de confiança de {row.score}."
            return result
        else:
            return "Nenhum resultado encontrado."

def main(request):
    player_name = request['player']
    return query_table(player_name)

main(request)