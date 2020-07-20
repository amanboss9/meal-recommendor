# meal-recommendor

### Sample graph nodes and relations
![alt text](https://github.com/amanboss9/meal-recommendor/blob/master/assets/img/graph.jpeg?raw=true)

* Benchmark for deleting, adding and matching from graph database for respective nodes. 

![alt text](https://github.com/amanboss9/meal-recommendor/blob/master/assets/img/test_results.jpeg?raw=true)

### Relationship between nodes

 - Food -[:PART_OF]-> Meal
 - Food -[:PART_OF]-> Cuisine
 - Food -[:GOOD_FOR]-> Allergy
 - Food -[:BAD_FOR]-> Allergy
 - Food -[:GOOD_FOR]-> MedicalCondition
 - Food -[:BAD_FOR]-> MedicalCondition
 - User -[:LIKES]-> Food
 - User -[:DISLIKES]-> Food
 - User -[:EATEN_UP]-> Food
 - Food -[:SIMILAR_TO]-> Food
 