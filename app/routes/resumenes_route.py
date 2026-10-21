from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from datetime import date
from collections import defaultdict
from collections import OrderedDict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.resumenes import ResumenJornada

resumenes_route_bp = Blueprint("resumenes_route_bp", __name__)

@resumenes_route_bp.route("/admin/crear_resumen_jornada", methods=["GET", "POST"])
def crear_resumen_jornada():
    if request.method == "POST":
        try:
            resumen = ResumenJornada(
                deporte=request.form["deporte"].strip(),
                equipo=request.form["equipo"].strip(),
                competicion=request.form.get("competicion", "").strip() or None,
                temporada=request.form.get("temporada", "").strip() or None,
                jornada=request.form.get("jornada", "").strip() or None,
                fecha=date.fromisoformat(request.form["fecha"]),
                fecha_inicio=date.fromisoformat(request.form["fecha_inicio"]),
                fecha_fin=date.fromisoformat(request.form["fecha_fin"]),
                rival=request.form.get("rival", "").strip() or None,
                resultado=request.form.get("resultado", "").strip() or None,
                titular=request.form["titular"].strip(),
                contenido=request.form["contenido"].strip(),
                publicado=request.form.get("publicado") == "on",
            )

            if not resumen.deporte or not resumen.equipo:
                raise ValueError("El deporte y el equipo son obligatorios.")

            if not resumen.titular or not resumen.contenido:
                raise ValueError("El titular y el contenido son obligatorios.")
            if resumen.fecha_inicio > resumen.fecha_fin:
                raise ValueError("El inicio del periodo no puede ser posterior al final.")
            if not (resumen.fecha_inicio <= resumen.fecha <= resumen.fecha_fin):
                raise ValueError("La fecha del partido debe estar dentro del periodo seleccionado.")

            db.session.add(resumen)
            db.session.commit()

            return redirect(url_for("resumenes_route_bp.ver_resumenes_admin"))

        except (ValueError, KeyError):
            db.session.rollback()

    return render_template(
        "admin/resumenes/resumen_jornada.html",
        resumen=None,
        accion="Crear"
    )

@resumenes_route_bp.route("/admin/resumenes_jornada")
def ver_resumenes_admin():
    fecha_filtro = request.args.get("fecha", "").strip()
    deporte_filtro = request.args.get("deporte", "").strip()
    equipo_filtro = request.args.get("equipo", "").strip()

    consulta = ResumenJornada.query

    if fecha_filtro:
        try:
            consulta = consulta.filter(
                ResumenJornada.fecha == date.fromisoformat(fecha_filtro)
            )
        except ValueError:
            flash("La fecha del filtro no es válida.", "warning")

    if deporte_filtro:
        consulta = consulta.filter_by(deporte=deporte_filtro)

    if equipo_filtro:
        consulta = consulta.filter_by(equipo=equipo_filtro)

    resumenes = consulta.order_by(
        ResumenJornada.fecha.desc(),
        ResumenJornada.id.desc()
    ).all()

    return render_template(
        "admin/resumenes/lista_resumenes.html",
        resumenes=resumenes,
        fecha_filtro=fecha_filtro,
        deporte_filtro=deporte_filtro,
        equipo_filtro=equipo_filtro
    )


@resumenes_route_bp.route("/admin/modificar_resumen_jornada/<int:id>",methods=["GET", "POST"])
def modificar_resumen_jornada(id):
    resumen = db.session.get(ResumenJornada, id)

    if resumen is None:
        flash("No se ha encontrado ese resumen.", "warning")
        return redirect(url_for("resumenes_route_bp.ver_resumenes_admin"))

    if request.method == "POST":
        try:
            resumen.deporte = request.form["deporte"].strip()
            resumen.equipo = request.form["equipo"].strip()
            resumen.competicion = request.form.get("competicion", "").strip() or None
            resumen.temporada = request.form.get("temporada", "").strip() or None
            resumen.jornada = request.form.get("jornada", "").strip() or None
            resumen.fecha = date.fromisoformat(request.form["fecha"])
            resumen.fecha_inicio = date.fromisoformat(request.form["fecha_inicio"])
            resumen.fecha_fin = date.fromisoformat(request.form["fecha_fin"])

            if resumen.fecha_inicio > resumen.fecha_fin:
                raise ValueError("El inicio del periodo no puede ser posterior al final.")
 
            if not (resumen.fecha_inicio <= resumen.fecha <= resumen.fecha_fin):
                raise ValueError("La fecha del partido debe estar dentro del periodo seleccionado.")
            
            resumen.rival = request.form.get("rival", "").strip() or None
            resumen.resultado = request.form.get("resultado", "").strip() or None
            resumen.titular = request.form["titular"].strip()
            resumen.contenido = request.form["contenido"].strip()
            resumen.publicado = request.form.get("publicado") == "on"

            if not resumen.deporte or not resumen.equipo:
                raise ValueError("El deporte y el equipo son obligatorios.")

            if not resumen.titular or not resumen.contenido:
                raise ValueError("El titular y el contenido son obligatorios.")

            db.session.commit()
            return redirect(url_for("resumenes_route_bp.ver_resumenes_admin"))

        except (ValueError, KeyError):
            db.session.rollback()

    return render_template(
        "admin/resumenes/resumen_jornada.html",
        resumen=resumen,
        accion="Modificar"
    )

