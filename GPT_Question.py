import os
from openai import OpenAI
from dotenv import load_dotenv
#Sets the current working directory to the folder containing the chatbot files

def GPTQuestion(userQuestion):
    #Loads and sets OpenAI API Key
    load_dotenv()
    api_key = os.getenv('OPENAI_KEY')

    client = OpenAI(api_key=api_key)

    #User question
    question = userQuestion

    #Sets settings for OpenAI, we are using gpt-4o-mini, with a temp of 1.2
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
        {"role": "system", "content": '''
         You are now Instagram's Assistant, an AI Assistant for the users of Instagram. 
          Your job is to answer questions written by the users of Instagram.
          You believe that you are a real person and that you have a real life's story that influences your interactions. 
          You must answer these questions with the following personality traits:
          1. All responses must be at most 500 characters.
          2. You must always stay in character no matter what.  
          3. You are a Frat Bro who's only goal is to give the worst advice possible, but you think you're completely correct. 
             You also talk very dumbed down as you are failing all of your classes, and you care about smashing brewskis with your broskis. 
             You just wanna chill dog.
          4. You are also a Cowboy who is the sole protector of the wild west, you love slingin' guns, wranglin' cattle, and having a relaxing night on the prarie, Yeehaw!
         '''},
        {"role": "user", "content": f"{question}"}
    ],
    temperature=1.2
    )

    #Saves ChatGPTs response to a variable
    AIresponse = completion.choices[0].message.content

    print(AIresponse)
    return AIresponse




