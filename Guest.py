import os
import pandas
import numpy as np
import pickle
import cv2

class Guest():
    def __init__(self, name="", question="", image=None, answers=None, right_answer=None, explaination=None):
        """
        Initialize the Guest class with default values.
        """
        self.name = name  # Default is an empty string
        self.question = question  # Default is an empty string
        self.image = image if image is not None else np.array([])  # Default is an empty numpy array
        self.answers = answers if answers is not None else {}  # Default is an empty dictionary
        self.right_answer = None  # Default is None
        self.explaination = None # List of: path to explainatory image, adn explaination text

def main():
    # # Example usage of the Guest class
    # guest = Guest()
    # guest.name = input("Enter guest name: ")  # Get the guest's name from user input
    # guest.question = input("\nEnter question: ")  # Get the question from user input
    # n_answers  = 4
    # for i in range(n_answers):
    #     answer = input(f"Enter answer {i+1}: ")
    #     guest.answers[chr(65 + i)] = answer  # Store answers in a dictionary with keys A, B, C, D

    # img_name = input("Enter path to image (without extension): ")  # Get the path to the image from user input
    # path_to_image = os.path.join("Images/guests_img", img_name)  # Construct the full path to the image
    # guest.image = cv2.imread(f"{path_to_image}.png")  # Load an image using OpenCV
    # cv2.imshow(guest.name, guest.image)  # Display the image using OpenCV
    # guest.right_answer = input("Enter the correct answer (A, B, C, D): ")  # Get the correct answer from user input

    # guest.explaination = [os.path.join("Images/Explainations", guest.name), input("Enter explaination text: ")]  # Get the explaination from user input

    # # Print the guest's details
    # print(f"Name: {guest.name}")
    # print(f"Question: {guest.question}")
    # print(f"Answers: {guest.answers}")
    # print(f"Right Answer: {guest.right_answer}")
    # print(f"Explaination: {guest.explaination}")

    # save_guest(guest)  # Save the guest object to a file

    # Load guest
    guest_name = input("Enter the name of the guest to load: ")  # Get the name of the guest to load from user input
    loaded_guest = load_guest(guest_name)

    if loaded_guest:
        print(f"\nLoaded Guest:")
        print(type(loaded_guest))
        print(f"Name: {loaded_guest.name}")
        print(f"Question: {loaded_guest.question}")
        print(f"Answers: {loaded_guest.answers}")
        print(f"Right Answer: {loaded_guest.right_answer}")
        print(f"Explaination: {loaded_guest.explaination}")

def save_guest(guest, directory="Guests"):
    os.makedirs(directory, exist_ok=True)  # Create the folder if it doesn't exist
    filename = f"{guest.name.replace(' ', '_')}.pkl"  # Sanitize filename
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(guest, f)
    print(f"Guest saved to: {filepath}")

def load_guest(name, directory="guests"):
    filename = f"{name.replace(' ', '_')}.pkl"
    filepath = os.path.join(directory, filename)
    
    if not os.path.exists(filepath):
        print(f"No saved guest found at: {filepath}")
        return None

    with open(filepath, 'rb') as f:
        guest = pickle.load(f)
    
    return guest
    
if __name__ == "__main__":
    main()