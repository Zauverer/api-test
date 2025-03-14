from utils import get, post, auth
from typing import List, Dict
from collections import Counter

class Dog:
    def __init__(self, id: int, name: str, breed: int):
        self.id = id
        self.name = name
        self.breed = breed

class Breed:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.dogs: List[Dog] = []

    def add_dog(self, dog: Dog):
        self.dogs.append(dog)

    def dogs_count(self) -> int:
        return len(self.dogs)

class DogHouse:
    def __init__(self):
        self.breeds: Dict[int, Breed] = {}
        self.dogs: List[Dog] = []

    def fetch_paginated_data(self, endpoint: str, token: str) -> List[Dict]:
        data = []
        url = f"https://dom.domain.cl/api/v1{endpoint}"
        while url:
            response = get(url, token)
            data.extend(response.get("results", []))
            url = response.get("next")
        return data

    def get_data(self, token: str):
        breeds_data = self.fetch_paginated_data("/breeds/", token)
        dogs_data = self.fetch_paginated_data("/dogs/", token)

        for breed in breeds_data:
            self.breeds[breed["id"]] = Breed(id=breed["id"], name=breed["name"])

        for dog in dogs_data:
            new_dog = Dog(id=dog["id"], name=dog["name"], breed=dog["breed"])
            self.dogs.append(new_dog)
            if new_dog.breed in self.breeds:
                self.breeds[new_dog.breed].add_dog(new_dog)

    def get_total_breeds(self) -> int:
        return len(self.breeds)

    def get_total_dogs(self) -> int:
        return len(self.dogs)

    def get_common_breed(self) -> Breed:
        if not self.breeds:
            return None
        return max(self.breeds.values(), key=lambda breed: breed.dogs_count())

    def get_common_dog_name(self) -> str:
        if not self.dogs:
            return ""
        name_counts = Counter(dog.name for dog in self.dogs)
        return name_counts.most_common(1)[0][0]

    def send_data(self, data: dict, token: str):
        post("https://dom.domain.cl/api/v1/answer/", data, token)
    
    def print_results(self):
        total_breeds = self.get_total_breeds()
        total_dogs = self.get_total_dogs()
        common_breed = self.get_common_breed()
        common_dog_name = self.get_common_dog_name()

        print(f"Total breeds: {total_breeds}")
        print(f"Total dogs: {total_dogs}")
        print(f"Most common breed name: {common_breed.name if common_breed else 'N/A'}")
        print(f"Most common dog name: {common_dog_name}")

if __name__ == "__main__":
    token = ""

    
    dog_house = DogHouse()
    dog_house.get_data(token)
    dog_house.print_results()
