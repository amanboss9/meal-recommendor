from sys import stderr
from threading import Thread
from timeit import default_timer as time
from tests.setup_cypher import SetupDB
from neo4j import GraphDatabase


class Runner(Thread):

    def __init__(self, food_nodes_size, meal_nodes_size):
        super(Runner, self).__init__()
        self.size = 10000
        self.batch_size = 20000
        self.food_nodes_size = food_nodes_size
        self.meal_nodes_size = meal_nodes_size
        self.driver = GraphDatabase.driver("bolt://localhost:7687/", auth=("neo4j", "admin"))

    def run(self):
        self.drop_index()
        self.delete_all()
        self.create_graph()
        self.create_index()
        self.match_nodes()

    def drop_index(self):
        with self.driver.session() as session:
            try:
                session.run("DROP CONSTRAINT ON (f:Food) ASSERT f.food_id IS UNIQUE").consume()
                session.run("DROP CONSTRAINT ON (u:User) ASSERT u.user_id IS UNIQUE").consume()
            except Exception as e:
                print(e)
                pass

    def delete_all(self):
        t0 = time()
        with self.driver.session() as session:
            total_nodes_deleted = 0
            deleting = True
            while deleting:
                summary = session.run(
                    f"""MATCH (a) WITH a LIMIT {self.batch_size} DETACH DELETE a RETURN count(a) as count""").data()
                total_nodes_deleted += summary[0].get('count')
                stderr.write("Deleted %d nodes\r" % total_nodes_deleted)
                deleting = bool(summary[0].get('count'))
            t1 = time()
            stderr.write("Deleted %d nodes in %fs\n" % (total_nodes_deleted, t1 - t0))

    def create_graph(self):
        t0 = time()
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                query = SetupDB(self.food_nodes_size, self.meal_nodes_size).get_cypher_query()
                tx.run(query)
            t1 = time()
            with session.begin_transaction() as tx:
                nodes_updated = tx.run("""MATCH (n) RETURN count(n) as count""").data()
                stderr.write("Created %d nodes in %fs\n" % (nodes_updated[0].get('count'), t1 - t0))

    def create_index(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT ON (n:Food) ASSERT n.food_id IS UNIQUE").consume()
            session.run("CREATE CONSTRAINT ON (n:User) ASSERT n.user_id IS UNIQUE").consume()

    def match_nodes(self):
        t0 = time()
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                n = 0
                result = tx.run("MATCH (a:Food) RETURN a")
                for n, record in enumerate(result, 1):
                    _ = record["a"]
                    if n % self.batch_size == 0:
                        stderr.write("Matched %d nodes\r" % n)
                t1 = time()
                stderr.write("Matched %d nodes in %fs\n" % (n, t1 - t0))

    def test_get_meal_query(self):

        query = """
            WITH %s as allergies, %s as medical_condition, %s as cuisines
            MATCH (u:User{user_id:%d})-[:LIKES|:SIMILAR_TO_EAT|:EATEN_UP]->(f:Food),
            (f)-[:GOOD_FOR]->(a:Allergy),
            (f)-[:GOOD_FOR]->(md:MedicalCondition),
            (f)-[:PART_OF]->  (cs:Cuisine)
            WHERE a.name IN allergies OR md.name IN medical_condition OR cs.name IN cuisines
            WITH f MATCH (f)-[:PART_OF]-(m:Meal) return m.name"""
        q1 = query % ([], ['Diabetes', 'Joint Pain'], ['Kannada'], 0)
        q2 = query % (['Cheese'], [], [], 0)
        q3 = query % ([], [], ['Kannada'], 0)
        queries = [q1, q2, q3]

        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                for _q in queries:
                    count = 0
                    t0 = time()
                    result = tx.run(_q)
                    count += len(result.data())
                    t1 = time()
                    stderr.write("Get %d meals for user in %fs\n" % (count, t1 - t0))


if __name__ == "__main__":
    # run function is to stress test for deleting, creating and matching operations.
    # Runner(100, 500).run()
    Runner(100, 500).test_get_meal_query()
