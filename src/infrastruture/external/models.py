from src.infrastruture.external.base import Base
from sqlalchemy import  Column, Integer, String, DateTime

class DoktuzDB(Base):
    __tablename__ = "doktuz"
    codigo = Column(String, primary_key=True)
    fecha = Column(DateTime)
    empresa = Column(String)
    subcontrata = Column(String)
    proyecto = Column(String)
    t_exam = Column(String)
    paciente = Column(String)
    imp = Column(String)
    #Defining One to Many relationships with the relationship function on the Parent Table
    #styles = relationship('ArchitecturalStyles', backref = 'points_of_interest',lazy=True,cascade="all, delete-orphan")
    #architects = relationship('Architects', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
    #categories = relationship('POICategories', backref = 'points_of_interest', lazy=True,cascade="all, delete-orphan")
    
    def __init__(self, codigo ,fecha ,empresa ,proyecto ,t_exam ,paciente ,imp, subcontrata='sin registro'):
        self.codigo = codigo
        self.fecha = fecha
        self.empresa = empresa
        self.subcontrata = subcontrata
        self.proyecto = proyecto
        self.t_exam = t_exam
        self.paciente = paciente
        self.imp = imp

    def __repr__(self):
        return f'Doktuz({self.empresa}, {self.paciente})'

    def __str__(self):
        return self.paciente