from flask import Flask, render_template, jsonify, request
import requests

# Configuramos Flask para que busque los HTML dentro de tu carpeta WEB
app = Flask(__name__, template_folder='WEB', static_folder='WEB')

# 1. Ruta para tu página principal (Home)
@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

# 2. Ruta para la página de la herramienta de IA
@app.route('/netflix_analyzer.html')
def analyzer_page():
    return render_template('netflix_analyzer.html')

# 3. El motor de la IA (¡AHORA CON POST Y MENÚ!)
@app.route('/analyze_script', methods=['POST'])
def analyze():
    url = "http://localhost:8008/answerDataQuestion"
    
    # 1. Recogemos qué opción ha elegido el usuario en la web
    user_data = request.json
    tipo_analisis = user_data.get("tipo_analisis")
    pregunta_libre = user_data.get("pregunta_libre", "") 
    
    # 2. Diccionario con nuestras Súper Preguntas
    preguntas = {
        "formato": "Actúa como un analista de datos. Analiza la tabla netflix_t y calcula la puntuación media exacta de la columna 'imdb_score' agrupando por la columna 'type' (es decir, comparando MOVIE contra SHOW). Recomiéndanos qué formato elegir basándote en cuál de los dos tiene el número más alto. Redacta la respuesta final en formato Markdown y ÚNICA y EXCLUSIVAMENTE en Español.",
        
        "expansion": "Actúa como un analista de negocios. Analiza la tabla netflix_t y dime cuáles son los 3 países (columna 'production_countries') con más títulos producidos, excluyendo a Estados Unidos ('US'). Basándote en esos 3 países, recomiéndanos dónde deberíamos abrir nuestro próximo estudio de grabación internacional. Redacta la respuesta en formato Markdown y ÚNICA y EXCLUSIVAMENTE en Español.",
        
        "calidad": "Actúa como un crítico de cine. Analiza la tabla netflix_t, agrupa por año de estreno ('release_year') y calcula la media de 'imdb_score' para los estrenos desde el año 2018 hasta el 2022. Analiza los resultados y dinos: ¿la calidad media de las producciones ha subido, ha bajado o se mantiene? Redacta la respuesta en formato Markdown y ÚNICA y EXCLUSIVAMENTE en Español."
    }
    
    # 3. Lógica de decisión: ¿Eligió una predefinida o la libre?
    if tipo_analisis == "libre":
        pregunta_final = pregunta_libre + " Responde en formato Markdown y exclusivamente en Español."
    else:
        pregunta_final = preguntas.get(tipo_analisis, preguntas["formato"])
    
    payload = {"question": pregunta_final}
    
    try:
        response = requests.post(url, json=payload, auth=('admin', 'admin'))
        data = response.json()
        ai_answer = data.get("answer", "No se pudo obtener una respuesta de la IA.")
        return jsonify({"recommendation": ai_answer})
    except Exception as e:
        return jsonify({"recommendation": f"Error de conexión con Denodo: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# python app.py