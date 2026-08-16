from app.extensions import db
from app.models.menu_competiciones import (
    SeccionConfig,
    CompeticionConfig,
)
from app.seo.menu_secciones import MENU_SECCIONES


def sincronizar_menu_competiciones():
    """
    Sincroniza MENU_SECCIONES con la base de datos.

    - Crea las secciones que no existan.
    - Crea las competiciones que no existan.
    - Respeta los estados actuales de la base de datos.
    - NO modifica una competición que ya exista.
    - NO elimina secciones ni competiciones de la base de datos.
    """

    nuevas_secciones = 0
    nuevas_competiciones = 0

    try:

        for nombre_seccion, competiciones in MENU_SECCIONES.items():

            # ---------------------------------------------------------
            # 1. BUSCAR LA SECCIÓN
            # ---------------------------------------------------------

            seccion = SeccionConfig.query.filter_by(
                nombre=nombre_seccion
            ).first()

            # ---------------------------------------------------------
            # 2. CREAR LA SECCIÓN SI NO EXISTE
            # ---------------------------------------------------------

            if not seccion:

                seccion = SeccionConfig(
                    nombre=nombre_seccion,
                    activa=True,
                )

                db.session.add(seccion)
                db.session.flush()

                nuevas_secciones += 1

                print(
                    f"[MENU] Nueva sección creada: "
                    f"{nombre_seccion}"
                )

            else:

                print(
                    f"[MENU] Sección encontrada: "
                    f"{nombre_seccion}"
                )

            # ---------------------------------------------------------
            # 3. RECORRER LAS COMPETICIONES
            # ---------------------------------------------------------

            for nombre_competicion, estado_inicial in competiciones.items():

                competicion = CompeticionConfig.query.filter_by(
                    seccion_id=seccion.id,
                    nombre=nombre_competicion,
                ).first()

                # -----------------------------------------------------
                # 4. CREAR SOLO LAS COMPETICIONES NUEVAS
                # -----------------------------------------------------

                if not competicion:

                    competicion = CompeticionConfig(
                        seccion_id=seccion.id,
                        nombre=nombre_competicion,
                        activa=estado_inicial,
                    )

                    db.session.add(competicion)

                    nuevas_competiciones += 1

                    print(
                        f"[MENU] Nueva competición creada: "
                        f"{nombre_seccion} → "
                        f"{nombre_competicion} "
                        f"(activa={estado_inicial})"
                    )

                else:

                    # IMPORTANTE:
                    # No modificamos competiciones existentes.
                    print(
                        f"[MENU] Competición existente: "
                        f"{nombre_seccion} → "
                        f"{nombre_competicion} "
                        f"(activa={competicion.activa})"
                    )

        # -------------------------------------------------------------
        # 5. GUARDAR LOS CAMBIOS
        # -------------------------------------------------------------

        db.session.commit()

        print(
            "[MENU] Sincronización completada. "
            f"Secciones nuevas: {nuevas_secciones}. "
            f"Competiciones nuevas: {nuevas_competiciones}."
        )

    except Exception as e:

        # Si ocurre cualquier problema, deshacemos los cambios
        # realizados durante esta sincronización.
        db.session.rollback()

        print(
            f"[MENU] ERROR durante la sincronización: {e}"
        )

        raise