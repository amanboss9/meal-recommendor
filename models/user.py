from database.db import GraphDB


class User:
    @staticmethod
    def register_user(name, age):
        graph = GraphDB.graph()
        query = """
        MERGE (u: User) ON CREATE SET u.count = 1 ON MATCH SET u.count = u.count + 1 WITH u.count AS uid 
        CREATE (user:User{user_id: uid, name:'%s', age:'%s' }) RETURN user
        """ % (name, age)
        results = graph.run(query).data()
        return results
