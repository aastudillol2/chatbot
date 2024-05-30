import re
import random

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

        # Basic responses
        response('Hola! ¿Cómo puedo ayudarte hoy?', ['hola', 'klk', 'saludos', 'buenas'], single_response=True)
        response('Estoy bien, ¿y tú?', ['cómo', 'estás', 'va', 'vas', 'sientes'], required_words=['cómo'])
        response('Estamos ubicados en la calle 23 número 123.', ['ubicados', 'dirección', 'dónde', 'ubicación'], single_response=True)
        response('Siempre a la orden.', ['gracias', 'te lo agradezco', 'thanks'], single_response=True)

        # Extended responses
        response('El clima está soleado y agradable.', ['cómo', 'está', 'clima', 'tiempo', 'hoy'], required_words=['clima'])
        response('Mi color favorito es el azul. ¿Cuál es el tuyo?', ['cuál', 'es', 'tu', 'color', 'favorito'], required_words=['color'])
        response('Me gusta la pizza, ¿y a ti?', ['qué', 'te', 'gusta', 'comer'], required_words=['gusta'])
        response('Trabajo como asistente virtual. ¿En qué trabajas tú?', ['a', 'qué', 'te', 'dedicas', 'trabajas'], required_words=['trabajas'])

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

while True:
    user_input = input('You: ')
    print("Bot:", chat_bot.get_response(user_input))
