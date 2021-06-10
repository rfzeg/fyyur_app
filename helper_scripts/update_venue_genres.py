#!/usr/bin/python

import psycopg2
import pickle

def update_venue(venue_id, genres):
    """ update venue genres based on the venue id """

    sql = """ UPDATE "Venue"
                SET genres = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        # Connect to an existing database
        conn = psycopg2.connect('dbname=fyyur_app_db')
        """
        conn = pg.connect(user="my_user",
              password="my_password",
              host="127.0.0.1",
              port="5432",
              dbname="misc_stats")
        """
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (genres, venue_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


if __name__ == '__main__':

    venue1={
        "id": 1,
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        }
    venue2={
        "id": 2,
        "genres": ["Classical", "R&B", "Hip-Hop"],
        }
    venue3={
        "id": 3,
        "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        }

    venues_to_update = [venue1,venue2,venue3]

    for venue in venues_to_update:
      venue_id = venue["id"]
      genres = venue["genres"]
      result = update_venue(venue_id, genres)
      print("Updated rows: %s"%(result))
