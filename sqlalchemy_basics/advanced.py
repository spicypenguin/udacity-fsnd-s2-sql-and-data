from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Person {self.id}, name: {self.name}>'


db.create_all()

names = [
    'Aaron',
    'Abdul',
    'Abe',
    'Abel',
    'Abraham',
    'Abram',
    'Adalberto',
    'Adam',
    'Adan',
    'Adolfo',
    'Adolph',
    'Adrian',
    'Agustin',
    'Ahmad',
    'Ahmed',
    'Al',
    'Alan',
    'Albert',
    'Alberto',
    'Alden',
    'Aldo',
    'Alec',
    'Alejandro',
    'Alex',
    'Alexander',
    'Alexis',
    'Alfonso',
    'Alfonzo',
    'Alfred',
    'Alfredo',
    'Ali',
    'Allan',
    'Allen',
    'Alonso',
    'Alonzo',
    'Alphonse',
    'Alphonso',
    'Alton',
    'Alva',
    'Alvaro',
    'Alvin',
    'Amado',
    'Ambrose',
    'Amos',
    'Anderson',
    'Andre',
    'Andrea',
    'Andreas',
    'Andres',
    'Andrew',
    'Andy',
    'Angel',
    'Angelo',
    'Anibal',
    'Anthony',
    'Antione',
    'Antoine',
    'Anton',
    'Antone',
    'Antonia',
    'Antonio',
    'Antony',
    'Antwan',
    'Archie',
    'Arden',
    'Ariel',
    'Arlen',
    'Arlie',
    'Armand',
    'Armando',
    'Arnold',
    'Arnoldo',
    'Arnulfo',
    'Aron',
    'Arron',
    'Art',
    'Arthur',
    'Arturo',
    'Asa',
    'Ashley',
    'Aubrey',
    'August',
    'Augustine',
    'Augustus',
    'Aurelio',
    'Austin',
    'Avery'
]

people = []
for name in names:
    people.append(Person(name=name))

db.session.add_all(people)
db.session.commit()

print(Person.query.filter(Person.name == 'Bob').all())
print(Person.query.filter(Person.name.like('%b%')).all())
print(Person.query.filter(Person.name.like('%b%')).limit(5).all())
print(Person.query.filter(Person.name.ilike('%b%')).all())
print(Person.query.filter(Person.name == 'Bob').count())

app.debug = True
app.run()
