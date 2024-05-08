import random
import nltk
import time
from tqdm import tqdm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fuzzywuzzy import fuzz
from nltk.corpus import words as nltk_words
from nltk.tokenize import word_tokenize

# Constants
SIMILARITY_THRESHOLD = 50
DYSLEXIA_SCORE_THRESHOLD = 3.5

# Ensure necessary NLTK resources are available
def ensure_nltk_resources():
    nltk.download('punkt')
    nltk.download('words')

# Initialize NLTK resources
ensure_nltk_resources()

# Create a set of English words from NLTK
english_vocab = set(w.lower() for w in nltk_words.words())

# Define dyslexic letter and word confusions as constants
DYSLEXIC_LETTER_CONFUSIONS = [
    ('b', 'd'), ('p', 'q'), ('m', 'w'), ('n', 'u'), ('n', 'r'),
    ('i', 'j'), ('a', 'e'), ('s', 'z'), ('f', 't'), ('c', 'k'),
    ('g', 'q'), ('h', 'n'), ('v', 'w'), ('b', 'p'), ('c', 's'),
    ('d', 't'), ('o', 'e'), ('a', 'o'), ('u', 'v'), ('m', 'n')
]

DYSLEXIC_WORD_CONFUSIONS = [
    ('was', 'saw'), ('there', 'their'), ('here', 'hear'),
    ('you', 'your'), ('where', 'wear'), ('to', 'too', 'two'),
    ('here', 'here'), ('their', 'there'), ('its', 'it\'s'),
    ('to', 'two', 'too'), ('where', 'were'), ('new', 'knew'),
    ('there', 'their', 'they\'re'), ('your', 'you\'re'), ('its', 'it\'s'),
    ('to', 'too', 'two'), ('break', 'brake'), ('bare', 'bear'), ('peace', 'piece'),
    ('where', 'wear'), ('here', 'hear'), ('right', 'write'), ('flower', 'flour'),
    ('buy', 'by', 'bye'), ('no', 'know'), ('for', ' four'), ('sun', 'son'),
    ('allowed', 'aloud'), ('hour', 'our'), ('blew', 'blue'), ('sew', 'sow'),
    ('be', 'bee'), ('one', 'won'), ('here', 'hair'), ('you', 'ewe'),
    ('toe', 'tow'), ('flower', 'flour'), ('threw', 'through'), ('role', 'roll'),
    ('flower', 'flour'), ('peace', 'piece'), ('mail', 'male'), ('tail', 'tale')
]

# Tokenize and clean the text using NLTK's word_tokenize
def tokenize_and_clean_text(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum()]

# Check if the user input sentence is exactly the same as the random sentence
def is_exact_match(user_text, random_sentence):
    user_text_lower = user_text.lower().strip()
    random_sentence_lower = random_sentence.lower().strip()
    return user_text_lower == random_sentence_lower

# Check if two strings are similar based on a threshold
def are_strings_similar(str1, str2, threshold):
    similarity_score = fuzz.ratio(str1.lower(), str2.lower())
    return similarity_score >= threshold

# Get a random sentence from a file
def read_sentences_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            sentences = file.readlines()
        return sentences
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{filename}': {e}")
        return []

