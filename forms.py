from datetime import datetime
from wsgiref.validate import validator
from xml.dom import ValidationErr
from flask_wtf import FlaskForm as  Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL , Optional, ValidationError
from enums import State, Genre, Days
import re


def is_valid_phone(number):
    """ Validate phone numbers """
    regex = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    return regex.match(number)

#Adapted from stackoverflow
# def coerce_for_enum(enum):
#     def coerce(name):
#         if isinstance(name, enum):
#             return name.value
#         try:
#             return enum[name].value
#         except KeyError:
#             raise ValidationError(name)
#     return coerce



class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices = State.choices(),
        coerce = State.coerce_for_enum()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[URL(), Optional()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices = Genre.choices() ,
        coerce= Genre.coerce_for_enum() 
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link', validators=[URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description', validators=[Optional()]
    )

    def validate(self):
        """Custom Validator"""
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).values()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True




class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices = State.choices(),
        coerce = State.coerce_for_enum()
    )
    phone = StringField(
        # TODO implement validation logic for phone 
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices = Genre.choices(),
        coerce= Genre.coerce_for_enum()
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link',
        validators=[URL()]
    )

    website_link = StringField(
        'website_link', validators=[Optional()]
    )
    
    available_days = SelectMultipleField(
        'available_days', validators=[Optional()],
        choices= Days.choices(),
        coerce= Days.coerce_for_enum()
    )

    seeking_venue = BooleanField( 'seeking_venue', validators=[Optional()] )

    seeking_description = StringField(
            'seeking_description', validators=[Optional()]
    )

    def validate(self):
        """Define a custom validate method in your Form:"""
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).values()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        if self.available_days.data not in dict(Days.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True
    


class SongForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    album = StringField(
        'album', validators=[Optional()]
    )

class AlbumForm(Form):
    name= StringField(
        'name', validators=[DataRequired()]
    )
