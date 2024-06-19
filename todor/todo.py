from flask import Blueprint, render_template, request, redirect, url_for, g
from todor.auth import login_required  # Importa el decorador login_required desde todor.auth
from .models import Todo, User         # Importa los modelos Todo y User desde .models (directorio actual)
from todor import db                  # Importa la instancia de SQLAlchemy llamada db desde todor

# Define un Blueprint llamado 'todo' con prefijo de URL '/todo'
bp = Blueprint('todo', __name__, url_prefix='/todo')

# Ruta para mostrar la lista de tareas
@bp.route('/list')
@login_required  # Aplica el decorador login_required para requerir autenticación
def index():
    todos = Todo.query.all()  # Consulta todas las tareas desde la base de datos
    return render_template('todo/index.html', todos=todos)  # Renderiza la plantilla 'todo/index.html' con las tareas

# Ruta para crear una nueva tarea
@bp.route('/create', methods=('GET', 'POST'))
@login_required  # Aplica el decorador login_required para requerir autenticación
def create():
    if request.method == 'POST':  # Si la solicitud es POST (envío de formulario)
        title = request.form['title']  # Obtiene el título de la tarea desde el formulario
        desc = request.form['desc']    # Obtiene la descripción de la tarea desde el formulario
        
        todo = Todo(g.user.id, title, desc)  # Crea una nueva instancia de Todo asignada al usuario actual
        
        db.session.add(todo)    # Agrega la nueva tarea a la sesión de la base de datos
        db.session.commit()     # Confirma los cambios en la base de datos
        
        return redirect(url_for('todo.index'))  # Redirecciona a la página principal de tareas
    
    return render_template('todo/create.html')  # Renderiza la plantilla 'todo/create.html' para mostrar el formulario de creación

# Función auxiliar para obtener una tarea por su ID
def get_todo(id):
    todo = Todo.query.get_or_404(id)  # Obtiene la tarea por su ID o devuelve un error 404 si no existe
    return todo

# Ruta para actualizar una tarea específica
@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required  # Aplica el decorador login_required para requerir autenticación
def update(id):
    todo = get_todo(id)  # Obtiene la tarea específica por su ID
    
    if request.method == 'POST':  # Si la solicitud es POST (envío de formulario)
        todo.title = request.form['title']  # Actualiza el título de la tarea desde el formulario
        todo.desc = request.form['desc']    # Actualiza la descripción de la tarea desde el formulario
        todo.state = True if request.form.get('state') == 'on' else False  # Actualiza el estado de la tarea
        
        db.session.commit()  # Confirma los cambios en la base de datos
        
        return redirect(url_for('todo.index'))  # Redirecciona a la página principal de tareas
    
    return render_template('todo/update.html', todo=todo)  # Renderiza la plantilla 'todo/update.html' para mostrar el formulario de actualización

# Ruta para eliminar una tarea específica
@bp.route('/delete/<int:id>')
@login_required  # Aplica el decorador login_required para requerir autenticación
def delete(id):
    todo = get_todo(id)  # Obtiene la tarea específica por su ID
    db.session.delete(todo)  # Elimina la tarea de la base de datos
    db.session.commit()  # Confirma los cambios en la base de datos
    
    return redirect(url_for('todo.index'))  # Redirecciona a la página principal de tareas después de eliminar la tarea