# Calculate the dyslexia score for a single word
def calculate_word_dyslexia_score(word, random_sentence):
    word_tokens = tokenize_and_clean_text(word)
    sentence_tokens = tokenize_and_clean_text(random_sentence)
    dyslexia_score = 0

    if word_tokens == sentence_tokens:
        dyslexia_score -= 1
        return 0

    for word_token in word_tokens:
        token_dyslexia_score = 0

        if word_token not in english_vocab:
            token_dyslexia_score += 3.0

        for confusion in DYSLEXIC_LETTER_CONFUSIONS:
            if confusion[0] in word_token and confusion[1] in word_token:
                token_dyslexia_score += 3.0

        for confusion in DYSLEXIC_WORD_CONFUSIONS:
            if all(conf_word in word_token for conf_word in confusion):
                token_dyslexia_score += 4.0

        if len(word_token) == len(sentence_tokens[0]):
            transpositions = [(word_token[:i] + word_token[i + 1] + word_token[i] + word_token[i + 2:]) for i in range(len(word_token) - 1)]
            if sentence_tokens[0] in transpositions:
                token_dyslexia_score += 3.0

        if word_token[::-1] == sentence_tokens[0]:
            token_dyslexia_score += 3.0

        dyslexia_score += token_dyslexia_score

        if token_dyslexia_score == 0:
            dyslexia_score -= 0.3

    return dyslexia_score


# Perform dyslexia analysis for a user-entered sentence
def dyslexia_analysis(user_text, random_sentence):
    if is_exact_match(user_text, random_sentence):
        return 0  # Exact match, no dyslexia detected

    words = tokenize_and_clean_text(user_text)
    dyslexia_scores = []

    with tqdm(total=len(words), desc="Dyslexia Analysis Status") as pbar:
        for word in words:
            dyslexia_score = calculate_word_dyslexia_score(word, random_sentence)
            dyslexia_scores.append(dyslexia_score)
            pbar.update(1)

    avg_score = round(sum(dyslexia_scores) / len(dyslexia_scores), 3)
    return avg_score

# Generate a PDF report with user's name and ID
def generate_pdf_report(user_responses, dyslexia_scores, avg_score, final_verdict, user_name, user_id):
    pdf_filename = f"{user_name}_{user_id}_dyslexia_report.pdf"

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter  # Get page dimensions

    # Title
    title_font_size = 16
    c.setFont("Helvetica-Bold", title_font_size)
    title_text = "Dyslexia Analysis Report"
    title_text_width = c.stringWidth(title_text, "Helvetica-Bold", title_font_size)
    title_x = (width - title_text_width) / 2
    c.drawString(title_x, height - 40, title_text)

    # Add space between title and content
    y_position = height - 70  # Adjust the vertical position

    # User Name
    user_name_font_size = 12
    c.setFont("Helvetica-Bold", user_name_font_size)
    user_name_text = "Full Legal Name:"
    c.drawString(100, y_position, user_name_text)

    c.setFont("Helvetica", user_name_font_size)
    c.drawString(220, y_position, user_name)

    # User ID
    user_id_font_size = 12
    c.setFont("Helvetica-Bold", user_id_font_size)
    user_id_text = "State ID Number:"
    y_position -= 20  # Space between User Name and User ID
    c.drawString(100, y_position, user_id_text)

    c.setFont("Helvetica", user_id_font_size)
    c.drawString(220, y_position, user_id)

    # User Responses
    user_response_font_size = 14
    c.setFont("Helvetica-Bold", user_response_font_size)
    user_response_text = "User Responses:"
    y_position -= 20  # Space between sections
    c.drawString(100, y_position, user_response_text)

    response_font_size = 12
    y_position -= response_font_size + 2
    for response in user_responses:
        c.setFont("Helvetica", response_font_size)
        response_text = "- " + response.strip()
        c.drawString(120, y_position, response_text)
        y_position -= response_font_size + 2

    # Dyslexia Scores
    dyslexia_score_font_size = 14
    c.setFont("Helvetica-Bold", dyslexia_score_font_size)
    dyslexia_score_text = "Dyslexia Scores:"
    y_position -= 20  # Space between sections
    c.drawString(100, y_position, dyslexia_score_text)

    score_font_size = 12
    y_position -= score_font_size + 2
    for score in dyslexia_scores:
        formatted_score = "{:.3f}".format(score)
        c.setFont("Helvetica", score_font_size)
        score_text = "- Score: " + formatted_score
        c.drawString(120, y_position, score_text)
        y_position -= score_font_size + 2

    # Average Score and Final Verdict
    avg_score_font_size = 14
    c.setFont("Helvetica-Bold", avg_score_font_size)
    avg_score_text = "Average Dyslexia Score:"
    y_position -= 20  # Space between sections
    c.drawString(100, y_position, avg_score_text)

    formatted_avg_score = "{:.3f}".format(avg_score)
    c.setFont("Helvetica", avg_score_font_size)
    avg_score_value_text = formatted_avg_score
    avg_score_text_width = c.stringWidth(avg_score_text, "Helvetica-Bold", avg_score_font_size)
    avg_score_value_text_width = c.stringWidth(avg_score_value_text, "Helvetica", avg_score_font_size)
    x_position = 100 + avg_score_text_width + 10  # Space between text and value
    c.drawString(x_position, y_position, avg_score_value_text)

    final_verdict_font_size = 14
    c.setFont("Helvetica-Bold", final_verdict_font_size)
    final_verdict_text = "Final Verdict:"
    y_position -= avg_score_font_size + 2
    c.drawString(100, y_position, final_verdict_text)

    x_position = 100 + c.stringWidth(final_verdict_text, "Helvetica-Bold",
                                     final_verdict_font_size) + 10  # Space between text and value
    c.setFont("Helvetica", final_verdict_font_size)

    # Set the color to green if "Final Verdict" does not contain "dyslexic", else set it to red
    text_color = "red" if "Likelihood of dyslexia detected." in final_verdict else "green"
    c.setFillColor(text_color)
    c.drawString(x_position, y_position, final_verdict)

    # Add space before the signature
    y_position -= 40

    # Signature line
    signature_font_size = 12
    text_color = "black"
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", signature_font_size)
    signature_text = "Signature: _____________"
    c.drawString(100, y_position, signature_text)

    # Save the PDF
    c.save()
    print(f"PDF report '{pdf_filename}' generated successfully.")

