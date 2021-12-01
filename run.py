from myapp import myapp_obj
from myapp import db
db.create_all()
myapp_obj.run(debug = True)
