#!/usr/bin/python

import psycopg2

def update_artist(artist_id, genres):
    """ update artist genres based on the artist id """

    sql = """ UPDATE "Artist"
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
        cur.execute(sql, (genres, artist_id))
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

    artist4={
      "id": 4,
      "genres": ["Rock n Roll"],
    }
    artist5={
      "id": 5,
      "genres": ["Jazz"],
    }
    artist6={
      "id": 6,
      "genres": ["Jazz", "Classical"],
    }

    artists_to_update = [artist5,artist6]

    for artist in artists_to_update:
      artist_id = artist["id"]
      genres = artist["genres"]
      result = update_artist(artist_id, genres)
      print("Updated rows: %s"%(result))

