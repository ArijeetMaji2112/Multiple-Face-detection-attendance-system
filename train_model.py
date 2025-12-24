import cv2
import os
import numpy as np

dataset_path = "dataset"
model_save_path = "models/face_trainer.yml"

# Create recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

# Map employee folder names to numeric labels
emp_folders = os.listdir(dataset_path)
label_dict = {}
label_count = 0

for emp_folder in emp_folders:
    label_count += 1
    label_dict[label_count] = emp_folder
    emp_path = os.path.join(dataset_path, emp_folder)
    
    for img_name in os.listdir(emp_path):
        img_path = os.path.join(emp_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        labels.append(label_count)

faces = np.array(faces)
labels = np.array(labels)

# Train the recognizer
recognizer.train(faces, labels)

# Save trained model
os.makedirs("models", exist_ok=True)
recognizer.save(model_save_path)

print(f"Model trained successfully and saved at {model_save_path}")
print("Label mapping:")
for k, v in label_dict.items():
    print(f"{k}: {v}")
