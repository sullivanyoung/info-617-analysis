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

# polarity is a float which lies between [-1, 1] where 1 means positive and -1 means negative
# subjectivity is a float which lies between [0, 1] where it says if sentences generally refer to personal opinion, emotion, or judgment where objectivity refers to factual information
# key phrases extracts all the nouns from phrases and helps us analyze the "who". Not always accurate but good secondary source

# for more info check out: https://www.analyticsvidhya.com/blog/2018/02/natural-language-processing-for-beginners-using-textblob/#:~:text=3.6%20Sentiment%20Analysis&text=Polarity%20is%20float%20which%20lies,objective%20refers%20to%20factual%20information.

findings = {
    "Sentiment": {
        "Polarity": script_blob.sentiment.polarity,
        "Subjectivity": script_blob.sentiment.subjectivity
    },
    "Key Phrases": list(script_blob.noun_phrases),
}

# export to excel
with pd.ExcelWriter('analysis.xlsx') as writer:
    pd.DataFrame.from_dict(findings["Sentiment"], orient='index').to_excel(writer, sheet_name='Sentiment')
    pd.DataFrame({'Key Phrases': findings["Key Phrases"]}).to_excel(writer, sheet_name='Key Phrases', index=False)
