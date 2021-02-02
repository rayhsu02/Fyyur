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
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Shows(db.Model):
  __tablename__ = "shows"

  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
  start_time= db.Column(db.DateTime, nullable=False, primary_key=True)
  venue = db.relationship("Venue", backref="show_venue")
  artist = db.relationship("Artist", backref='show_artists', lazy=True)

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Shows', backref="venues")
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<venue {self.name}>'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    shows = db.relationship('Shows', backref="artists")
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


def init_db():
  db.create_all()

def seed_data():
  artist = Artist( name="Guns N Petals",
    genres= ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    city= "San Francisco",
    state= "CA",
    phone= "326-123-5000",
    website='https://www.gunsnpetalsband.com',
    facebook_link= "https://www.facebook.com/GunsNPetals",
    seeking_venue= True,
    seeking_description= "Looking for shows to perform at in the San Francisco Bay Area!",
    image_link= "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    )
  db.session.add(artist)
  
  venue = Venue( 
    name= "The Musical Hop",
    genres= ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    address= "1015 Folsom Street",
    city= "San Francisco",
    state= "CA",
    phone= "123-123-1234",
    website= "https://www.themusicalhop.com",
    facebook_link= "https://www.facebook.com/TheMusicalHop",
    seeking_talent= True,
    seeking_description= "We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link= "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
   
  )
  db.session.add(venue)
  venue2 = Venue( 
    name= "The Dueling Pianos Bar",
    genres= ["Classical", "R&B", "Hip-Hop"],
    address= "335 Delancey Street",
    city= "New York",
    state= "NY",
    phone= "914-003-1132",
    website= "https://www.theduelingpianos.com",
    facebook_link= "https://www.facebook.com/theduelingpianos",
    seeking_talent= False,
    image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  
  )
  db.session.add(venue2)
  venue3 = Venue( 
    name= "Park Square Live Music & Coffee",
    genres= ["Rock n Roll", "Jazz", "Classical", "Folk"],
    address= "34 Whiskey Moore Ave",
    city= "San Francisco",
    state= "CA",
    phone= "415-000-1234",
    website= "https://www.parksquarelivemusicandcoffee.com",
    facebook_link= "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent= False,
    image_link= "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
 
  )
  db.session.add(venue3)
  db.session.commit()

  show1 = Shows(start_time=datetime.now(), venue_id=venue.id, artist_id=artist.id)
  db.session.add(show1)
  db.session.commit()
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
    "past_shows_count": len([show for show in venue.shows if show.start_time + timedelta(1)  < datetime.now()]),
    "past_shows": [show for show in venue.shows if show.start_time + timedelta(1)< datetime.now()],
    "upcoming_shows_count": len([show for show in venue.shows if show.start_time > datetime.now()]),
    "upcoming_shows":[show for show in venue.shows if show.start_time > datetime.now()],
   
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
    "past_shows_count": len([show for show in artist.shows if show.start_time + timedelta(1)  < datetime.now()]),
    "past_shows": [show for show in artist.shows if show.start_time + timedelta(1)< datetime.now()],
    "upcoming_shows_count": len([show for show in artist.shows if show.start_time > datetime.now()]),
    "upcoming_shows":[show for show in artist.shows if show.start_time > datetime.now()],
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
