from flask import Flask, request
import openai
import os

openai.api_key = os.getenv("OPENAI_KEY")
used_words = {'3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}

app = Flask(__name__)


def get_word_from_open_ai(num):

    system_role = "You are a helpful assistant that answers only a json object containing a random word with the " \
                  "number of letters that is sent to you and that same word scrambled. For example: {'word': 'cat', " \
                  "'scrambledWord': 'tac'}. That word cannot be in this list: %s. If you can't come up with a word, " \
                  "fill the 'word' field with 'n'" % used_words.get(str(num))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_role}, {"role": "user", "content": str(num)}],
        temperature=0.9,
        )

    return response['choices'][0]['message']['content']

def getNewWord(data):
    difficulties = {
                      "easy":   3,
                      "medium": 4,
                      "intermediate": 5,
                      "challenging":  6,
                      "hard":   7,
                      "expert": 8,
                      "master": 9
                    }
    difficulty = data.get('difficulty')
    num_of_letters = difficulties[difficulty]

    word_data = get_word_from_open_ai(num_of_letters)

    word_data_dictionary = eval(word_data)

    used_words.get(str(num_of_letters)).append(word_data_dictionary.get('word'))
    print(used_words)
    return word_data


@app.route('/getword', methods=['POST'])
def getWord():
    return getNewWord(request.json)


if __name__ == '__main__':
    app.run()
