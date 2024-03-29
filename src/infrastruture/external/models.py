from src.infrastruture.external.base import Base
from sqlalchemy import  Column, Integer, String, Boolean, Date, DateTime

class DoktuzDB(Base):
    __tablename__ = "doktuz"
    codigo = Column(String(20), primary_key=True)
    fecha = Column(Date)
    empresa = Column(String(255))
    subcontrata = Column(String(255))
    proyecto = Column(String(128))
    t_exam = Column(String(128))
    paciente = Column(String(255))
    certificado = Column(String(2000))
    certificado_downloaded = Column(Boolean)
    imp = Column(String(2000))
    imp_downloaded = Column(Boolean)
    fecha_downloaded = Column(DateTime)
    #Defining One to Many relationships with the relationship function on the Parent Table
    #styles = relationship('ArchitecturalStyles', backref = 'points_of_interest',lazy=True,cascade="all, delete-orphan")
    #architects = relationship('Architects', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
    #categories = relationship('POICategories', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
    
    def __init__(self, codigo ,fecha, fecha_downloaded, empresa ,proyecto ,t_exam ,paciente, 
    certificado=None, imp=None, certificado_downloaded=False, imp_downloaded=False, subcontrata='-',):
        self.codigo = codigo
        self.fecha = fecha
        self.fecha_downloaded = fecha_downloaded
        self.empresa = empresa
        self.subcontrata = subcontrata
        self.proyecto = proyecto
        self.t_exam = t_exam
        self.paciente = paciente
        self.certificado = certificado
        self.certificado_downloaded = certificado_downloaded
        self.imp = imp
        self.imp_downloaded = imp_downloaded
    def __repr__(self):
        return f'Doktuz({self.empresa}, {self.paciente})'

    def __str__(self):
        return self.paciente