import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import streamlit as st


# Charger le fichier texte de questions-réponses
def load_qa_file(file_path):
    qa_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            question = lines[i].strip()
            i += 1
            answer = lines[i].strip()
            i += 1
            qa_dict[question] = answer
    return qa_dict

# Charger le fichier de questions-réponses
qa_file = 'football_info_fr.txt'  # Assurez-vous que le chemin est correct
qa_dict = load_qa_file(qa_file)

# Tokeniser le texte en phrases
def preprocess(sentence):
    words = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.lower() not in stop_words and word not in string.punctuation]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Définir une fonction pour trouver la réponse à partir de la question
def get_most_relevant_sentence(query):
    query = preprocess(query)
    max_similarity = 0
    most_relevant_sentence = ""
    for question, answer in qa_dict.items():
        question_words = preprocess(question)
        similarity = len(set(query).intersection(question_words)) / float(len(set(query).union(question_words)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = answer
    return most_relevant_sentence

# Définir la fonction du chatbot
def chatbot(question):
    response = get_most_relevant_sentence(question)
    return response

# Créer une application Streamlit
def main():
    st.title("Chatbot sur le Football")
    st.write("Bonjour ! Je suis un chatbot. Posez-moi toutes vos questions sur le football.")
    
    question = st.text_input("Vous:")
    
    if st.button("Envoyer"):
        response = chatbot(question)
        st.write("Chatbot:", response)

if __name__ == "__main__":
    main()
