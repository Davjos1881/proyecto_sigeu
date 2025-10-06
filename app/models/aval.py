from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base
from app.models.unidad_academica import UnidadAcademica

class AvalEvento(Base):
    __tablename__ = "aval_evento"

    id_aval = Column(Integer, primary_key=True, autoincrement=True)
    evento_id_evento = Column(Integer, ForeignKey("evento.id_evento"), nullable=False)
    id_unidad = Column(Integer, ForeignKey("unidad_academica.id_unidad"), nullable=False)
    usuario_id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    nombre_responsable = Column(String(100), nullable=False)
    rol_responsable = Column(String(20), nullable=False)  # 'estudiante'|'docente'
    fecha_emision = Column(Date, nullable=True)
    emitido_por = Column(String(100), nullable=True)

    evento = relationship("Evento", back_populates="avales")
    unidad = relationship("UnidadAcademica")
    usuario = relationship("Usuario")