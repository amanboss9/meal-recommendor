from typing import List
from flask import abort
from database.db import GraphDB
import logging

logger = logging.getLogger('Meal')


class Meal:
    @staticmethod
    def get_recommended_meals(user_id, cuisines: List[str], medical_conditions: List[str], allergies: List[str]):
        try:
            assert isinstance(cuisines, List)
            assert isinstance(medical_conditions, List)
            assert isinstance(allergies, List)

            graph = GraphDB.graph()
            query = """
            WITH %s as allergies, %s as medical_condition, %s as cuisines
            MATCH (u:User{user_id:%s}),(f:Food),
            (f)-[:GOOD_FOR]->(a:Allergy),
            (f)-[:GOOD_FOR]->(md:MedicalCondition),
            (f)-[:PART_OF]->  (cs:Cuisine)
            WHERE (u)-[:LIKES|:EATEN_UP]->(f) AND a.name IN allergies OR md.name IN medical_condition OR cs.name IN cuisines
            WITH f
            MATCH (m:Meal)<-[:PART_OF]-(f:Food) RETURN DISTINCT m.name LIMIT 10""" % (
                allergies, medical_conditions, cuisines, user_id)
            results = graph.run(query).data()
            print(results)
            return results
        except AssertionError:
            return abort(status=400, body={'error': {'message': 'Invalid input'}})
        except Exception as e:
            logger.error(e)
            return abort(status=400, body={'error': {'message': 'Something went wrong!'}})
