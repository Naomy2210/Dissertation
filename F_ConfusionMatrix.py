from A_ConnexionDB import connect, sql_to_dataframe, engine, dataframe_to_sql, disconnect
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# 1 Creating variables
# 1a creating a query variable to store our query to pass into the function
query = """SELECT created_at,pk,sentiment_noneu,sentiments_labels,bert_sentiment_labels,vader_sentiment_labels, distilbert_sentiment_labels, flair_sentiment_labels,roberta_sentiment_labels,sentistrength_sentiment_labels                         
            FROM merged_table
            """
# 1b creating a list with columns names to pass into the function
column_names = ['created_at', 'pk', 'sentiment_noneu', 'sentiments_labels', 'bert_sentiment_labels', 'vader_sentiment_labels', 'distilbert_sentiment_labels', 'flair_sentiment_labels','roberta_sentiment_labels','sentistrength_sentiment_labels']

# 2 opening the connection
conn = connect()

# 3 loading our dataframe
df = sql_to_dataframe(conn, query, column_names)

model = int(input("which analysis you want to run [1] for BERT, [2] for SentiStrength, [3] for VADER, [4] for GPT-2, [5] for FLAIR, [6] for DISTILBERT or [7] for ROBERTA ?"))
if model == 1:
    models = "bert"
elif model == 2:
    models= "sentistrength"
elif model == 3:
    models = "vader"
elif model == 5:
    models = "flair"
elif model == 6:
    models = "distilbert"
elif model == 7:
    models = "roberta"

# Assuming you have the true sentiment labels and predicted sentiment labels
predicted_labels = df[f'{models}_sentiment_labels']  # Model's predicted sentiment labels


if int(model) > 4 :
    true_labels = df['sentiment_noneu']  # Ground truth sentiment labels
    # Filter out None values from true_labels and predicted_labels
    mask = pd.notna(true_labels) & pd.notna(predicted_labels)
    true_labels = true_labels[mask]
    predicted_labels = predicted_labels[mask]
    cm = confusion_matrix(true_labels, predicted_labels, labels=['POS', 'NEG'])

    # Visualize the confusion matrix as a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['POS', 'NEG'], yticklabels=['POS', 'NEG'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(f'Confusion Matrix of {models} model')
    plt.show()

else :
    true_labels = df['sentiments_labels']  # Ground truth sentiment labels
    cm = confusion_matrix(true_labels, predicted_labels, labels=['POS', 'NEU', 'NEG'])

    # Visualize the confusion matrix as a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['POS', 'NEU', 'NEG'], yticklabels=['POS', 'NEU', 'NEG'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(f'Confusion Matrix of {models} model')
    plt.show()

# You can also get a classification report with precision, recall, and F1-score
report = classification_report(true_labels, predicted_labels)
print(report)
