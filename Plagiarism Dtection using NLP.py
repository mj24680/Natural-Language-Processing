# Import Some Libraries For User Interface
import os
# This library provides a way for Python programs to interact with the operating system. For example, you can use
# os.listdir() to get a list of files in a directory, or os.getcwd() to get the current working directory.

import tkinter as tk
# Tkinter is Python's standard GUI toolkit. It provides a set of modules that allows you to create windows, buttons,
# text boxes, and other graphical elements in your Python programs.

from tkinter import messagebox
# You can use them to display information, warnings, errors, or to ask the user for confirmation before proceeding
# with an action.
from tkinter import PhotoImage
from tkinter import filedialog
#  It allows you to prompt the user to select a file or a directory from their computer.

import nltk
# Natural Language Toolkit provides various tools and resources for tasks like tokenization (splitting text into
# words or sentences), tagging (assigning parts of speech to words). It's widely used in NLP tasks such as text
# classification, sentiment analysis, and language translation.

from nltk.tokenize import word_tokenize
# This is a function from the NLTK library that takes a piece of text (like a sentence or paragraph)
# and breaks it down into individual words or tokens.

from nltk.corpus import stopwords
# This part of the NLTK library contains a list of common words in a language
# that are often filtered out from text before analysis because they don't carry much meaning.
# These words include things like "the", "is", "and", etc.

from collections import Counter
# counts the occurrences of items in a list. or word frequencies in a text.

# import cosine similarity function from sklearn
from sklearn.metrics.pairwise import cosine_similarity

import string
import math

# Download Some NLTK Resources
nltk.download('punkt')
nltk.download('stopwords')


def preprocess_text(text):
    # Tokenize the text into words
    tokens = word_tokenize(text.lower())

    # Remove punctuation
    tokens = [word for word in tokens if word not in string.punctuation]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return tokens


def calculate_magnitude(vector):
    sum_of_squares = 0

    for element in vector:
        sum_of_squares += element ** 2

    magnitude = math.sqrt(sum_of_squares)

    return magnitude


def calculate_cosine_similarity(doc1, doc2):
    doc1_tokens = preprocess_text(doc1)
    doc2_tokens = preprocess_text(doc2)

    # count words Frequency or Occurrence of a words
    # Counter function returns a dictionary
    doc1_words_count = Counter(doc1_tokens)
    print(doc1_words_count)

    doc2_words_count = Counter(doc2_tokens)
    print(doc2_words_count)

    # get all words from both two Documents

    all_words = set(doc1_words_count).union(doc2_words_count)
    print(all_words)

    doc1_vector = []

    for word in all_words:
        if word in doc1_tokens:
            doc1_vector.append(doc1_words_count[word])
        else:
            doc1_vector.append(0)

    print(doc1_vector)

    doc2_vector = []
    for word in all_words:
        if word in doc2_tokens:
            doc2_vector.append(doc2_words_count[word])
        else:
            doc2_vector.append(0)

    print(doc2_vector)

    # Find Similarity by using built-in Function
    # similarity = cosine_similarity([doc1_vector], [doc2_vector])[0][0]

    # Find Similarity Manually
    dot_product = 0
    for i in range(len(doc1_vector)):
        dot_product += doc1_vector[i] * doc2_vector[i]

    print(dot_product)

    doc1_vector_magnitude = calculate_magnitude(doc1_vector)
    doc2_vector_magnitude = calculate_magnitude(doc2_vector)

    similarity = dot_product / (doc1_vector_magnitude * doc2_vector_magnitude)

    return similarity


def browse_files():
    # Clear Previous Output
    text_output.delete(1.0, tk.END)

    # Show Dialog Box for Select files
    # returning a list of selected files
    file_paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])

    if len(file_paths) < 2:
        messagebox.showwarning("Warning", "Please select at least two text files.")

    # Read and Compare Files
    for i in range(len(file_paths)):
        for j in range(i + 1, len(file_paths)):
            document1 = open(file_paths[i], 'r').read()
            document2 = open(file_paths[j], 'r').read()
            similarity_score = calculate_cosine_similarity(document1, document2)
            text_output.insert(tk.END,
                               f"Similarity between {os.path.basename(file_paths[i])} and {os.path.basename(file_paths[j])}: {similarity_score:.2f}\n")


# Create the GUI
root = tk.Tk()
root.title("Plagiarism Detection")
root.geometry("700x450")
root.minsize(700, 450)
root.maxsize(700, 450)

img = tk.PhotoImage(file="Black and Blue Modern Gradient Zoom Virtual Background.png")
bg_img = tk.Label(root, image=img)
bg_img.place(relheight=1, relwidth=1)

# Create browse button
round_btn = PhotoImage(file="Round Button.png")
browse_button = tk.Button(root, image=round_btn, border=0, bg="black", command=browse_files)
browse_button.place(relx=0.49, rely=0.42, anchor="center")  # Manually set the position
browse_button.config(cursor='hand2')

# Create text output area
text_output = tk.Text(root, height=6, width=50)
text_output.place(relx=0.5, rely=0.75, anchor="center")  # Manually set the position
text_output.config(font=("Helvetica", 18))

root.mainloop()
