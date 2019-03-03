import psycopg2


class dbtools:
    def __init__(self, dbname, user, password):
        self.dbname = dbname
        self.user = user
        self.password = password
        try:
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(host="localhost", database=dbname, user=user, password=password)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_all_rows(self, vars, table):
        try:
            cur = self.conn.cursor()

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

    def custom_query(self, statement):
        try:
            cur = self.conn.cursor()
            cur.execute(statement)
            row = cur.fetchall()

            cur.close()
            return row
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_metric(self, matches_team_ids, metric, in_autonomous):
        try:
            cur = self.conn.cursor()
            data = []
            for i in matches_team_ids:
                if in_autonomous == '':
                    statement = 'SELECT "game_piece_type" FROM cycles WHERE matches_team_id = ' + str(i) + \
                                ' AND "game_piece_type" = ' + metric + ' AND "failed" = false'
                else:
                    statement = 'SELECT "game_piece_type", "to" FROM cycles WHERE matches_team_id = ' + str(i) + \
                                ' AND "game_piece_type" = ' + metric + ' AND "failed" = false and "in_autonomous" = ' + in_autonomous
                cur.execute(statement)
                rows = cur.fetchall()
                data.append(len(rows))

            cur.close()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_status(self, matches_team_ids, what):
        try:
            cur = self.conn.cursor()
            data = []
            for i in matches_team_ids:
                if what == 'endgame':
                    statement = 'SELECT "endgame_status" FROM matches_teams WHERE id = ' + str(i)
                    cur.execute(statement)
                    rows = cur.fetchall()
                    if rows != []:
                        data.append(rows[0][0])
                if what == 'auto':
                    statement = 'SELECT "starting_position" FROM matches_teams WHERE id = ' + \
                                str(i) + ' AND "cross_hab_line" = true'
                    cur.execute(statement)
                    rows = cur.fetchall()
                    if rows != []:
                        data.append(rows[0][0])
            cur.close()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_competition_id(self, competition_name):
        try:
            cur = self.conn.cursor()
            statement = 'SELECT id FROM competitions where name = ' + competition_name
            cur.execute(statement)
            row = cur.fetchall()

            cur.close()
            return row[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_team_id(self, team_key):
        number = team_key[3:]
        try:
            cur = self.conn.cursor()
            statement = 'SELECT id FROM teams where number = ' + str(number)
            cur.execute(statement)
            row = cur.fetchall()

            cur.close()
            return row[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_matches_team_id(self, team_id, competition_id, match_cutoff):
        try:
            cur = self.conn.cursor()
            statement = 'SELECT matches_teams.id FROM matches_teams ' \
                        'INNER JOIN matches ON(matches_teams.match_id = matches.id) ' \
                        'INNER JOIN competitions ON(matches.competition_id = competitions.id) ' \
                        'WHERE matches_teams.team_id = ' + str(team_id) + ' AND competitions.id = ' \
                        + str(competition_id) + ' AND matches.number <= ' + str(match_cutoff)
            cur.execute(statement)
            row = cur.fetchall()

            cur.close()
            ids = []
            for i in row:
                ids.append(i[0])
            return ids
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)