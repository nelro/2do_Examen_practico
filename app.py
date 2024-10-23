from flask import Flask, session, request, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = 'nelro_123'


#generador de id unico
def generar_id():
    if 'productos' in session and len(session['productos']) > 0:
        return max(item['id'] for item in session['productos']) + 1
    else:
        return 1

# Página principal
@app.route('/')
def index():    
    productos = session.get('productos', [])
    return render_template('index.html',productos=productos)

# Ruta para agregar un nuevo producto
@app.route('/nuevo_producto', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        cantidad = int(request.form.get('cantidad'))
        precio = float(request.form.get('precio'))
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        categoria = request.form.get('categoria')

        # Crear un ID único
        id_producto = len(session.get('productos', [])) + 1

        # Crear el diccionario del producto
        nuevo_producto = {
            'id': generar_id(),
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        # Asegurarse de que la lista de productos exista en la sesión
        if 'productos' not in session:
            session['productos'] = []
        
        # Agregar el nuevo producto a la lista de productos en sesión
        session['productos'].append(nuevo_producto)
        session.modified = True

        # Redirigir a la lista de productos
        return redirect(url_for('index'))

    return render_template('nuevo_producto.html')


# ahora esta es la funcionde editar
@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    # capturar datos de la lsita de ssession
    list_edi_pro = session.get('productos', [])
    # buscamos el id del producto a editar
    producto_editar = next((item for item in list_edi_pro if item['id']==id),None)
    #comprovamos  si el producto existe
    if not  producto_editar:
        return redirect(url_for('index'))
    else:
        # si existe lo mostramos en el formulario
        if request.method == 'POST':
            # Obtener datos del formulario
            producto_editar['nombre']=request.form['nombre']
            producto_editar['cantidad']=request.form['cantidad']
            producto_editar['precio']=request.form['precio']
            producto_editar['fecha_vencimiento']=request.form['fecha_vencimiento']
            producto_editar['categoria']=request.form['categoria']
            #indicamos  que se ha modificado la sesion
            session.modified = True
            #redirigimos a la lista de productos donde sta la tabla
            return redirect(url_for('index'))
    
    return render_template('editar_producto.html', producto_editar=producto_editar)


#relaizamos ñla funcion par aelimar  un producto
@app.route('/eliminar_producto/<int:id>', methods=['GET'])
def eliminar_producto(id):
    # Asegurarse de que la lista de productos exista en la sesión
    if 'productos' not in session:
        session['productos'] = []
    # capturamos la  lista de productos
    eliminar_pro = session.get('productos',[])

    #realizamos el producto que se va a eliminar
    bus_producto_a_elim = next((item_pro for item_pro in eliminar_pro if item_pro['id'] == id),None)
    #dato_eliminar=next((item for item in datos_reg_seminario if item['id']== id),None)
    if bus_producto_a_elim:
        session['productos'].remove(bus_producto_a_elim)
    #indicamos que se realiuzo un amodificacion en session
    session.modified=True
    
    #nos dirigimos donde esta la tablas de los productos para mostrar la eliminacion
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
