from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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