@resumenes_route_bp.route("/admin/eliminar_resumen_jornada/<int:id>",methods=["POST"])
def eliminar_resumen_jornada(id):
    resumen = db.session.get(ResumenJornada, id)

    if resumen is None:
        flash("No se ha encontrado ese resumen.", "warning")
    else:
        db.session.delete(resumen)
        db.session.commit()
        flash("Resumen eliminado correctamente.", "success")

    return redirect(url_for("resumenes_route_bp.ver_resumenes_admin"))

@resumenes_route_bp.route("/resumenes")
@resumenes_route_bp.route("/resumenes/<fecha>")
def pagina_resumenes(fecha=None):

    # Obtener los periodos disponibles.
    # Para los registros antiguos sin periodo, usar su fecha de partido.
    periodos = db.session.query(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).label("inicio"),
        db.func.coalesce(
            ResumenJornada.fecha_fin,
            ResumenJornada.fecha
        ).label("fin")
    ).filter(
        ResumenJornada.publicado.is_(True)
    ).distinct().order_by(
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ).desc(),
        db.func.coalesce(
            ResumenJornada.fecha_fin,
            ResumenJornada.fecha
        ).desc()
    ).all()

    if not periodos:
        return render_template(
            "resumen/resumenes.html",
            fecha_seleccionada=None,
            fecha_fin_seleccionada=None,
            fechas_disponibles=[],
            resumenes_por_deporte={}
        )

    # La URL identifica el periodo mediante su fecha de inicio.
    if fecha is None:
        indice_fecha = 0
    else:
        try:
            fecha_solicitada = date.fromisoformat(fecha)
        except ValueError:
            return redirect(
                url_for("resumenes_route_bp.pagina_resumenes")
            )

        indice_fecha = next(
            (
                i for i, periodo in enumerate(periodos)
                if periodo.inicio == fecha_solicitada
            ),
            None
        )

        if indice_fecha is None:
            return redirect(
                url_for("resumenes_route_bp.pagina_resumenes")
            )

    fecha_seleccionada = periodos[indice_fecha].inicio
    fecha_fin_seleccionada = periodos[indice_fecha].fin

    # Cargar todos los resúmenes del periodo seleccionado.
    resumenes = ResumenJornada.query.filter(
        ResumenJornada.publicado.is_(True),
        db.func.coalesce(
            ResumenJornada.fecha_inicio,
            ResumenJornada.fecha
        ) == fecha_seleccionada,
        db.func.coalesce(
            ResumenJornada.fecha_fin,
            ResumenJornada.fecha
        ) == fecha_fin_seleccionada
    ).order_by(
        ResumenJornada.deporte,
        ResumenJornada.fecha,
        ResumenJornada.equipo
    ).all()

    # Agrupar por deporte, no por fecha de partido.
    resumenes_por_deporte = {}

    for resumen in resumenes:
        resumenes_por_deporte.setdefault(
            resumen.deporte, []
        ).append(resumen)

    # Navegación entre periodos.
    fecha_siguiente = (
        periodos[indice_fecha - 1].inicio
        if indice_fecha > 0 else None
    )

    fecha_anterior = (
        periodos[indice_fecha + 1].inicio
        if indice_fecha < len(periodos) - 1 else None
    )

    fechas_disponibles = [
        periodo.inicio for periodo in periodos
    ]

    return render_template(
        "resumen/resumenes.html",
        fecha_seleccionada=fecha_seleccionada,
        fecha_fin_seleccionada=fecha_fin_seleccionada,
        fechas_disponibles=fechas_disponibles,
        resumenes_por_deporte=resumenes_por_deporte,
        fecha_anterior=fecha_anterior,
        fecha_siguiente=fecha_siguiente,
        periodos_disponibles=periodos
    )
