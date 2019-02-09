import psycopg2


def connect():
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="2018Scouting", user="frc900", password="frc900")

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getRows(conn, vars, table):
    try:
        cur = conn.cursor()

        statement = "SELECT "
        for var in vars:
            statement = statement + str(var) + ", "
        statement = statement[:-2] + " FROM " + str(table)

        cur.execute(statement)
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchall()

        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def query(conn, statement):
    try:
        cur = conn.cursor()
        cur.execute(statement)
        row = cur.fetchall()

        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getMetric (conn, matches_team_ids, metric):
    try:
        cur = conn.cursor()
        data = []
        for i in matches_team_ids:
            statement = 'SELECT "to" FROM cycles WHERE matches_team_id = ' + str(i) + \
                        ' AND "to" = ' + metric + ' AND "failed" = false'
            cur.execute(statement)
            rows = cur.fetchall()
            data.append(len(rows))

        cur.close()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getCompetitionId(conn, competition_name):
    try:
        cur = conn.cursor()
        statement = 'SELECT id FROM competitions where name = ' + competition_name
        cur.execute(statement)
        row = cur.fetchall()

        cur.close()
        return row[0][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def getTeamId(conn, number):
    try:
        cur = conn.cursor()
        statement = 'SELECT id FROM teams where number = ' + str(number)
        cur.execute(statement)
        row = cur.fetchall()

        cur.close()
        return row[0][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def getMatchesTeamId(conn, team_id, competition_id):
    try:
        cur = conn.cursor()
        statement = 'SELECT matches_teams.id FROM matches_teams ' \
                    'INNER JOIN matches ON(matches_teams.match_id = matches.id) ' \
                    'INNER JOIN competitions ON(matches.competition_id = competitions.id) ' \
                    'WHERE matches_teams.team_id = ' + str(team_id) + ' AND competitions.id = ' + competition_id
        cur.execute(statement)
        row = cur.fetchall()

        cur.close()
        ids = []
        for i in row:
            ids.append(i[0])
        return ids
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)