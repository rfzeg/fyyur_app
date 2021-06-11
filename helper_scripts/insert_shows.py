import psycopg2
from psycopg2.extensions import AsIs

show1={
    "id": 1,
    "parent_venue_id": 1,
    # "venue_name": "The Musical Hop",
    "parent_artist_id": 4,
    # "artist_name": "Guns N Petals",
    # "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }
show2={
    "id": 2,
    "parent_venue_id": 3,
    # "venue_name": "Park Square Live Music & Coffee",
    "parent_artist_id": 5,
    # "artist_name": "Matt Quevedo",
    # "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }
show3={
    "id": 3,
    "parent_venue_id": 3,
    # "venue_name": "Park Square Live Music & Coffee",
    "parent_artist_id": 6,
    # "artist_name": "The Wild Sax Band",
    # "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }
show4={
    "id": 4,
    "parent_venue_id": 3,
    # "venue_name": "Park Square Live Music & Coffee",
    "parent_artist_id": 6,
    # "artist_name": "The Wild Sax Band",
    # "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }
show5={
    "id": 5,
    "parent_venue_id": 3,
    # "venue_name": "Park Square Live Music & Coffee",
    "parent_artist_id": 6,
    # "artist_name": "The Wild Sax Band",
    # "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }

show_list = [show1,show2,show3,show4,show5]

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
    cursor = conn.cursor()
    for show in show_list:

      # Create show record in db
      columns = show.keys()
      values = [show[column] for column in columns]
      insert_statement = """INSERT INTO "Show" (%s) values %s returning id"""
      query = cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
      cursor.execute(query)
      inserted_id = cursor.fetchone()[0]
      print("Inserted id: %s"%(inserted_id))
    conn.commit()

except (Exception, psycopg2.Error) as e:
    print(e)

finally:
    if (conn):
        cursor.close()
        conn.close()
        print("Connection closed.")