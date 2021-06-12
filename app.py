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
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
# import from config file in Flask
app.config.from_object('config')
db = SQLAlchemy(app)
# link up Flask app and SQLAlchemy db to use Flask-Migrate
migrate = Migrate(app, db, compare_type=True)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String(120)))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='parent_venue', lazy=True)

    def __repr__(self):
      return f'<Venue ID: {self.id}, name: {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String(120)))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='parent_artist', lazy=True)

    def __repr__(self):
      return f'<Artist ID: {self.id}, name: {self.name}>'

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_time = db.Column(db.DateTime, nullable=False)
    parent_artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    parent_venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self):
      return f'<Show name: {self.name}, start time: {self.start_time}, Artist: {self.parent_artist_id}, Venue: {self.parent_venue_id}>'

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
  data = Venue.query.get(venue_id)
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
    venue = Venue(name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  address = form.address.data,
                  phone = form.phone.data,
                  genres = form.genres.data,
                  image_link = form.image_link.data,
                  seeking_talent = form.seeking_talent.data,
                  seeking_description = form.seeking_description.data)
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

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  for instance in Artist.query.with_entities(Artist.id, Artist.name):
      print(instance.id, instance.name)
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
  data = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

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
    # retrieve object
    venue = Venue.query.get(venue_id)
    # update fields
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.image_link = form.image_link.data
    venue.website = form.website_link.data
    venue.facebook_link = form.facebook_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
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
    artist = Artist(name = form.name.data,
                    city = form.city.data,
                    state = form.state.data,
                    phone = form.phone.data,
                    website = form.website_link.data,
                    genres = form.genres.data,
                    image_link = form.image_link.data,
                    facebook_link = form.facebook_link.data,
                    seeking_venue = form.seeking_venue.data,
                    seeking_description = form.seeking_description.data)
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

  data =[]
  query_result = Show.query.join(Artist).join(Venue).all()
  for row in query_result:
    data.append({"venue_id":  row.parent_venue_id, "venue_name": row.parent_venue.name, "artist_id": row.parent_artist_id, "artist_name": row.parent_artist.name, "artist_image_link": row.parent_artist.image_link,  "start_time": row.start_time.strftime('%Y-%m-%d %H:%M:%S')})

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
