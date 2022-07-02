import enum
from wtforms.validators import ValidationError

class Genre(enum.Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    Hip_Hop = 'Hip-Hop'
    Heavy_Metal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    R_B = 'R&B'
    Reggae = 'Reggae'
    Rock_Roll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
    
    @classmethod
    def coerce_for_enum(self):
        def coerce(name):
            if isinstance(name, self):
                return name.value
            try:
                return self[name].value
            except KeyError:
                raise ValidationError(name)
        return coerce

class State(enum.Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def coerce_for_enum(self):
        def coerce(name):
            if isinstance(name, self):
                return name.value
            try:
                return self[name].value
            except KeyError:
                raise ValidationError(name)
        return coerce

class Days(enum.Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

    @classmethod
    def choices(cls):
        return [(choice.name) for choice in cls]
    
    @classmethod
    def coerce_for_enum(self):
        def coerce(name):
            if isinstance(name, self):
                return name.value
            try:
                return self[name].value
            except KeyError:
                raise ValidationError(name)
        return coerce




# def coerce_for_enum(enum):
#     def coerce(name):
#         if isinstance(name, enum):
#             return name.value
#         try:
#             return enum[name].value
#         except KeyError:
#             raise ValidationError(name)
#     return coerce