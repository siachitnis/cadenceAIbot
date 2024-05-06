import pandas as pd
import mysql.connector
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 5

from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

def apply_nlp(text, summary_length=5):
    # Check if the text is long enough for summarization
    if len(text.split()) > 10:  
        # Perform summarization
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    return text  # Return the original text if too short for meaningful summarization

# def apply_lsa(text, summary_length=5):
#     parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
#     stemmer = Stemmer(LANGUAGE)
#     summarizer = Summarizer(stemmer)
#     summarizer.stop_words = get_stop_words(LANGUAGE)
#     return " ".join([str(sentence) for sentence in summarizer(parser.document, summary_length)])

def main():
    # Load the CSV file
    df = pd.read_csv('/Users/siachitnis/Downloads/thrive grant data - responses.csv')
    
    # Apply LSA summarization to your text column
    text_columns = ['Business Name.','Business Purpose','Achievements and Goals', 'Cash Flow Challenges', 'Actionable Insights','Angel Features and Tools']
    for col in text_columns:
        df[f'{col}_summary'] = df[col].apply(lambda x: apply_nlp(x, 5))

    df.to_csv('/Users/siachitnis/Downloads/summarized-responses.csv', index=False)


    conn = mysql.connector.connect(
      host='localhost',
      user='siachitnis',
      password='Synasia654',
      database='cadence_db')
    cursor = conn.cursor()


    # Insert data into the database
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO client_summaries (client_name, business_purpose, business_goals, cash_flow_challenges, desire_for_insights, desired_features_and_budget)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['Business Name.'], row['Business Purpose'], row['Achievements and Goals'], row['Cash Flow Challenges'], row['Actionable Insights'], row['Angel Features and Tools'])
        )
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
