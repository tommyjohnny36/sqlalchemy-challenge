# Use SQLAlchemy `create_engine` to connect to your sqlite database.

# * Use SQLAlchemy `automap_base()` to reflect your tables into classes
#  and save a reference to those classes called `Station` and `Measurement`.

# * Link Python to the database by creating an SQLAlchemy session.

# * **Important** Don't forget to close out your session at the end of your notebook.

# SQL Alchemy
from sqlalchemy import create_engine
# Pandas
import pandas as pd

database_path = "../Resources/hawaii.sqlite"

# Create Engine
engine = create_engine(f"sqlite:///{database_path}")
conn = engine.connect()

# Query All Records in the the Census Table
hawaii_data = pd.read_sql("SELECT * FROM hawaii", conn)



# Define the Surfer Class
# class Surfer():

#   # Initialize the Surfer constructor 
#   def __init__(self, name, hometown, rank):
#       self.name = name + " " + "Dude"
#       self.hometown = hometown + " " + "Waves"
#       self.rank = rank