# Main program
def main():
    user_responses = []
    used_sentences = set()

    try:
        user_name = input("\nPlease enter the patient's name: ").strip()
        user_id = input("Please enter the patient's ID: ").strip()

        max_attempts = 3

        for attempt in range(max_attempts):
            sentences = read_sentences_from_file("sentences.txt")
            if not sentences:
                print("Unable to read sentences from the file. Exiting.")
                return

            random_sentence = random.choice(sentences).strip()
            print(f"\nGenerated Sentence (Attempt {attempt + 1}): {random_sentence}")

            while True:
                user_text = input("Enter the sentence for analysis: \n").strip()

                if not user_text:
                    print("Empty input received. Please try again.")
                    continue

                if is_exact_match(user_text, random_sentence):
                    user_responses.append(user_text)
                    break
                elif are_strings_similar(user_text, random_sentence, SIMILARITY_THRESHOLD):
                    user_responses.append(user_text)
                    break
                else:
                    print("Your response is significantly different from the generated sentence. Please try again.")
                    time.sleep(1)
                    print(f"Copy the following sentence: {random_sentence}")

        dyslexia_scores = []
        for response in user_responses:
            score = dyslexia_analysis(response, random_sentence)
            if score > 0:
                dyslexia_scores.append(score)

        non_zero_scores = [score for score in dyslexia_scores if score > 0]
        avg_score = round(sum(non_zero_scores) / len(non_zero_scores), 3) if non_zero_scores else 0.0

        final_verdict = "Likelihood of dyslexia detected." if avg_score >= DYSLEXIA_SCORE_THRESHOLD else "No significant signs of dyslexia detected."
        print(f"\nAverage Dyslexia Score: {avg_score:.3f}\nFinal Verdict: {final_verdict}")

        generate_pdf_report(user_responses, dyslexia_scores, avg_score, final_verdict, user_name, user_id)


    except KeyboardInterrupt:
        print("\nOperation aborted by the user.")

if __name__ == "__main__":
    main()