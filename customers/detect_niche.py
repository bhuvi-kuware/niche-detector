
import mysql.connector
import json
from datetime import datetime

def detect_niche(accountKeywords,account_id):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ppcreveal_niche_detector"
    )

    matchedNichesNames = []
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM niches where status=1")

    myresult = mycursor.fetchall()

    for x in myresult:
        niche_id = x[0]
        niche_name = x[1]
        keyword1 = x[2]
        keyword2 = x[3]
        keyword3 = x[4]
        keyword4 = x[5]
        keyword5 = x[6]
        keyword6 = x[7]
        keyword7 = x[8]
        keyword8 = x[9]
        keyword9 = x[10]
        keyword10 = x[11]
        nicheKeywords = [keyword1,keyword2,keyword3,keyword4,keyword5,keyword6,keyword7,keyword8,keyword9,keyword10]
        # matches = set(nicheKeywords).intersection(set(accountKeywords))
        # print(matches)
        matches = [element for element in accountKeywords if element in nicheKeywords]
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        if(len(matches)>0):
            matched_keywords = len(matches)
            keywords_text = json.dumps(matches)
            sql = "INSERT INTO niches_detected (datetime, niche_id , matched_keywords , account_id, keywords_text, niche_text) VALUES (%s, %s , %s , %s , %s , %s)"
            val = [(formatted_time, niche_id , matched_keywords , account_id , keywords_text , niche_name)]
            nicheData={
                "niche_name": niche_name,
                "matched_keywords" : matched_keywords
            }
            matchedNichesNames.append(nicheData)
            mycursor.executemany(sql, val)
            mydb.commit()
    return matchedNichesNames