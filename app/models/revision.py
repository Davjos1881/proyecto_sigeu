from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Revision(Base):
    __tablename__ = "revision"

    id_revision = Column(Integer, primary_key=True, autoincrement=True)
    id_evento = Column(Integer, ForeignKey("evento.id_evento"), nullable=False)
    id_secretario = Column(Integer, ForeignKey("secretario_academico.id_secretaria"), nullable=False)
    estado = Column(String(20), nullable=False, default="en espera")  # 'aprobado'|'rechazado'|'en espera'
    fecha_revision = Column(Date, nullable=True)
    justificacion = Column(Text, nullable=True)
    usuario_id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    evento = relationship("Evento", back_populates="revisiones")
    secretario = relationship("SecretarioAcademico")
    usuario = relationship("Usuario")