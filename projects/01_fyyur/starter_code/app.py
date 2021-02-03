#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime, timedelta
from models import db, Artist, Shows, Venue
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  result = Venue.query.distinct(Venue.city, Venue.state).order_by(Venue.city, Venue.state)
  for r in result:
    data.append({
      "city": r.city,
      "state": r.state,
      "venues": [{
        "id": venue.id,
        "name": venue.name,
        "num_upcomming_shows" : len([show for show in venue.shows if datetime(show.start_time.year, show.start_time.month, show.start_time.day )> datetime.now()])
      } for venue in Venue.query.filter_by(city=r.city , state=r.state )]
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchTerm = request.form.get('search_term', '')
  
  data = Venue.query.filter(func.lower(Venue.name).like('%' + func.lower(searchTerm) + '%')).all()
  
  count = len(data)
  response = {
    "count" : count,
    "data" : [{
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len([show for show in venue.shows if datetime(show.start_time.year, show.start_time.month, show.start_time.day )> datetime.now()])
 } for venue in data]
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  
  venue = Venue.query.get(venue_id)

  shows = db.session.query(Shows)
  join_venue = shows.join(Venue)
  show_for_venue = join_venue.filter(Shows.venue_id == venue_id)
  past_shows = show_for_venue.filter(Shows.start_time < datetime.now()).all()
  upcoming_shows = show_for_venue.filter(Shows.start_time >= datetime.now()).all()

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows_count": len(past_shows),
    "past_shows": past_shows,
    "upcoming_shows_count": len(upcoming_shows),
    "upcoming_shows":upcoming_shows,
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
 
  error=False
  try:
  
    form = VenueForm(request.form, meta={'csrf': False})
    new_venue = Venue()
    form.populate_obj(new_venue)
    new_venue.image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    db.session.add(new_venue)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      flash('Venue ' + request.form['name'] + ' was an error!')
      return render_template('pages/home.html')
    else:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')
            

  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error= False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
    
  finally:
    db.session.close()
    if error:
      flash('Venue was an error!')
      print(sys.exc_info())
      return render_template('pages/home.html')
    else:
      flash('Venue: ' + venue.name + '  was successfully deleted!')
      return jsonify({'success': True})
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  artists = Artist.query.all()
  data = [{
    "id": artist.id,
    "name":artist.name
  } for artist in artists
  ]

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(func.lower(Artist.name).like('%' + func.lower(search_term) + '%')).all()
  
  response = {
    "count": len(artists),
    "data": [
      {
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": len([show for show in artist.shows if datetime(show.start_time.year, show.start_time.month, show.start_time.day ) > datetime.now()])
      } for artist in artists
    ]
  }
 
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  artist = Artist.query.get(artist_id)
  shows = db.session.query(Shows)
  join_artist = shows.join(Artist)
  show_for_artist = join_artist.filter(Shows.artist_id == artist_id)
  past_shows = show_for_artist.filter(Shows.start_time < datetime.now()).all()
  upcoming_shows = show_for_artist.filter(Shows.start_time >= datetime.now()).all()  

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows_count": len(past_shows),
    "past_shows": past_shows,
    "upcoming_shows_count": len(upcoming_shows),
    "upcoming_shows": upcoming_shows,
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  form = ArtistForm(request.form, meta={'csrf': False})
  artist = Artist.query.get(artist_id)
  form.populate_obj(artist)
  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  form = VenueForm(request.form, meta={'csrf': False})
  venue = Venue.query.get(venue_id)
  form.populate_obj(venue)
  db.session.commit()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form

  error=False
  try:
     form = ArtistForm(request.form, meta={'csrf': False})
     new_artist = Artist()
     form.populate_obj(new_artist)
     new_artist.image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
     db.session.add(new_artist)
     db.session.commit()
  except:
    db.session.rollback()
    error=True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Artist ' + request.form['name']  + ' could not be listed.')
      return render_template('pages/home.html')
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
 
  shows = Shows.query.all()
  
  data = [{
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")

  } for show in shows
  ]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
 
  error = False
  try:
     form = ShowForm(request.form, meta={'csrf': False})
     newshow = Shows()
     form.populate_obj(newshow)
    #  print(newshow)
     db.session.add(newshow)
     db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error=True
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Show could not be listed.')
      print('error listed!')
      return render_template('pages/home.html')
    else:
      print('Show was successfully listed!')
      flash('Show was successfully listed!')
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
    # print("call seed data")
    # seed_data()
    app.run()
    

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
