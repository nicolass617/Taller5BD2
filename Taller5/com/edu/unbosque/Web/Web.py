from flask import Flask, render_template, request, redirect, jsonify, g, session
from com.edu.unbosque.model import model as model

app = Flask(__name__)
app.secret_key = "1234"
mascotasList = []
fotos = []
top = []

@app.route('/inicio')
def inicio():
    return render_template('Inicio.html')

@app.route('/Ingresar', methods=['GET', 'POST'])
def ingresar():
    if request.method == 'GET':
        return render_template('Ingreso.html')
    else:
        username = request.form['username']
        usr = model.validarUser(username)
        if usr != "None":
            session['user'] = username
            return redirect("/Mascotas")
        else:
            return redirect("/Registrarse")


@app.route('/Registrarse', methods=['GET', 'POST'])
def registro():
    language = request.args.get('language')
    if request.method == 'GET':
        return render_template('Registro.html')
    else:
        username = request.form['username']
        usr = model.validarUser(username)
        if usr == "None":
            model.crearPersona(username)
            return render_template('Ingreso.html')
        else:
            return '''<form action="/Registrarse">
                                <h3>El nombre de usuario ya existe, intente con otro</h3>
                                <button class="btn btn-lg btn-primary" style="background:gray; color:white" type="submit">Ok</button>
                            </form>'''.format(language)

@app.route('/Mascotas')
def mascotas():
    usr = session['user']
    list = model.petUser(usr)
    if list != 'None':
        for i in list:
            if i['name'] not in mascotasList:
                mascotasList.append(i['name'])
    return render_template("Mascota.html", mascotas=mascotasList)

@app.route('/RegistrarMascota', methods=['GET', 'POST'])
def regMascota():
    if request.method == 'GET':
        return render_template("RegMascota.html")
    else:
        usr = session['user']
        nombre = request.form['nombre']
        especie = request.form['especie']
        foto = request.form['foto']
        model.crearMascota(usr, nombre, especie)
        model.taggearFoto1(nombre, foto)
        list = model.petUser(usr)
        if(list != "None"):
            for m in list:
                if m['name'] not in mascotasList:
                    mascotasList.append(m['name'])
        return redirect('/Mascotas')

@app.route('/Publicaciones', methods=['GET', 'POST'])
def publicaciones():
    if request.method == 'GET':
        list = model.fotos()
        if list != 'None':
            for i in list:
                if i['foto'] not in fotos:
                    fotos.append(i['foto'])
        return render_template("Publicaciones.html", fotos=fotos)
    else:
        usr = session['user']
        url = request.form['id']
        print(url)
        model.like(usr, url)
        return redirect("/Publicaciones")

@app.route('/TopFotos')
def topfotos():
    top.clear()
    list = model.countLikes()
    l = []
    if list != None:
        for i in list:
            l.append(i)
        tam = len(l)
        if tam > 3:
            tam = 3
        for i in range(tam):
            if l[i] not in top:
                top.append(l[i])
    return render_template('TopFotos.html', tops=top)

@app.route('/cerrarSecion')
def cerrarSecion():
    if 'user' in session:
        pass
    mascotasList.clear()
    fotos.clear()
    top.clear()
    return redirect('/inicio')

if __name__ == '__main__':
    app.add_url_rule("/", endpoint="inicio")
    app.run(debug=True, host="localhost", port="8080")