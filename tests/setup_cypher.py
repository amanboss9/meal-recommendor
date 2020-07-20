import random
import string
from py2neo import Graph

graph = Graph(password="admin")


def get_food_name(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


def get_meal_name(size=8, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))


class SetupDB:
    def __init__(self, num_of_food, num_of_meals):
        self.graph_gist = "CREATE "
        self.number_of_food_items = num_of_food
        self.number_of_meals = num_of_meals
        self.number_of_users = 5  # Minimum 1 user and max of 5 user.
        self.food_ids = []
        self.meal_ids = []
        self.cuisine_ids = []
        self.allergy_ids = []
        self.medical_condition_ids = []
        self.user_ids = []
        self.init()

    def init(self):
        self.create_food_nodes()
        self.create_meal_nodes()
        self.create_meal_food_relationship()
        self.create_cuisine_nodes()
        self.create_allergy_nodes()
        self.create_medical_condition_node()
        self.create_cuisine_food_relationship()
        self.create_allergy_food_relationship()
        self.create_medical_cond_food_relationship()
        self.create_user_node()
        self.create_user_food_relationships()

    def get_cypher_query(self):
        return self.graph_gist

    def create_food_nodes(self):
        self.graph_gist += """
        //foods 
        """
        for i in range(self.number_of_food_items):
            a1 = random.randint(1, 10)
            a2 = random.randint(1, 10)
            a3 = random.randint(1, 10)
            protein = (a1 / (a1 + a2 + a3))
            carbs = (a2 / (a1 + a2 + a3))
            fats = (a3 / (a1 + a2 + a3))
            line = """(food_%s:Food {food_id: %s,name: "%s", protein:%.2f, carb:%.2f, fat:%.2f}),\n"""
            line = line % (i, i, get_food_name().title(), protein, carbs, fats)
            self.food_ids.append(f"food_{i}")
            self.graph_gist += line

    def create_meal_nodes(self):
        self.graph_gist += """//meals 
        """

        for i in range(self.number_of_meals):
            line = """(meal_%s:Meal {name: "%s"}),\n"""
            line = line % (i, get_meal_name().title())
            self.meal_ids.append(f"meal_{i}")
            self.graph_gist += line

    def create_meal_food_relationship(self):
        self.graph_gist += """//meal-food relationship 
        """
        for i in range(len(self.meal_ids)):
            f = random.randint(1, 5)  # Maximum of 5 foods allowed in a meal
            chosen_food = []
            for j in range(f):
                random_food_id = random.randint(0, len(self.food_ids) - 1)
                if random_food_id not in chosen_food:
                    chosen_food.append(random_food_id)
                    #             line="""(%s) - [:INCLUDES] -> (%s),\n"""
                    #             line = line % (meal_ids[i], food_ids[random_food_id])
                    #             gist+=line
                    line = """(%s) - [:PART_OF] -> (%s),\n"""
                    line = line % (self.food_ids[random_food_id], self.meal_ids[i])
                    self.graph_gist += line

    def create_cuisine_nodes(self):
        self.graph_gist += """// cuisines
        """
        cuisines = ['Mexican', 'Italian', 'Indian', 'Korean', 'Japanese', 'Chinese', 'Thai', 'American', 'French',
                    'Middle East', 'Veg', 'Non Veg', 'South Indian', 'North Indian', 'Assamese', 'Gujrati', 'Kannada',
                    'Tamil',
                    'Punjabi', 'Bengali']

        for i in range(len(cuisines)):
            self.cuisine_ids.append(f"cuisine_{i}")
            self.graph_gist += """(cuisine_%s:Cuisine {name: "%s"}),\n""" % (i, cuisines[i])

    def create_allergy_nodes(self):
        self.graph_gist += """// Allergies
        """
        allergies = ['Eggs', 'Milk', 'Soy', 'Chicken', 'Nuts', 'Peanut', 'Pork', 'Cheese', 'Wheat', 'Honey']
        for i in range(len(allergies)):
            self.allergy_ids.append(f"allergy_{i}")
            self.graph_gist += """(allergy_%s:Allergy {name: "%s"}),\n""" % (i, allergies[i])

    def create_medical_condition_node(self):
        self.graph_gist += """// Medical Conditions
        """
        medical_conditions = ['Anaemia', 'Iron', 'Weak Bones', 'Obesity', 'Migrane', 'Diabetes', 'Lactose',
                              'Joint Pain',
                              'Heart', 'Spinal']
        for i in range(len(medical_conditions)):
            self.medical_condition_ids.append(f"med_condition_{i}")
            self.graph_gist += """(med_condition_%s:MedicalCondition {name: "%s"}),\n""" % (i, medical_conditions[i])

    def create_cuisine_food_relationship(self):
        self.graph_gist += """//Cuisine-food relationship 
        """

        for i in range(len(self.food_ids)):
            random_cuisine = random.randint(1, len(self.cuisine_ids) - 1)
            self.graph_gist += """(%s) - [:PART_OF] -> (%s),\n""" % (self.food_ids[i], self.cuisine_ids[random_cuisine])

    def create_allergy_food_relationship(self):
        self.graph_gist += """//Allergy-food relationship 
        """
        for i in range(len(self.food_ids)):
            chosen = []
            for j in range(3):
                boolean = bool(random.getrandbits(1))
                random_index = random.randint(1, len(self.allergy_ids) - 1)
                if random_index not in chosen:
                    chosen.append(random_index)
                    if boolean:
                        self.graph_gist += """(%s) - [:GOOD_FOR] -> (%s),\n""" % (
                            self.food_ids[i], self.allergy_ids[random_index])
                    else:
                        self.graph_gist += """(%s) - [:BAD_FOR] -> (%s),\n""" % (
                            self.food_ids[i], self.allergy_ids[random_index])

    def create_medical_cond_food_relationship(self):
        self.graph_gist += """//Medical Condition-food relationship 
        """

        for i in range(len(self.food_ids)):
            chosen = []
            for j in range(3):
                boolean = bool(random.getrandbits(1))
                random_index = random.randint(1, len(self.medical_condition_ids) - 1)
                if random_index not in chosen:
                    chosen.append(random_index)
                    if boolean:
                        self.graph_gist += """(%s) - [:GOOD_FOR] -> (%s),\n""" % (
                            self.food_ids[i], self.medical_condition_ids[random_index])
                    else:
                        self.graph_gist += """(%s) - [:BAD_FOR] -> (%s),\n""" % (
                            self.food_ids[i], self.medical_condition_ids[random_index])

    def create_user_node(self):
        self.graph_gist += """// Users
        """
        user_names = ['Amit Sharma', 'Mithun D', 'Salman', 'Aman Sharma', 'Gunjan'][0:self.number_of_users]
        for i in range(len(user_names)):
            self.user_ids.append(f"user_{i}")
            self.graph_gist += """(user_%s:User {user_id: %s, name: "%s"}),\n""" % (i, i, user_names[i])

    def create_user_food_relationships(self):
        self.graph_gist += """//User-food likes- Dislikes and eaten - similar to eat relationship 
        """
        for i in range(len(self.user_ids)):
            random_likes = random.randint(4, 10)
            chosen = []
            for j in range(random_likes):
                random_index = random.randint(0, len(self.food_ids) - 1)
                if random_index not in chosen:
                    chosen.append(random_index)
                    self.graph_gist += """(%s) - [:LIKES] -> (%s),\n""" % (
                        self.user_ids[i], self.food_ids[random_index])

            random_dislikes = random.randint(2, 8)
            dislike_chosen = []
            for j in range(random_dislikes):
                random_index = random.randint(0, len(self.food_ids) - 1)
                if random_index not in chosen:
                    chosen.append(random_index)
                    dislike_chosen.append(random_index)
                    self.graph_gist += """(%s) - [:DISLIKES] -> (%s),\n""" % (
                        self.user_ids[i], self.food_ids[random_index])

            user_eaten = []
            random_eaten = random.randint(4, 10)
            for j in range(random_eaten):
                random_index = random.randint(0, len(self.food_ids) - 1)
                if random_index not in dislike_chosen:
                    self.graph_gist += """(%s) - [:EATEN_UP] -> (%s),\n""" % (
                        self.user_ids[i], self.food_ids[random_index])
                    user_eaten.append(self.food_ids[random_index])

            similar_to_eat = random.randint(2, 4)
            similar_foods = []
            for j in range(similar_to_eat):
                random_index = random.randint(0, len(self.food_ids) - 1)
                if self.food_ids[random_index] not in user_eaten:
                    similar_foods.append(self.food_ids[random_index])

            for sim in similar_foods:
                for j in user_eaten:
                    self.graph_gist += """(%s) - [:SIMILAR_TO] -> (%s),\n""" % (
                        sim, j)

        self.graph_gist = self.graph_gist[:-2]
