from flask import Blueprint

timetable_mod = Blueprint('timetable', __name__)

from blueprints.timetables.routings_timetables import *
from blueprints.timetables.routings_timetables_templates import *