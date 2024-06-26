import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)


from .router import Router
from .database import DataBase
from .hashingpassword import Hashing