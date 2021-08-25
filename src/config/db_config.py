# dependencies
from flask_sqlalchemy import SQLAlchemy

# create exportable database object that includes a thread-safe Flask_SQLAlchemy session
db = SQLAlchemy()