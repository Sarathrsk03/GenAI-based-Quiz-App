from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
load_dotenv()
import csv 

from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)



try:
    client = genai.Client(api_key=os.getenv('geminiAPI'))
except Exception as e:
    print("Error: ", e)




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




def addToDataset(topic: str):
    data = generateSyntheticData(topic)
    if not data:
        print("Failed to generate data")
        return
        
    try:
        with open('dataset.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for i in data:
                for question_number, question_details in i.items():
                    row = [
                        question_number,
                        question_details['question'],
                        question_details['options'][0],
                        question_details['options'][1],
                        question_details['options'][2],
                        question_details['options'][3],
                        question_details['correct_choice']
                    ]
                    writer.writerow(row)
                    
                    try:
                        supabase.table("quizQuestions").insert({
                            "topic": topic,
                            "question": question_details['question'],
                            "choice-1": question_details['options'][0],
                            "choice-2": question_details['options'][1],
                            "choice-3": question_details['options'][2],
                            "choice-4": question_details['options'][3],
                            "correctChoice": question_details['correct_choice']
                        }).execute()
                    except Exception as e:
                        print(f"Error inserting to Supabase: {e}")
                        
            print("Added to dataset successfully")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


if __name__ == "__main__":    
    addToDataset(topic="Python Programming")


