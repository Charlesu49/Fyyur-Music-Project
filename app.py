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
from sqlalchemy.sql.functions import current_date, current_time
from forms import *
from flask_migrate import Migrate
from models import db, Artist, Venue, Show
import sys
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
  return render_template('/pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  
  venues = Venue.query.all()
  places = set()

  for venue in venues:
    places.add((venue.city, venue.state))

  for place in places:
    data.append({
      "city": place[0],
      "state": place[1],
      "venues": []
    })

  for venue in venues:
    num_upcoming_shows = 0

    shows = Show.query.filter_by(venue_id=venue.id).all()
    currentDate = datetime.now()

    for show in shows:
      if show.start_time > currentDate:
        num_upcoming_shows += 1
    

    for venue_area in data:
      if venue.state == venue_area['state'] and venue.city == venue_area['city']:
        venue_area['venues'].append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_upcoming_shows
        })

  return render_template('pages/venues.html', areas=data)




@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('/forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    venue = Venue()
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.genres = request.form.getlist('genres')
    # get genre as a list
    # genre_list = request.form.getlist('genres')
    # convert the list to string seperated by ","
    # venue.genres = ','.join(genre_list)
    venue.facebook_link = request.form['facebook_link']
    db.session.add(venue)
    db.session.commit()
    db.session.close()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.' )
    else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!' )
  return render_template('/pages/home.html')




@app.route('/venues/search', methods=['POST'])
def search_venues():
  keyword = request.form.get('search_term')
  venues = Venue.query.filter(
      Venue.name.ilike('%{}%'.format(keyword))).all()

  data = []
  for venue in venues:
      tmp = {}
      tmp['id'] = venue.id
      tmp['name'] = venue.name
      tmp['num_upcoming_shows'] = len(venue.shows)
      data.append(tmp)

  response = {}
  response['count'] = len(data)
  response['data'] = data

  return render_template('/pages/search_venues.html', results=response, keyword=request.form.get('search_term', ''))




@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  
  # declare variables
  past_shows = []
  upcoming_shows = []

  # select from show and venue, joining both on venue_id and include a where clause for the show time
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time < datetime.now()).all()

  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time > datetime.now()).all()

  for show in past_shows_query:
    data = {
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': format_datetime(str(show.start_time))
    }
    past_shows.append(data)


  for show in upcoming_shows_query:
    data = {
      'artist_id': show.artist_id,
      'artist_name': show.venue.name,
      'artist_image_link': show.artist.image_link,
      'start_time': format_datetime(str(show.start_time))
    }
    past_shows.append(data)

  data = {
    'id': venue.id,
    'name': venue.name,
    'genres': venue.genres,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'facebook_link': venue.facebook_link,
    'image_link': venue.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows),
    'website': venue.website
  }

  return render_template('pages/show_venue.html', venue=data)




@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  # fetch data and pre-populated the form fields
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  return render_template('/forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)

  error = False
  try:
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      venue.genres = request.form.getlist('genres'),
      venue.facebook_link = request.form['facebook_link']
      db.session.add(venue)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
      if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
      else:
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))




@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = None

  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()

  if error:
    # flash error and return to home page
    flash('An error occured')
    return redirect(url_for('index'))
  else:
    # flash success and return to home page
    flash('Venue successfully deleted')
    return redirect(url_for('index'))
  






#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []

  # fetch artists data
  artists = Artist.query.all()

  # append the initially declared data list
  for artist in artists:
    data.append(
      {
        "id": artist.id,
        "name": artist.name
      }
    )
  return render_template('/pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # get the search term from the form
  search_term = request.form.get('search_term', '')

  # query the artist table filtering with the search term
  search_results = Artist.query.filter( Artist.name.ilike('%{}%'.format(search_term))).all()  # search results by ilike matching partern to match every search term

  # assign the results to the below variables to be passed into the search artist page
  response = {}
  response['count'] = len(search_results)
  response['data'] = search_results

  return render_template('/pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  # shows = Show.query.filter_by(artist_id=artist_id).all()

  # declare variables
  past_shows = []
  upcoming_shows = []

  # select from show and artist, joining both on artist_id and including a where clause for the show time
  past_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time < datetime.now()).all()

  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time > datetime.now()).all()

  for show in past_shows_query:
    data = {
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': format_datetime(str(show.start_time))
    }
    past_shows.append(data)


  for show in upcoming_shows_query:
    data = {
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': format_datetime(str(show.start_time))
    }
    past_shows.append(data)

  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genres,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'facebook_link': artist.facebook_link,
    'image_link': artist.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows),
    'website': artist.website
  }

  return render_template('/pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  # fetch data and pre-populate form fields
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)

  return render_template('/forms/edit_artist.html', form=form, artist=artist)



@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get(artist_id)
  
  try:
    artist = Artist.query.filter_by(id=artist_id).all()[0]

    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    genre_list = request.form.getlist('genres')
    artist.genres = ','.join(genre_list)
    artist.facebook_link = request.form.get('facebook_link')
    artist.website = request.form.get('website_link')
    artist.image_link = request.form.get('image_link')
    artist.seeking_venue = request.form.get('seeking_venue') == 'True'
    artist.seeking_description =request.form.get('seeking_description')

    db.session.commit()
  except:
    db.session.rollback()
    flash('An error occurred. Artist could not be updated')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # form = ArtistForm()
  error = False
  try:
      artist = Artist()
      artist.name = request.form.get('name')
      artist.city = request.form.get('city')
      artist.state = request.form.get('state')
      artist.phone = request.form.get('phone')
      artist.genres = request.form.getlist('genres')
      # artist.genres = ','.join(genre_list)
      artist.website = request.form.get('website')
      artist.image_link = request.form.get('image_link')
      artist.facebook_link = request.form.get('facebook_link')
      artist.seeking_description = request.form.get('seeking_description')
      db.session.add(artist)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
      if error:
          flash('An error occurred. Artist ' +
                request.form['name'] + ' could not be listed.')
      else:
          flash('Artist ' + request.form['name'] +
                ' was successfully listed!')
      return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()

  data = []
  for show in shows:
      data.append({
          'venue_id': show.venue.id,
          'venue_name': show.venue.name,
          'artist_id': show.artist.id,
          'artist_name': show.artist.name,
          'artist_image_link': show.artist.image_link,
          'start_time': show.start_time.isoformat()
      })
  return render_template('/pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('/forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  error = False
  try:
      show = Show()
      show.artist_id = request.form['artist_id']
      show.venue_id = request.form['venue_id']
      show.start_time = request.form['start_time']
      db.session.add(show)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
      if error:
          flash('An error occurred. Show could not be listed')
      else:
          flash('Show was successfully listed!')
      return render_template('/pages/home.html')


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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
