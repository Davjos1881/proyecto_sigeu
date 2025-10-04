from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.mysql import Base 

class ContrasenaModel(Base):
    __tablename__ = "contrasena"  

    id_contrasena = Column(Integer, primary_key=True, nullable=False)
    usuario_id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_creacion = Column(Date, nullable=False)
    fecha_ultimo_cambio = Column(Date, nullable=False)
    esta_vigente = Column(Boolean, nullable=False)

    # relación opcional con UsuarioModel; ajusta el nombre del modelo si tu clase de usuario se llama distinto
    usuario = relationship("UsuarioModel", back_populates="contrasenas")
