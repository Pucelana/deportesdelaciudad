from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.recoletas import JornadaRecoletas, RecoletasPartido, RecoletasClub, PlayoffRecoletas, CopaRecoletas, SupercopaIbericaRecoletas, EuropaRecoletas

recoletas_route_bp = Blueprint('recoletas_route_bp', __name__)

# LIGA RECOLETAS ATL.VALLADOLID
# Crear el calendario Recoletas Atl.Valladolid