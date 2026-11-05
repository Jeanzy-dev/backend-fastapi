from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter
from app.repositories.reporte_repo import ReporteRepository

router = APIRouter(prefix="/api/reportes", tags=["Reportes y Tablero"])
repo = ReporteRepository()

@router.get("/resumen")
def resumen(desde: Optional[date] = None, hasta: Optional[date] = None):
    hasta = hasta or date.today()
    desde = desde or (hasta - timedelta(days=30))
    return repo.resumen(desde, hasta)
