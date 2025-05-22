import os
import numpy as np
import cv2
from Guest import Guest  # Assuming Guest class is defined in Guest.py
from utils import save_guest, load_guest  # Assuming save_guest and load_guest functions are defined in utils.py


def main():
    # Example usage of the Guest class
    guest = Guest()
    guest.name = input("Enter guest name: ")  # Get the guest's name from user input
    guest.question = input("\nEnter question: ")  # Get the question from user input
    n_answers  = 4
    for i in range(n_answers):
        answer = input(f"Enter answer {i+1}: ")
        guest.answers[chr(65 + i)] = answer  # Store answers in a dictionary with keys A, B, C, D

    img_name = guest.name  # Get the path to the image from user input
    path_to_image = os.path.join("Images/guests_img", img_name)  # Construct the full path to the image
    guest.image = cv2.imread(f"{path_to_image}.png")  # Load an image using OpenCV
    # cv2.imshow(guest.name, guest.image)  # Display the image using OpenCV
    guest.right_answer = input("Enter the correct answer (A, B, C, D): ")  # Get the correct answer from user input

    guest.explaination = [os.path.join("Images/Explainations", guest.name), input("Enter explaination text: ")]  # Get the explaination from user input
    
    # Print the guest's details
    print(f"Name: {guest.name}")
    print(f"Question: {guest.question}")
    print(f"Answers: {guest.answers}")
    print(f"Right Answer: {guest.right_answer}")
    print(f"Explaination: {guest.explaination}")

    save_guest(guest)  # Save the guest object to a file

    # Load guest
    # guest_name = input("Enter the name of the guest to load: ")  # Get the name of the guest to load from user input
    # loaded_guest = load_guest(guest_name)

    # if loaded_guest:
    #     print(f"\nLoaded Guest:")
    #     print(type(loaded_guest))
    #     print(f"Name: {loaded_guest.name}")
    #     print(f"Question: {loaded_guest.question}")
    #     print(f"Answers: {loaded_guest.answers}")
    #     print(f"Right Answer: {loaded_guest.right_answer}")
    #     print(f"Explaination: {loaded_guest.explaination}")

    
if __name__ == "__main__":
    main()