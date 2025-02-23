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

class RescueCenter:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def adopt_animal(self, animal_name):
        for animal in self.animals:
            if animal.name == animal_name:
                if animal.adopted:
                    return f"{animal_name} is already adopted."
                else:
                    animal.adopt()
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