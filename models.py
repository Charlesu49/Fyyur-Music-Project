from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String()))
    address = db.Column(db.String(200))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)

    # return a dictionary of venues
    def venue_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
        }

    
    def __repr__(self):
        return f'<Venue {self.name} with ID {self.id}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)


    # return a dictionary of artists
    def artist_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
        }


    def __repr__(self):
        return f'<Artist - {self.name} with ID  {self.id}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


    # returns a dictionary of show artists and venue respectively
    def show_artist(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            # do below to convert date time to a string
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def show_venue(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            # do below to convert date time to a string
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }

# ======================================

# class Venue(db.Model):
#     __tablename__ = 'venue'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     genres = db.Column(db.Array(db.String()))
#     address = db.Column(db.String(120))
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     website_link = db.Column(db.String(120))
#     seeking_talent = db.Column(db.Boolean)
#     seeking_description = db.Column(db.String(500))
#     shows = db.relationship('Show', backref='Venue', lazy=True)

#     def __repr__(self):
#         return '<Venue {}>'.format(self.name)


# class Artist(db.Model):
#     __tablename__ = 'artist'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     genres = db.Column(db.ARRAY(db.String))
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     website_link = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     seeking_venue = db.Column(db.Boolean)
#     seeking_description = db.Column(db.String(500))
#     shows = db.relationship('show', backref='Artist', lazy=True)

#     def __repr__(self):
#         return '<Artist {}>'.format(self.name)

# class Show(db.Model):
#     __tablename__ = 'Show'
#     id = db.Column(db.Integer, primary_key=True)
#     artist_id = db.Column(db.Integer, db.ForeignKey(
#         'Artist.id'), nullable=False)
#     venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)

#     def __repr__(self):
#         return '<Show {}{}>'.format(self.artist_id, self.venue_id)\

# genres = request.form.getlist('genres')
