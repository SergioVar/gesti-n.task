from todor import db

# Definición del modelo de usuario
class User(db.Model):
    # Atributos de la tabla 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    # Constructor para inicializar un nuevo usuario
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    # Método para representar el objeto como una cadena
    def __repr__(self):
        return f'<User: {self.username}>'

# Definición del modelo de tarea
class Todo(db.Model):
    # Atributos de la tabla 'todo'
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)
    state = db.Column(db.Boolean, default=False)
    
    # Constructor para inicializar una nueva tarea
    def __init__(self, created_by, title, desc, state=False):
        self.created_by = created_by
        self.title = title
        self.desc = desc
        self.state = state
        
    # Método para representar el objeto como una cadena
    def __repr__(self):
        return f'<Todo: {self.title}>'
