from flask import Flask, render_template, request
import os
import google.generativeai as genai
import re

os.environ["GOOGLE_API_KEY"] = "AIzaSyAhhYlDosHx2ruW-I2ZRQn3tG1uI2vOdZo"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

app = Flask(__name__)

prompt_template = """"Diet Recommendation System:\n"
             "I want you to recommend 6 restaurants names only, 6 breakfast names only, 5 dinner names only, and 6 workout names only, "
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}.
             (No suggestion no extra word need)
             (also add emoji for particular restuarants, foods)
             """



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_noveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']

        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,  # Consider converting to cm if needed
            'veg_or_nonveg': veg_or_noveg,
            'disease': disease,
            'region': region,
            'allergics': allergics,
            'foodtype': foodtype
        }

        # Generate the formatted prompt
        prompt = prompt_template.format(**input_data)

        response = model.generate_content(prompt).text

        # Extracting the different recommendations using regular expressions
        import re
        names = re.findall(r"Restaurants:(.*?)Breakfast:", response, re.DOTALL)
        breakfast = re.findall(r"Breakfast:(.*?)Dinner:", response, re.DOTALL)
        dinner = re.findall(r"Dinner:(.*?)Workout:", response, re.DOTALL)
        workout = re.findall(r"Workout:(.*)$", response, re.DOTALL)

        # Cleaning up the extracted lists
        restaurant_names = [i.strip() for i in names[0].strip().split('\n') if i.strip() != "**"] if names else []
        breakfast_names = [i.strip() for i in breakfast[0].strip().split('\n') if i.strip() != "**"] if breakfast else []
        dinner_names = [i.strip() for i in dinner[0].strip().split('\n') if i.strip() != "**"] if dinner else []
        workout_names = [i.strip() for i in workout[0].strip().split('\n') if i.strip() != "**"] if workout else []

        return render_template('result.html', restaurant_names=restaurant_names,breakfast_names=breakfast_names,dinner_names=dinner_names,workout_names=workout_names)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)