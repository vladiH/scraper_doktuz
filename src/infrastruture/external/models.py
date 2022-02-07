from src.infrastruture.external.base import Base
from sqlalchemy import  Column, Integer, String, DateTime, Boolean

class DoktuzDB(Base):
    __tablename__ = "doktuz"
    codigo = Column(String, primary_key=True)
    fecha = Column(DateTime)
    empresa = Column(String)
    subcontrata = Column(String)
    proyecto = Column(String)
    t_exam = Column(String)
    paciente = Column(String)
    certificado = Column(String)
    certificado_downloaded = Column(Boolean)
    imp = Column(String)
    imp_downloaded = Column(Boolean)
    #Defining One to Many relationships with the relationship function on the Parent Table
    #styles = relationship('ArchitecturalStyles', backref = 'points_of_interest',lazy=True,cascade="all, delete-orphan")
    #architects = relationship('Architects', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
    #categories = relationship('POICategories', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
    
    def __init__(self, codigo ,fecha ,empresa ,proyecto ,t_exam ,paciente, 
    certificado, certificado_downloaded,imp, imp_downloaded=False, subcontrata='sin registro'):
        self.codigo = codigo
        self.fecha = fecha
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