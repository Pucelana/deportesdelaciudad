from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.caja import JornadaCaja, CajaPartido, CajaClub, PlayoffCaja, CopaCaja, SupercopaCaja, EuropaCaja

caja_route_bp = Blueprint('caja_route_bp', __name__)