import re
import random
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        self.context = {}

    def get_response(self, user_input):
        split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
        response = self.check_all_messages(split_message)
        return response

    def message_probability(self, user_message, recognized_words, single_response=False, required_word=[]):
        message_certainty = 0
        has_required_words = True

        for word in user_message:
            if word in recognized_words:
                message_certainty += 1

        percentage = float(message_certainty) / float(len(recognized_words))

        for word in required_word:
            if word not in user_message:
                has_required_words = False
                break

        if has_required_words or single_response:
            return int(percentage * 100)
        else:
            return 0

    def check_all_messages(self, message):
        highest_prob = {}

        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            nonlocal highest_prob
            highest_prob[bot_response] = self.message_probability(message, list_of_words, single_response, required_words)

        # Time-based greetings
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = 'Buenos días'
        elif 12 <= current_hour < 18:
            greeting = 'Buenas tardes'
        else:
            greeting = 'Buenas noches'

        response(f'{greeting}! ¿Cómo puedo ayudarte hoy?', ['hola', 'klk', 'saludos', 'buenas'], single_response=True)

        # Basic responses
        response('Estoy bien, ¿y tú?', ['cómo', 'estás', 'va', 'vas', 'sientes'], required_words=['cómo'])
        response('Estamos ubicados en la calle 23 número 123.', ['ubicados', 'dirección', 'dónde', 'ubicación'], single_response=True)
        response('Siempre a la orden.', ['gracias', 'te lo agradezco', 'thanks'], single_response=True)

        # Extended responses
        response('El clima está soleado y agradable.', ['cómo', 'está', 'clima', 'tiempo', 'hoy'], required_words=['clima'])
        response('Mi color favorito es el azul. ¿Cuál es el tuyo?', ['cuál', 'es', 'tu', 'color', 'favorito'], required_words=['color'])
        response('Me gusta la pizza, ¿y a ti?', ['qué', 'te', 'gusta', 'comer'], required_words=['gusta'])
        response('Trabajo como asistente virtual. ¿En qué trabajas tú?', ['a', 'qué', 'te', 'dedicas', 'trabajas'], required_words=['trabajas'])

        # New responses
        response('Me encanta jugar al fútbol. ¿Y a ti?', ['qué', 'te', 'gusta', 'hacer', 'hobbies', 'pasatiempos'], required_words=['gusta', 'hacer'])
        response('Mi película favorita es Inception. ¿Cuál es la tuya?', ['cuál', 'es', 'tu', 'película', 'favorita'], required_words=['película'])
        response('Prefiero los gatos. ¿Tienes mascotas?', ['prefieres', 'perros', 'gatos', 'mascotas'], required_words=['mascotas'])
        response('La inteligencia artificial es un campo fascinante. ¿Qué piensas sobre la tecnología?', ['qué', 'piensas', 'sobre', 'tecnología'], required_words=['tecnología'])
        response('Creo que la salud mental es muy importante. ¿Qué opinas?', ['qué', 'piensas', 'sobre', 'salud', 'mental'], required_words=['salud', 'mental'])
        response('Me gusta aprender sobre historia. ¿Qué asignatura te gusta más?', ['cuál', 'es', 'tu', 'asignatura', 'favorita'], required_words=['asignatura', 'favorita'])
        response('La programación es divertida. ¿Qué lenguaje de programación prefieres?', ['qué', 'lenguaje', 'programación', 'prefieres'], required_words=['programación'])

        # Additional responses
        response('Estoy aquí para ayudarte con tus estudios.', ['puedes', 'ayudarme', 'estudios'], required_words=['ayudarme', 'estudios'])
        response('La capital de Francia es París.', ['cuál', 'es', 'la', 'capital', 'de', 'francia'], required_words=['capital', 'francia'])
        response('El agua hierve a 100 grados Celsius.', ['a', 'qué', 'temperatura', 'hierve', 'el', 'agua'], required_words=['temperatura', 'hierve'])
        response('La gravedad en la Tierra es 9.8 m/s².', ['cuál', 'es', 'la', 'gravedad', 'en', 'la', 'tierra'], required_words=['gravedad', 'tierra'])
        response('El sol es una estrella.', ['qué', 'es', 'el', 'sol'], required_words=['sol'])
        response('Las ballenas son mamíferos.', ['las', 'ballenas', 'son', 'mamíferos'], required_words=['ballenas', 'mamíferos'])
        response('Hay siete continentes en el mundo.', ['cuántos', 'continentes', 'hay', 'en', 'el', 'mundo'], required_words=['continentes', 'mundo'])
        response('El lenguaje más hablado en el mundo es el inglés.', ['cuál', 'es', 'el', 'lenguaje', 'más', 'hablado', 'en', 'el', 'mundo'], required_words=['lenguaje', 'hablado'])
        response('La distancia de la Tierra al Sol es aproximadamente 150 millones de kilómetros.', ['cuál', 'es', 'la', 'distancia', 'de', 'la', 'tierra', 'al', 'sol'], required_words=['distancia', 'tierra', 'sol'])
        response('La fórmula química del agua es H₂O.', ['cuál', 'es', 'la', 'fórmula', 'química', 'del', 'agua'], required_words=['fórmula', 'agua']),
        response('cual es la capital de ecuador', ['cuál', 'es', 'la', 'capital', 'de', 'ecuador'], required_words=['capital', 'ecuador']),
        response('La fórmula química del agua es oxigeno.', ['cuál', 'es', 'la', 'fórmula', 'química', 'del', 'oxigeno'], required_words=['fórmula', 'oxigeno'])
        
        # Remembering context
        if 'nombre' in message:
            user_name = ' '.join(message[message.index('nombre')+1:])
            if user_name:
                self.context['name'] = user_name
                response(f'Mucho gusto, {user_name}', ['nombre'], single_response=True)

        if 'name' in self.context:
            response(f'¿Cómo estás hoy, {self.context["name"]}?', ['cómo', 'estás'], required_words=['cómo'])

        best_match = max(highest_prob, key=highest_prob.get)

        return self.unknown() if highest_prob[best_match] < 1 else best_match

    def unknown(self):
        responses = ['¿Puedes decirlo de nuevo?', 'No estoy seguro de lo que quieres.', 'Búscalo en Google a ver qué tal.']
        return random.choice(responses)

chat_bot = ChatBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = chat_bot.get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
