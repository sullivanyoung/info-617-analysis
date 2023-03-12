#pip install textblob pandas

import urllib.request
from textblob import TextBlob
import pandas as pd

# can input your favorite movie script from imsdb website here:
url = "https://imsdb.com/scripts/How-to-Train-Your-Dragon.html"
response = urllib.request.urlopen(url)
html = response.read()

# extract the script from the HTML
start_tag = "<pre>"
end_tag = "</pre>"
start = html.decode().find(start_tag)
end = html.decode().find(end_tag, start + len(start_tag))
script_text = html.decode()[start+len(start_tag):end].strip()

script_blob = TextBlob(script_text)

# create a dictionary of findings to export to CSV
findings = {
    "Sentiment": {
        "Polarity": script_blob.sentiment.polarity,
        "Subjectivity": script_blob.sentiment.subjectivity
    },
    "Key Phrases": list(script_blob.noun_phrases),
}

# export to CSV
with pd.ExcelWriter('analysis.xlsx') as writer:
    pd.DataFrame.from_dict(findings["Sentiment"], orient='index').to_excel(writer, sheet_name='Sentiment')
    pd.DataFrame({'Key Phrases': findings["Key Phrases"]}).to_excel(writer, sheet_name='Key Phrases', index=False)
