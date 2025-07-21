from flask import Flask, request, render_template, redirect
import boto3, json, uuid, os

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET = 'petpost-images-cglynn'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        file = request.files['image']

        image_name = f"{uuid.uuid4()}_{file.filename}"
        s3.upload_fileobj(file, BUCKET, image_name, ExtraArgs={'ACL': 'public-read'})
        image_url = f"https://{BUCKET}.s3.amazonaws.com/{image_name}"

        new_pet = {"name": name, "age": age, "breed": breed, "image": image_url}
        pets = []

        if os.path.exists("pets.json"):
            with open("pets.json", "r") as f:
                pets = json.load(f)

        pets.append(new_pet)

        with open("pets.json", "w") as f:
            json.dump(pets, f)

        return redirect('/')

    pets = []
    if os.path.exists("pets.json"):
        with open("pets.json", "r") as f:
            pets = json.load(f)

    return render_template("index.html", pets=pets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

