
import pyodbc
import pickle
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    port = '3306',
    database = 'wine'
)

mycursor = mydb.cursor()

query='SELECT * FROM user_wine  ORDER BY id DESC LIMIT 1'
mycursor.execute(query)

myresult = mycursor.fetchall()

result_List =[]
for x in myresult:
    print(type(x))
    result_List=list(x)
variety=result_List[4]


with open('model1','rb') as f:
    nb=pickle.load(f)
    wine_pivot=pd.read_pickle("pivotpickle.pkl")
    wine=list(wine_pivot.index)
    l=wine.index(variety)
    distance, indice = nb.kneighbors(wine_pivot.iloc[l,:].values.reshape(1,-1),n_neighbors=2)
    for i in range(1, len(distance.flatten())):
        prediction=wine_pivot.index[indice.flatten()[i]]

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    port = '3306',
    database = 'wine'
)

mycursor = mydb.cursor()

#query="INSERT INTO result(user,prediction)VALUES(user,prediction);"
#mycursor.execute(query)


sql = "INSERT INTO predict (recom) VALUES (%s)"
val = [(prediction)]
mycursor.execute(sql, val)
mydb.commit()


 



       





       
