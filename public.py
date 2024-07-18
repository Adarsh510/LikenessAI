import uuid
from flask import *

public=Blueprint('public',__name__)

@public.route("/")
def home():
	return render_template("index.html")


@public.route("/upload",methods=['get','post'])
def upload():
    data={}
    if 'submit' in request.form:
        img1 = request.files['img1']
        path1='static/'+str(uuid.uuid4())+str(img1.filename)
        img1.save(path1)
        img2 = request.files['img2']
        path2='static/'+str(uuid.uuid4())+str(img2.filename)
        img2.save(path2)
        ab=are_faces_same(path1, path2)
        data['res']=ab
        return redirect(url_for("public.result",ab=data['res']))
        # print("///////////////////////////////////////// : ",ab)

    return render_template("upload.html",data=data)

@public.route("/result")
def result():
    data={}
    ab=request.args['ab']
    data['res']=ab
    
    return render_template("result.html",data=data)







import face_recognition
import cv2
import numpy as np

def are_faces_same(image_path1, image_path2):
    # Load the images
    image1 = face_recognition.load_image_file(image_path1)
    image2 = face_recognition.load_image_file(image_path2)

    # Find face locations and encodings
    face_locations1 = face_recognition.face_locations(image1)
    face_encodings1 = face_recognition.face_encodings(image1, face_locations1)

    face_locations2 = face_recognition.face_locations(image2)
    face_encodings2 = face_recognition.face_encodings(image2, face_locations2)

    # Check if any faces were found in both images
    if not face_locations1 or not face_locations2:
        print("No faces found in one or both images.")
        return False

    # Compare face encodings
    results = []
    for encoding1 in face_encodings1:
        for encoding2 in face_encodings2:
            distance = np.linalg.norm(np.array(encoding1) - np.array(encoding2))
            results.append(distance)

    # Calculate the average similarity
    average_similarity = np.mean(results)
    re=""

    # Determine if there's a match and print the percentage
    if average_similarity < 0.6:  # You can adjust the threshold based on your requirements
        re=f"The given face images are the same. Similarity: {100 - average_similarity * 100:.2f}%"
        print(f"The given face images are the same. Similarity: {100 - average_similarity * 100:.2f}%")
    else:
        print("The given face images are different.")
        re="The given face images are different."
    return re

# # Example usage
# image_path1 = "sh2.jpg"
# image_path2 = "amm.jpg"
# are_faces_same(image_path1, image_path2)
