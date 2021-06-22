import csv, datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Time, Sequence
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import exists


Base = declarative_base()

class Curso(Base):
    __tablename__ = 'curso'

    id = Column(Integer,Sequence('curso_id_seq'), primary_key=True)
    name = Column(String)

    alumnos = relationship('Alumno', order_by ='Alumno.id', back_populates='curso')
    horarios_cursos = relationship('Horario', order_by ='Horario.h_ent', back_populates='curso')
    

    def __repr__(self):
        return "{}".format(self.name)

class Alumno (Base):
    __tablename__ = 'alumno'

    id = Column(Integer,Sequence('alumno_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    curso_id = Column(Integer, ForeignKey('curso.id'))

    curso = relationship('Curso', back_populates='alumnos')


    def __repr__(self):
        return "{}, {}".format(self.lastname, self.firstname)

class Profesor(Base):
    __tablename__ = 'profesor'

    id = Column(Integer,Sequence('profesor_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    horarios_profesor = relationship('Horario', order_by ='Horario.h_ent', back_populates='profesor')

    def __repr__(self):
        return "{}, {}".format(self.lastname, self.firstname)

class Horario(Base):
    __tablename__ = 'horario'

    id = Column(Integer,Sequence('horario_id_seq'), primary_key=True)
    dia = Column(Integer)
    h_ent = Column(Time)
    h_salida = Column(Time)

    curso_id = Column(Integer, ForeignKey('curso.id'))
    profesor_id = Column(Integer, ForeignKey('profesor.id'))

    curso = relationship('Curso', back_populates='horarios_cursos')
    profesor = relationship('Profesor', back_populates='horarios_profesor')

    def __repr__(self):
        return "{}, {}".format(self.lastname, self.firstname)



class ReporteDeCurso(object):

    def __init__(self, path):
        self.path = path

    def reporte(self, curso):
        alumnos = curso.alumnos
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for alumno in alumnos:
                writer.writerow([str(alumno)])

class ReporteDeHorarios(object):

    def __init__(self, path):
        self.path = path

    def reporte(self, curso):
        horarios = curso.horarios_cursos
        with open(self.path,'w') as a_file:
            writer = csv.writer(a_file)
            for horario in horarios:
                writer.writerow(['Dia: ' + str(horario.dia) + '\nHora ingreso: ' + str(horario.h_ent) + '\nHora salida: '+str(horario.h_salida) +'\nProfesor: ' + str(horario.profesor)])

class ReporteDeProfesor(object):
    
    def __init__(self, path):
        self.path = path

    def reporte(self, profesor):
        profesores = profesor.horarios_profesor
        with open(self.path,'w') as a_file:
            writer = csv.writer(a_file)
            for profesor in profesores:
                writer.writerow(['Dia: ' + str(profesor.dia) + '\nHora Ingreso: ' + str(profesor.h_ent) + '\nHora Salida: ' + str(profesor.h_salida) + '\nCurso: ' + profesor.curso.name])

def main(*args, **kwargs):
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    cursoA = Curso(name='1')
    cursoB = Curso(name='2')

    estudianteA = Alumno(firstname='Juan',lastname='Perez', curso=cursoA)
    estudianteB = Alumno(firstname='Cintia',lastname='Rodriguez', curso=cursoA)
    estudianteC = Alumno(firstname='Pedro',lastname='Caballero', curso=cursoA)
    estudianteD = Alumno(firstname='Rodrigo',lastname='Videla', curso=cursoB)
    estudianteE = Alumno(firstname='Guido',lastname='Martinez', curso=cursoB)
    estudianteF = Alumno(firstname='Marcelo',lastname='Torres', curso=cursoB)

    profesorA = Profesor(firstname = 'Ramon',lastname="Cabrera")
    profesorB = Profesor(firstname = 'Silvio',lastname="Romero")
    
    aux = datetime.time(8, 0, 0)
    aux2 = datetime.time(10, 0, 0)
    aux3 = datetime.time(12, 0, 0)

    horarioA = Horario(dia=1, h_ent=aux, h_salida=aux2, curso=cursoA, profesor=profesorA)
    horarioB = Horario(dia=2, h_ent=aux2, h_salida=aux3, curso=cursoB, profesor=profesorB)
    horarioC = Horario(dia=1, h_ent=aux, h_salida=aux2, curso=cursoB, profesor=profesorA)
    horarioD = Horario(dia=2, h_ent=aux2, h_salida=aux3, curso=cursoA, profesor=profesorB)

    session.add(cursoA)
    session.add(cursoB)

    session.add(estudianteA)
    session.add(estudianteB)
    session.add(estudianteC)
    session.add(estudianteD)
    session.add(estudianteE)
    session.add(estudianteF)

    session.add(profesorA)
    session.add(profesorB)

    session.add(horarioA)
    session.add(horarioB)
    session.add(horarioC)
    session.add(horarioD)

    session.commit()

    ReporteDeCurso('Curso_{}.csv'.format(cursoA.name)).reporte(cursoA)
    ReporteDeCurso('Curso_{}.csv'.format(cursoB.name)).reporte(cursoB)

    ReporteDeHorarios('Horarios_curso_{}.csv'.format(cursoA.name)).reporte(cursoA)
    ReporteDeHorarios('Horarios_curso_{}.csv'.format(cursoB.name)).reporte(cursoB)

    ReporteDeProfesor('Horarios_prof_{}.csv'.format(profesorA)).reporte(profesorA)
    ReporteDeProfesor('Horarios_prof_{}.csv'.format(profesorB)).reporte(profesorB)

if __name__ == "__main__":
    main()