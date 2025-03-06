class Animal:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
        self.adopted = False

    def adopt(self):
        self.adopted = True

    def __str__(self):
        return f"Name: {self.name}, Species: {self.species}, Age: {self.age}, Adopted {self.adopted}"

import csv
class RescueCenter:
    def __init__(self):
        self.animals = []
        self.load_animals_from_csv("animals.csv")

    def load_animals_from_csv(self, filename):
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row["name"]
                    species = row["species"]
                    age = int(row["age"])
                    adopted = row ["adopted"].lower() == "true"
                    animal = Animal(name, species, age)
                    animal.adopted = adopted

                    if adopted and row["adopter_name"]:
                        adopter = Adopter(row["adopter_name"], row["adopter_email"], row["adopter_phone"], row["adopter_address"])
                        adopter.adopt(animal)
                        animal.adopter = adopter

                    self.animals.append(animal)
        except FileNotFoundError:
            print("CSV file not found.")
    
    def save_animals_to_csv(self, filename="animals.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "species", "age", "adopted", "adopter_name", "adopter_email", "adopter_phone", "adopter_address"])

            for animal in self.animals:
                adopter = animal.adopter if hasattr(animal, "adopter") else None
                writer.writerow([animal.name, animal.species, animal.age, animal.adopted, adopter.name if adopter else "", adopter.email if adopter else "", adopter.phone if adopter else "", adopter.address if adopter else ""])


    def add_animal(self, animal):
        self.animals.append(animal)
        self.save_animals_to_csv()

    def adopt_animal(self, animal_name):
        for animal in self.animals:
            if animal.name == animal_name:
                if animal.adopted:
                    return f"{animal_name} is already adopted."
                else:
                    animal.adopt()
                    self.save_animals_to_csv()
                    return f"{animal_name} is available for adoption!"
        return f"{animal_name} is not in the rescue center."
    
class Adopter:
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.adopted_animals = []

    def adopt(self, animal):
        if animal not in self.adopted_animals:
            self.adopted_animals.append(animal)
            animal.adopt()

    def __str__(self):
        adopted_names = [animal.name for animal in self.adopted_animals]
        return (f"Adopter: {self.name}\n"
                f"Email: {self.email}\n"
                f"Phone: {self.phone}\n"
                f"Address: {self.address}\n"
                f"Animals Adopted: {adopted_names}")
    
import tkinter as tk
from tkinter import messagebox

class animal_rescue_gui:
    def __init__(self, root, rescue_center):
        self.root = root
        self.root.title("Animal Rescue Management System")
        self.rescue_center = rescue_center
        
        #Label and entry fields
        tk.Label(root, text="Animal Name:").grid(row=0, column=0)
        self.animal_name_entry = tk.Entry(root)
        self.animal_name_entry.grid(row=0, column=1)
        #Label and entry fields
        tk.Label(root, text="Species:").grid(row=1, column=0)
        self.species_entry = tk.Entry(root)
        self.species_entry.grid(row=1, column=1)
        #Label and entry fields
        tk.Label(root, text="Age:").grid(row=2, column=0)
        self.age_entry = tk.Entry(root)
        self.age_entry.grid(row=2, column=1)
        #Label and entry fields
        tk.Label(root, text="Adopter Name:").grid(row=7, column=0)
        self.adopter_name_entry = tk.Entry(root)
        self.adopter_name_entry.grid(row=7, column=1)
        #Label and entry fields
        tk.Label(root, text="Email:").grid(row=8, column=0)
        self.adopter_email_entry = tk.Entry(root)
        self.adopter_email_entry.grid(row=8, column=1)
        #Label and entry fields
        tk.Label(root, text="Phone:").grid(row=9, column=0)
        self.adopter_phone_entry = tk.Entry(root)
        self.adopter_phone_entry.grid(row=9, column=1)
        #Label and entry fields
        tk.Label(root, text="Address:").grid(row=10, column=0)
        self.adopter_address_entry = tk.Entry(root)
        self.adopter_address_entry.grid(row=10, column=1)

        #Buttons
        tk.Button(root, text="Add Animal", command=self.add_animal).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="List Animals", command=self.list_animals).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Assign Adopter", command=self.adopt_animal).grid(row=11, column=0, columnspan=2)

        #box for displaying animals
        self.animals_listbox = tk.Listbox(root, width=150, height=20)
        self.animals_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def add_animal(self):
        name = self.animal_name_entry.get()
        species = self.species_entry.get()
        age = self.age_entry.get()

        if name and species and age.isdigit():
            age_int = int(age)
            if age_int <= 0:
                messagebox.showerror("Age must be a positive number")
            elif age_int > 20:
                messagebox.showerror("Age is too large")
            else:
                animal = Animal(name, species, int(age))
                self.rescue_center.add_animal(animal)
                messagebox.showinfo("Success", f"{name} added to the rescue center!")
        else:
            messagebox.showerror("Error", "Please enter valid animal details.")

    def list_animals(self):
        self.animals_listbox.delete(0, tk.END)
        not_adopted_animals = [animal for animal in self.rescue_center.animals if not animal.adopted]
        adopted_animals = [animal for animal in self.rescue_center.animals if animal.adopted]
        
        not_adopted_animals.sort(key=lambda x: x.name.lower())
        adopted_animals.sort(key=lambda x: x.name.lower())

        for animal in not_adopted_animals:
            self.animals_listbox.insert(tk.END, f"{animal.name} - {animal.species} - Age: {animal.age} - Adopted: {animal.adopted}")
        
        for animal in adopted_animals:
            adopter_info = ""
            if animal.adopted and hasattr(animal, "adopter") and animal.adopter:
                adopter = animal.adopter
                adopter_info = f" | Adopter: {adopter.name} | Email: {adopter.email} | Phone: {adopter.phone} | Address: {adopter.address}"
            self.animals_listbox.insert(tk.END, f"{animal.name} - {animal.species} - Age: {animal.age} - Adopted: {animal.adopted}{adopter_info}")

            

    def adopt_animal(self):
        name = self.animal_name_entry.get()
        adopter_name = self.adopter_name_entry.get()
        adopter_email = self.adopter_email_entry.get()
        adopter_phone = self.adopter_phone_entry.get()
        adopter_address = self.adopter_address_entry.get()

        for animal in self.rescue_center.animals:
            if animal.name == name:
                if animal.adopted:
                    messagebox.showerror("Error", f"{name} is already adopted!")
                    return
                adopter = Adopter(adopter_name, adopter_email, adopter_phone, adopter_address)
                adopter.adopt(animal)  
                animal.adopter = adopter

                self.rescue_center.save_animals_to_csv()
                messagebox.showinfo("Success", f"{name} has been adopted by {adopter_name}!")
                self.list_animals()
                return
        messagebox.showerror("Error", f"{name} not found in the rescue center.")


if __name__ == "__main__":
    root = tk.Tk()
    rescue_center = RescueCenter()
    gui = animal_rescue_gui(root, rescue_center)
    root.mainloop()