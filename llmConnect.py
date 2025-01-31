from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
load_dotenv()
import csv 


try:
    client = genai.Client(api_key=os.getenv('geminiAPI'))
except Exception as e:
    print("Error: ", e)


def readSystemInstructions():
    try:
        with open('systemInstruction.txt', 'r') as file:
            data = file.read()
            return data 
    except Exception as e:
        print("Error: ", e)
        return None
    

def generateSyntheticData(topic:str):
    response = client.models.generate_content(
       model="gemini-2.0-flash-exp", 
       contents= topic ,
       config = types.GenerateContentConfig(
           response_mime_type="application/json",
           system_instruction= readSystemInstructions()
       )
    )

    return json.loads(response.text)   





def addToDataset(topic:str):
    data = generateSyntheticData(topic)
    print(data)
    print(type(data))
    with open('dataset.csv', 'w') as file:
        writer = csv.writer(file)
        for i in data:
            for question_number, question_details in i.items():
                writer.writerow([question_number,question_details['question'],question_details['options'][0],question_details['options'][1],question_details['options'][2],question_details['options'][3],question_details['correct_choice']])
            print("Added to dataset")


if __name__ == "__main__":    
    addToDataset(topic="Python Programming")


