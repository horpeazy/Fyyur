#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from http.client import INTERNAL_SERVER_ERROR
import sys
from xml.dom import NotFoundErr
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
    abort )
import logging
from flask_moment import Moment
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from forms import *
from models import *
from datetime import datetime
import calendar
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
db.create_all(app=app)

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
  artists = db.session.query(Artist.id, Artist.name).\
                      order_by(db.desc(Artist.id)).limit(10).all()
  venues = db.session.query(Venue.id, Venue.name).\
                      order_by(db.desc(Venue.id)).limit(10).all()
  return render_template('pages/home.html', artists=artists, venues=venues)

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  try:
    """Select a combination of city and state that are 
        unique as areas from the database
    """
    areas = db.session.query(Venue.city, Venue.state).\
      group_by(Venue.city, Venue.state).all()
    data = []
    
    #Loop through the areas and get the corresponding venues
    for area in areas:
      area_data = {}
      venues = db.session.query(Venue.id, Venue.name).\
                filter_by(city=area.city, state=area.state)
      area_data['city'] = area.city
      area_data['state'] = area.state
      area_data['venues'] = venues
      data.append(area_data)
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term=request.form.get('search_term', '')     
  try:
    query_results = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).\
                          all()  
    results = {}
    results['data'] = query_results
    results['count'] = len(query_results)
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('pages/search_venues.html', 
                        results=results, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  try:
    venue = Venue.query.get_or_404(venue_id)

    past_shows = []
    upcoming_shows = []
    
    #Returns the shows from the joined statement performed when loading venue.shows
    for show in venue.shows:
        temp_show = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        if show.start_time <= datetime.now():
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    # converts object class to dict
    data = vars(venue)

    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('pages/show_venue.html', venue=data)

# #  Create Venue
# #  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  error = False
  if form.validate_on_submit:
    try:
      # create an instance of venue
      venue = Venue()
      form.populate_obj(venue)

      db.session.add(venue)                           
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      if error == True:
        #on unsuccessful db insert, flash an error instead. 
        flash('An error occurred. Venue ' +venue.name+' could not be listed.')
      else:
        # on successful db insert, flash success
        flash('Venue ' + venue.name + ' was successfully listed!')
      db.session.close()
  else:
    #If form does not validate, render back the form with errors
    return render_template('forms/new_venue.html', form=form)

  return redirect(url_for('index'))


@app.route('/venues/delete/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    if error == True:
      #on unsuccessful db insert, flash an error instead. 
      flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
      return redirect(url_for('index'))
    else:
      # on successful db insert, flash success
      flash('Venue ' + venue.name + ' was successfully deleted!')
    db.session.close()
  
  return redirect(url_for('index'))


# #  Artists
# #  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  try:
    artists = db.session.query(Artist.id, Artist.name).all()
  except:
    print(sys.exc_info())
    abort(500)
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term', '')      
  try:
    query_results = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).\
                            all() 
    results = {}
    results['data'] = query_results
    results['count'] = len(query_results)
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('pages/search_artists.html',
                        results=results, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  song_form = SongForm()
  album_form = AlbumForm()
  songs = Song.query.filter_by(artist_id=artist_id).all()
  albums = Album.query.filter_by(artist_id=artist_id).all()
  try:
    artist = Artist.query.get_or_404(artist_id)

    past_shows = []
    upcoming_shows = []
    
    #Returns the shows from the join statement performed when loading artist.shows
    for show in artist.shows:
        temp_show = {
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        if show.start_time <= datetime.now():
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    # object class to dict
    data = vars(artist)

    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows)
    data['upcoming_shows_count'] = len(upcoming_shows)
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('pages/show_artist.html',artist=artist,song_form=song_form,
                        album_form=album_form, songs=songs, albums=albums)

# #  Update
# #  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  try:
    artist = Artist.query.get_or_404(artist_id)

    #Populate the form with venue information
    form = ArtistForm(obj=artist)
    form.available_days.data = [d.day for d in artist.available_days]
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(request.form, obj=artist)
  error = False

  if form.validate_on_submit:
    try:
      #current available days
      available_days = [d.day for d in artist.available_days]   
      submitted_days = form.available_days.data     

      #Check for discrepancies between existing available and submitted days
      if sorted(submitted_days) != sorted(available_days):
        #Delete existing genres
        for day in artist.available_days:
          db.session.delete(day)

        #Add new set of available days
        for day in form.available_days.data:
          name = calendar.day_name[day]
          available_day = AvailableDays(day=day,artist_id=artist_id,name=name)
          db.session.add(available_day)

      artist.name=form.name.data
      artist.city=form.city.data
      artist.state=form.state.data
      artist.phone=form.phone.data
      artist.image_link=form.image_link.data
      artist.genres=form.genres.data
      artist.facebook_link=form.facebook_link.data
      artist.website_link=form.website_link.data
      artist.seeking_venue=form.seeking_venue.data
      artist.seeking_description=form.seeking_description.data

      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      if error == True:
        #on unsuccessful db insert, flash an error instead. 
        flash('An error occurred. Artist '+artist.name+' could not be update.')
        abort(500)
      else:
        # on successful db insert, flash success
        flash('Artist ' + artist.name + ' was successfully updated!')
      db.session.close()
  else:
    return render_template('forms/edit_artist.html', form=form, artist=artist)

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  try:
    venue = Venue.query.get_or_404(venue_id)

    #Populate the form with venue information
    form = VenueForm(obj=venue)
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(request.form, obj=venue)
  error = False

  if form.validate_on_submit:
    try:
      form.populate_obj(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      if error == True:
        #on unsuccessful db insert, flash an error instead. 
        flash('An error occurred. Venue '+venue.name+' could not update.')
        abort(500)
      else:
        # on successful db insert, flash success
        flash('Venue ' + venue.name + ' was successfully updated!')
      db.session.close()
  else:
    #Render the edit venue template if there is an error with the form
    return render_template('forms/edit_venue.html', form=form, venue=venue)

  return redirect(url_for('show_venue', venue_id=venue_id))

# #  Create Artist
# #  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = ArtistForm(request.form)
  error = False

  if form.validate_on_submit:
    try:
      # create an instance of artist
      artist = Artist(name=form.name.data,
                      city=form.city.data,
                      state=form.state.data,
                      phone=form.phone.data,
                      image_link=form.image_link.data,
                      genres=form.genres.data,
                      facebook_link=form.facebook_link.data,
                      website_link=form.website_link.data,
                      seeking_venue=form.seeking_venue.data,
                      seeking_description=form.seeking_description.data
                      )
      db.session.add(artist)

      #Query the database to flush already persisted data
      #Also try to catch cases of already existing artist name
      try:
        db.session.query(Artist.id).filter_by(name=form.name.data).one()
      except:
        flash('Artist Name already Exists')
        abort(500)
      
      # Add the available days to the available days table
      for day in form.available_days.data:
        name = calendar.day_name[day]
        available_day = AvailableDays(day=day, artist_id=artist.id, name=name)
        db.session.add(available_day)
      
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      if error == True:
        #on unsuccessful db insert, flash an error instead. 
        flash('An error occurred. Artist '+ artist.name +' could not be listed')
        abort(500)
      else:
        # on successful db insert, flash success
        flash('Artist ' + artist.name + ' was successfully listed!')
      db.session.close()
  else:
    #If there are any errors in the form, render back the form 
    return render_template('forms/new_artist.html', form=form)

  return redirect(url_for('index'))


# #  Shows
# #  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  try:
    shows = Show.query.all()
    data = []
    for show in shows:
      show_detail = {
        'venue_id' : show.venue.id,
        'venue_name' : show.venue.name,
        'artist_id' : show.artist.id,
        'artist_name' : show.artist.name,
        'artist_image_link' : show.artist.image_link,
        'start_time' : show.start_time.strftime("%m/%d/%Y, %H:%M")
      }

      data.append(show_detail)
  except:
    print(sys.exc_info())
    abort(500)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  form = ShowForm()
  error = False
  if form.validate_on_submit:
    try:    
      artist_id = form.artist_id.data
      venue_id = form.venue_id.data
      start_time = form.start_time.data
      try:
        artist = Artist.query.get_or_404(artist_id)
        venue = Venue.query.get_or_404(venue_id)
      except:
        flash('Either Artist or Venue does not exist')

      available_days = [d.day for d in artist.available_days]    
      day_of_week = start_time.weekday()                        

      if day_of_week not in available_days:
        flash('Artist not available on this date, see artist page')
        return redirect(url_for('create_shows'))
      else:
        show = Show(artist_id=artist_id, 
                    venue_id=venue_id,
                    start_time=start_time)

        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close() 
      if error == True:
        # on unsuccessful db insert, flash an error instead.
        abort(500)
  else:
    return redirect(url_for('create_shows'))

  return redirect(url_for('index'))



@app.route('/song/<int:artist_id>/create', methods=['POST'])
def create_song(artist_id):
  form = SongForm()
  error = False
  if form.validate_on_submit:
    name = form.name.data
    album_name = form.album.data
    album = 1

    """Check to see if album name is empty, otherwise, 
       get the album instance ignoring the case
     """
    if album_name != '':
      #Returns None if albulm doesn't exist
      album = Album.query.filter(Album.name.ilike(album_name), 
                                  Album.artist_id == artist_id).first()
    
    """If album exists or is not provided, add song to database 
       otherwise flash an error message
    """
    if album != None:
      try:
        if album == 1:
          # Album name was not provided, create songs instance without album id
          song = Song(name=name, artist_id=artist_id)
        else:
          #Get album id and create song instance
          album_id = album.id
          song = Song(name=name, artist_id=artist_id, album_id=album_id)

        db.session.add(song)
        db.session.commit()
      except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
      finally:
        db.session.close()
        if error == True:
          flash('An error occured, could not list song')
          abort(500)
        else:
          flash('Song was successfully listed')
    else:
      flash("Could not list your song, Album doesn't exist")
  else:
    flash('Invalid form')
    return redirect(url_for('show_artist', artist_id=artist_id))

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/song/<int:artist_id>/album', methods=['POST'])
def create_album(artist_id):
  form = AlbumForm()
  error = False
  if form.validate_on_submit:
    name = form.name.data
    
    try:
      album = Album(name=name, artist_id=artist_id)
      db.session.add(album)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
      if error == True:
        flash('An erroe occured, could not list album')
        abort(500)
      else:
        flash('Album was successfully listed') 

  return redirect(url_for('show_artist', artist_id=artist_id))


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
