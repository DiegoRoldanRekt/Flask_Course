from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Función para conectar con la base de datos
def get_db_connection():
    conn = sqlite3.connect("Usuarios.db")  # Se conecta a tu base de datos
    conn.row_factory = sqlite3.Row  # Permite acceder a los datos como diccionario
    return conn

# Endpoint para obtener todos los hospitales
@app.route('/hospitales', methods=['GET'])
def get_hospitales():
    conn = get_db_connection()
    hospitales = conn.execute("SELECT * FROM hospitales").fetchall()
    conn.close()

    # Convertir los resultados a formato JSON
    return jsonify([
        {
            "Nhospital": hospital["Nhospital"],
            "Nombre": hospital["Nombre"],
            "Direccion": hospital["Direccion"],
            "Latitud": hospital["Latitud"],
            "Longitud": hospital["Longitud"]
        } 
        for hospital in hospitales
    ])

# Endpoint para obtener el hospital más cercano
@app.route('/hospital_cercano', methods=['GET'])
def get_hospital_cercano():
    try:
        # Obtener latitud y longitud desde los parámetros de la URL
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))

        conn = get_db_connection()
        hospital = conn.execute(
            """
            SELECT *, 
                ((Latitud - ?) * (Latitud - ?) + (Longitud - ?) * (Longitud - ?)) AS distancia
            FROM hospitales
            ORDER BY distancia ASC
            LIMIT 1;
            """,
            (lat, lat, lon, lon)
        ).fetchone()
        conn.close()

        # Si encontramos un hospital, devolver sus datos
        if hospital:
            return jsonify({
                "Nhospital": hospital["Nhospital"],
                "Nombre": hospital["Nombre"],
                "Direccion": hospital["Direccion"],
                "Latitud": hospital["Latitud"],
                "Longitud": hospital["Longitud"]
            })
        else:
            return jsonify({"error": "No se encontraron hospitales"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)