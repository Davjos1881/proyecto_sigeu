from sqlalchemy import Column, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base

class Notificacion(Base):
    __tablename__ = "notificacion"

    id_notificacion = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    evento_id_evento = Column(Integer, ForeignKey("evento.id_evento"), nullable=True)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(Date, nullable=True)

    evento = relationship("Evento", back_populates="notificaciones")
    usuario = relationship("Usuario", back_populates="notificaciones")