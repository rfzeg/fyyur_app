import psycopg2
from psycopg2.extensions import AsIs

artist4={
    "id": 4,
    "name": "Guns N Petals",
    # "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    # "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    # "past_shows": [{
    #   "venue_id": 1,
    #   "venue_name": "The Musical Hop",
    #   "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #   "start_time": "2019-05-21T21:30:00.000Z"
    # }],
    # "upcoming_shows": [],
    # "past_shows_count": 1,
    # "upcoming_shows_count": 0,
  }
artist5={
    "id": 5,
    "name": "Matt Quevedo",
    # "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    # "past_shows": [{
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2019-06-15T23:00:00.000Z"
    # }],
    # "upcoming_shows": [],
    # "past_shows_count": 1,
    # "upcoming_shows_count": 0,
  }
artist6={
    "id": 6,
    "name": "The Wild Sax Band",
    # "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    # "past_shows": [],
    # "upcoming_shows": [{
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2035-04-01T20:00:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2035-04-08T20:00:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "start_time": "2035-04-15T20:00:00.000Z"
    # }],
    # "past_shows_count": 0,
    # "upcoming_shows_count": 3,
  }
artist7={
    "id": 7,
    "name": "Cosmic Play.",
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5555",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    # "past_shows": [], # not congruent with data in venues
    # "upcoming_shows": [], # not congruent with data in venues
    # "past_shows_count": 0,
    # "upcoming_shows_count": 0,
  }

artist_list = [artist4,artist5,artist6,artist7]

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
    for artist in artist_list:
      columns = artist.keys()
      values = [artist[column] for column in columns]
      insert_statement = """INSERT INTO "Artist" (%s) values %s  """
      query = cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
      cursor.execute(query)
    conn.commit()

except (Exception, psycopg2.Error) as e:
    print(e)

finally:
    if (conn):
        cursor.close()
        conn.close()
        print("Connection closed.")