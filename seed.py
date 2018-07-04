from app.models.Country import Country
from app.Blueprints import db

c = Country(code = 'IND', name = 'India')
db.session.add(c)
c = Country(code = 'USA', name = 'America')
db.session.add(c)
c = Country(code = 'CAN', name = 'Canada')
db.session.add(c)
c = Country(code = 'AUS', name = 'Australia')
db.session.add(c)
c = Country(code = 'GER', name = 'Germany')
db.session.add(c)
db.session.commit()


