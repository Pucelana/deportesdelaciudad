from flask import Blueprint, render_template, redirect, url_for, flash, request

from app.extensions import db
from app.models.menu_competiciones import (
    SeccionConfig,
    CompeticionConfig,
)
from app.seo.menu_secciones import MENU_SECCIONES


menu_competiciones_bp = Blueprint(
    "menu_competiciones",
    __name__,
)


# ==========================================================
# NOMBRES QUE SE MOSTRARÁN EN EL ADMIN
# ==========================================================

NOMBRES_SECCIONES = {
    "uemc": "UEMC Valladolid",
    "ponce": "Pucela Basket",
    "cdsi_vall": "CDSI Valladolid",
    "vcv": "Universidad VCV",
    "san_jose": "CD San José",
    "aliados": "BSR Valladolid",
    "aula": "Aula Valladolid",
    "recoletas": "Atl. Valladolid",
    "valladolid": "Real Valladolid",
    "valladoliDi": "Real ValladoliDi",
    "promesas": "RV Promesas",
    "caja": "CPLV Caja Rural",
    "panteras": "CPLV Panteras C.R",
    "vrac": "VRAC",
    "salvador": "El Salvador",
    "salvador_fem": "El Salvador Femenino",
    "rv_fem": "RV Femenino",
    "parquesol": "CD Parquesol",
    "galvan": "CD Tierno Galván",
    "vall_sala": "Valladolid S.S",
}


# ==========================================================
# SINCRONIZAR MENU_SECCIONES CON LA BASE DE DATOS
# ==========================================================

def sincronizar_menu_competiciones():

    cambios = False

    for nombre_seccion, competiciones in MENU_SECCIONES.items():

        # --------------------------------------------------
        # BUSCAR SECCIÓN
        # --------------------------------------------------

        seccion = SeccionConfig.query.filter_by(
            nombre=nombre_seccion
        ).first()

        # --------------------------------------------------
        # SI NO EXISTE, CREARLA
        # --------------------------------------------------

        if not seccion:

            seccion = SeccionConfig(
                nombre=nombre_seccion,
                activa=True,
            )

            db.session.add(seccion)

            # Necesitamos el ID antes de crear
            # las competiciones relacionadas.
            db.session.flush()

            cambios = True

        # --------------------------------------------------
        # CREAR COMPETICIONES QUE NO EXISTAN
        # --------------------------------------------------

        for nombre_competicion, activa in competiciones.items():

            competicion = CompeticionConfig.query.filter_by(
                seccion_id=seccion.id,
                nombre=nombre_competicion,
            ).first()

            if not competicion:

                competicion = CompeticionConfig(
                    seccion_id=seccion.id,
                    nombre=nombre_competicion,
                    activa=activa,
                )

                db.session.add(competicion)

                cambios = True

    # ------------------------------------------------------
    # GUARDAR CAMBIOS
    # ------------------------------------------------------

    if cambios:
        db.session.commit()


# ==========================================================
# ADMINISTRAR SECCIONES Y COMPETICIONES
# ==========================================================

@menu_competiciones_bp.route("/admin/menu_competiciones", methods=["GET", "POST"],)
def menu_competiciones():

    # ASEGURAR QUE EXISTEN LOS DATOS INICIALES

    sincronizar_menu_competiciones()

    # GUARDAR CAMBIOS

    if request.method == "POST":

        # ==================================================
        # SECCIONES ACTIVAS
        # ==================================================

        secciones_activas = {
            int(seccion_id)
            for seccion_id in request.form.getlist(
                "secciones_activas"
            )
        }

        secciones = SeccionConfig.query.all()

        for seccion in secciones:

            seccion.activa = (
                seccion.id in secciones_activas
            )

        # ==================================================
        # COMPETICIONES ACTIVAS
        # ==================================================

        competiciones_activas = {
            int(competicion_id)
            for competicion_id in request.form.getlist(
                "competiciones_activas"
            )
        }

        competiciones = CompeticionConfig.query.all()

        for competicion in competiciones:

            competicion.activa = (
                competicion.id in competiciones_activas
            )

        # ==================================================
        # GUARDAR EN BASE DE DATOS
        # ==================================================

        db.session.commit()

        flash(
            "Menú de secciones y competiciones actualizado correctamente.",
            "success",
        )

        return redirect(
            url_for(
                "menu_competiciones.menu_competiciones"
            )
        )

    # ------------------------------------------------------
    # MOSTRAR ADMINISTRACIÓN
    # ------------------------------------------------------

    secciones = SeccionConfig.query.order_by(
        SeccionConfig.nombre.asc()
    ).all()

    return render_template(
        "admin/menu_competiciones.html",
        secciones=secciones,
        nombres_secciones=NOMBRES_SECCIONES,
    )