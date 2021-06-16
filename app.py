#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fyyur Flask app using PostgreSQL via SQLAlchemy
Author: Roberto Zegers R.
Date: June 2021
Usage: python3 app.py
"""


#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    jsonify
    )
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show # Models
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
# import from config file in Flask
app.config.from_object('config')
db.init_app(app)
# link up Flask app and SQLAlchemy db to use Flask-Migrate
migrate = Migrate(app, db, compare_type=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  for row in db.session.query(func.count(Venue.id), Venue.state, Venue.city).group_by(Venue.state,Venue.city).all():
    state = row[1]
    city = row[2]
    # grab details
    venues = []
    result = db.session.query(Venue).filter(Venue.state==str(state), Venue.city==str(city))
    for row in result:
      #count_upcoming_shows = Show.query.filter(Show.parent_venue_id==row.id).filter(Show.start_time>datetime.now()).count()
      #venues.append({"id":row.id,"name":row.name,"num_upcoming_shows": count_upcoming_shows})
      venues.append({"id":row.id,"name":row.name})
    data.append({"state":str(state),"city":str(city),"venues": venues })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Case-insensitive search on venues with partial string search.

  response = {}
  search_term = request.form.get('search_term', '')
  query_term = "%%"+search_term+"%%"
  query_result = db.session.query(Venue).filter(Venue.name.ilike(query_term)).all()
  data = []
  for row in query_result:
    #count_upcoming_shows = Show.query.filter(Show.parent_venue_id==row.id).filter(Show.start_time>datetime.now()).count()
    #data.append({"id": row.id, "name": row.name, "num_upcoming_shows": count_upcoming_shows})
    data.append({"id": row.id, "name": row.name})
  response["count"] = len(query_result)
  response["data"] = data

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.get(venue_id)
  venue_shows_query = Show.query.filter(Show.parent_venue_id==venue_id)
  upcoming_shows_query = venue_shows_query.filter(Show.start_time>datetime.now())
  past_shows_query = venue_shows_query.filter(Show.start_time<datetime.now())
  upcoming_shows_count = upcoming_shows_query.count()
  past_shows_count = len(venue.shows) - upcoming_shows_count
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }

  for show in upcoming_shows_query:
    data["upcoming_shows"].append({"artist_id": show.parent_artist.id,
                                   "artist_name": show.parent_artist.name,
                                   "artist_image_link": show.parent_artist.image_link,
                                   "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                   })

  for show in past_shows_query:
    data["past_shows"].append({"artist_id": show.parent_artist.id,
                               "artist_name": show.parent_artist.name,
                               "artist_image_link": show.parent_artist.image_link,
                               "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                               })

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  error = False
  try:
    venue = Venue()
    # populate the attributes of venue with data from the form’s fields
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
      error = True
      db.session.rollback()
      flash('An error occured. Venue ' + request.form['name'] + ' could not be listed!')
  finally:
      db.session.close()
  
  return render_template('pages/home.html')

# Endpoint for deleting a venue
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get_or_404(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue with id: ' + str(venue_id) + ' was successfully deleted!')
    except:
        db.session.rollback()
        error = True
        flash('An error occured, venue with id:' + str(venue_id) + ' could not be deleted!')
    finally:
        db.session.close()
        return jsonify({"success": True})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  for instance in Artist.query.with_entities(Artist.id, Artist.name):
      data.append({"id": instance.id, "name": str(instance.name)})

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Case-insensitive search on artists with partial string search.

  response = {}
  search_term = request.form.get('search_term', '')
  query_term = "%%"+search_term+"%%"
  query_result = db.session.query(Artist).filter(Artist.name.ilike(query_term)).all()
  data = []
  for row in query_result:
    #count_upcoming_shows = Show.query.filter(Show.parent_artist_id==row.id).filter(Show.start_time>datetime.now()).count()
    #data.append({"id": row.id, "name": row.name, "num_upcoming_shows": count_upcoming_shows})
    data.append({"id": row.id, "name": row.name})
  response["count"] = len(query_result)
  response["data"] = data

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  artist = Artist.query.get(artist_id)
  artist_shows_query = Show.query.filter(Show.parent_artist_id==artist_id)
  upcoming_shows_query = artist_shows_query.filter(Show.start_time>datetime.now())
  past_shows_query = artist_shows_query.filter(Show.start_time<datetime.now())
  upcoming_shows_count = upcoming_shows_query.count()
  past_shows_count = len(artist.shows) - upcoming_shows_count
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }

  for show in upcoming_shows_query:
    data["upcoming_shows"].append({"venue_id": show.parent_venue.id,
                                       "venue_name": show.parent_venue.name,
                                       "venue_image_link": show.parent_venue.image_link,
                                       "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                       })

  for show in past_shows_query:
    data["past_shows"].append({"venue_id": show.parent_venue.id,
                               "venue_name": show.parent_venue.name,
                               "venue_image_link": show.parent_venue.image_link,
                               "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                               })

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # retrieve current data with the given artist_id
  data = Artist.query.get(artist_id)
  # Fill in ArtistForm with current data from the db
  form = ArtistForm(obj=data)
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  error = False
  try:
    artist = Artist.query.get(artist_id)
    # populate the attributes of artist with data from the form’s fields
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    error = True
    db.session.rollback()
    flash('An error occured. Artist ' + request.form['name'] + ' could not be updated!')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # retrieve current data with the given venue_id
  data = Venue.query.get(venue_id)
  # Pre-populate VenueForm with current data from the db
  form = VenueForm(obj=data)
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  error = False
  try:
    venue = Venue.query.get(venue_id)
    # populate the attributes of venue with data from the form’s fields
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    error = True
    db.session.rollback()
    flash('An error occured. Venue ' + request.form['name'] + ' could not be updated!')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  error = False
  try:
    artist = Artist()
    # populate the attributes of artist with data from the form’s fields
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      error = True
      db.session.rollback()
      flash('An error occured. Artist ' + request.form['name'] + ' could not be listed!')
  finally:
      db.session.close()

  return render_template('pages/home.html')
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # To-do: display only upcoming shows
  data =[]
  query_result = Show.query.join(Artist).join(Venue).all()
  for row in query_result:
    data.append({"venue_id": row.parent_venue_id, "venue_name": row.parent_venue.name, "artist_id": row.parent_artist_id, "artist_name": row.parent_artist.name, "artist_image_link": row.parent_artist.image_link,  "start_time": row.start_time.strftime('%Y-%m-%d %H:%M:%S')})

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  error = False
  try:
    show = Show(start_time = form.start_time.data,
                parent_artist_id = form.artist_id.data,
                parent_venue_id = form.venue_id.data)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
      error = True
      db.session.rollback()
      flash('An error occured. Show could not be listed!')
  finally:
      db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
