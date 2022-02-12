import pickle
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    port = '3306',
    database = 'toxic_comment'
)

mycursor = mydb.cursor()

query='SELECT * FROM comments  ORDER BY id DESC LIMIT 1'
mycursor.execute(query)

myresult = mycursor.fetchall()

result_List =[]
for x in myresult:
    #print(type(x))
    result_List=list(x)
variety=result_List[3]
print(variety )


# In[2]:


MAX_SEQUENCE_LENGTH = 100
MAX_NB_WORDS = 100000
EMBEDDING_DIM = 50


# In[3]:



from tensorflow import keras
model1 = keras.models.load_model("C:\\Users\MaSsS\Downloads\Try_model1.h5")


# In[4]:


train_df = pd.read_csv("C:\\Users\\MaSsS\\Downloads\\train.csv")
test_df = pd.read_csv("C:\\Users\\MaSsS\\Downloads\\test.csv")


# In[5]:


def get_pos_ratio(data):
    return data.sum() / len(data)

pos_ratio = []
for col in ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']:
    pos_ratio.append(get_pos_ratio(train_df[col]))


# In[6]:


########################################
## Text pre-processing and cleaning
########################################
print('Processing text dataset')
from collections import defaultdict

# regex to remove all Non-Alpha Numeric and space
special_character_removal=re.compile(r'[^a-z\d ]',re.IGNORECASE)

# regex to replace all numeric
replace_numbers=re.compile(r'\d+',re.IGNORECASE)

def clean_text(text, stem_words=False):
    # Clean the text, with the option to remove stopwords and to stem words.
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"i’m", "i am", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = replace_numbers.sub('', text)
    text = special_character_removal.sub('',text)
    
    return text


# In[7]:



train_comments = []
test_comments = []


# In[8]:




train_comments = [clean_text(text) for text in train_df["comment_text"]]
test_comments = [clean_text(text) for text in test_df["comment_text"]]


# In[9]:


assert len(train_comments) == 159571 and len(test_comments) == 153164, "It seems that you lost some data."
assert 'E' not in train_comments[0], "It seems you did not preprocess the sentecnes. I found a upper case alphabet in your train set."


# In[10]:


# Create a tokenize, which transforms a sentence to a list of ids
tokenizer = Tokenizer(num_words=MAX_NB_WORDS)

# Build the relation between words and ids 
tokenizer.fit_on_texts(train_comments + test_comments)


# In[11]:


tests_input_sentences =  [['Hello', 'World'], ['Greeting', 'my', 'friend'], ['Hello', 'have', 'a', 'nice', 'day']]
transform_this_sentences = [['Hello', 'my', 'friend']]

def index_encoding(sentences, raw_sent):
    word2idx = {}
    idx2word = {}
    ctr = 1
    for sentence in sentences:
        for word in sentence:
            if word not in word2idx.keys():
                word2idx[word] = ctr
                idx2word[ctr] = word
                ctr += 1
    results = []
    for sent in raw_sent:
        results.append([word2idx[word] for word in sent])
    return results


# In[12]:


CLASSES = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]


# In[29]:


def comment_toxic_predict(comment):
  ad=[comment]
  cla=[clean_text(text) for text in ad]
  tokenizer.fit_on_texts(cla)
  cla = tokenizer.texts_to_sequences(cla)
  ada = pad_sequences(cla, maxlen=MAX_SEQUENCE_LENGTH)
  pred=model1.predict(ada, batch_size=256, verbose=1)
  df_pred=pd.DataFrame(data=pred, columns=CLASSES)
  sams = df_pred.iloc[0]
  if (sams[0]>0.5 or sams[1]>0.5 or sams[2]>0.5 or sams[3]>0.5 or sams[4]>0.5 or sams[5]>0.5):
    return (1)
    print("Given below gives your level of toxicity in u=your comment. Please be resposible while posting comment.")
    print(df_pred)
    
  else:
    print(df_pred)
    return (2)
    


# In[31]:

#query="INSERT INTO result(user,prediction)VALUES(user,prediction);"
#mycursor.execute(query)
