from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos Modelo
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    return render_template('new.html', user=user)

@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')
    
    #Validación de Receta
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')
    
    #Guardamos la receta
    Recipe.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    # queremos la instancia de la receta que se quiere desplegar en editar en base a su identificador que se recibe en la URL
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta) #objeto de receta que deseo enviar a recipe

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    #Verificar que haya iniciado sesion
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #recibimos formulario = request.form 
    #request.form = {name: "Albondigas", description:"123"....... recipe_id:1}

    #Verificar que todos los datos esten correctos
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id']) #/edit/recipe/1

    #Guardar los cambios
    Recipe.update(request.form)

    #Redireccionar a /dashboard
    return redirect('/dashboard')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    #Verificar que haya iniciado sesion
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Borramos
    formulario = {"id": id}
    Recipe.delete(formulario)

    #Redirigir a /dashboard
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Saber cuál es el nombre del usuario que inicio sesión
    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #Objeto receta que queremos desplegar
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    #Renderizar show_recipe.html
    return render_template('show_recipe.html', user=user, recipe=recipe)
