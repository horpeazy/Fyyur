from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.PickleType, nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")

    def __repr__(self) -> str:
        return f'<ID: {self.id} Name: {self.name}>'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.PickleType, nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")
    available_days = db.relationship('AvailableDays', backref='artist', lazy=True)
    songs = db.relationship('Song', backref='artist', lazy=True)

    def __repr__(self) -> str:
        return f'<ID: {self.id}  Name: {self.name}>'


class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    songs = db.relationship('Song', backref='album', lazy=True)

    def __repr__(self) -> str:
        return f'<ID: {self.id} Name: {self.name} Artist ID: {self.artist_id}>'

class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)

    def __repr__(self) -> str:
        return f'<ID: {self.id} Name: {self.name}>'

class AvailableDays(db.Model):
    __tablename__ = 'available_days'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Day: {self.name}>'
