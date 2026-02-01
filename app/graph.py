import os
import logging
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class GraphManager:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None

    def connect(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.verify_connectivity()
            logger.info("Connected to Neo4j Graph Database")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def verify_connectivity(self):
        if self.driver:
            self.driver.verify_connectivity()

    def close(self):
        if self.driver:
            self.driver.close()

    def clear_database(self):
        """
        Deletes all nodes and relationships in the database.
        Use with caution!
        """
        if not self.driver:
            self.connect()
            
        if not self.driver:
            logger.error("Cannot clear database: No active connection")
            return False
            
        try:
            query = "MATCH (n) DETACH DELETE n"
            self.driver.execute_query(query, database_="neo4j")
            logger.warning("CLEARED ENTIRE KNOWLEDGE GRAPH")
            return True
        except Exception as e:
            logger.error(f"Failed to clear database: {e}")
            return False

    def query(self, query: str, parameters: dict = None, db: str = None):
        if not self.driver:
            self.connect()
        
        if not self.driver:
            logger.error("Cannot execute query: No active Neo4j driver connection.")
            return None

        try:
            result = self.driver.execute_query(
                query, 
                parameters_=parameters, 
                database_=db, 
                result_transformer_=lambda r: r.data()
            )
            return result
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None

    def ingest_note(self, note: 'ProcessedNote', file_path: str):
        if not self.driver:
            self.connect()
        
        if not self.driver:
            logger.warning("Skipping graph ingestion: No database connection")
            return

        query = """
        MERGE (c:Category {name: $category})
        MERGE (s:SubCategory {name: $subcategory})
        MERGE (s)-[:IS_A]->(c)
        
        MERGE (n:Note {title: $title})
        SET n.summary = $summary,
            n.filename = $filename,
            n.filepath = $file_path,
            n.updated_at = datetime()
            
        MERGE (n)-[:BELONGS_TO]->(s)
        
        FOREACH (tagName IN $tags | 
            MERGE (t:Tag {name: tagName})
            MERGE (n)-[:HAS_TAG]->(t)
        )
        """
        
        params = {
            "category": note.category.value,
            "subcategory": note.subcategory,
            "title": note.title,
            "summary": note.summary,
            "filename": note.suggested_filename,
            "file_path": file_path,
            "tags": note.tags
        }
        
        try:
            self.driver.execute_query(query, parameters_=params, database_="neo4j")
            logger.info(f"Ingested note '{note.title}' into Knowledge Graph")
        except Exception as e:
            logger.error(f"Failed to ingest note into graph: {e}")

    async def query_knowledge_graph(self, cypher_query: str) -> str:
        """
        Executes a Read-Only Cypher query against the knowledge graph.
        Use this tool to answer questions about the user's notes, projects, areas, and tags.
        Example queries:
        - MATCH (n:Note)-[:BELONGS_TO]->(p:SubCategory {name: 'Project Alpha'}) RETURN n.title, n.summary
        - MATCH (t:Tag {name: 'important'})<-[:HAS_TAG]-(n:Note) RETURN n.title
        """
        if not self.driver:
            self.connect()
        
        # Security check: Simple validation to prevent mutations
        forbidden_keywords = ["MERGE", "CREATE", "DELETE", "SET", "REMOVE", "DROP", "DETACH"]
        if any(keyword in cypher_query.upper() for keyword in forbidden_keywords):
            return "Error: Only read-only queries (MATCH, RETURN) are allowed."

        try:
            results = self.driver.execute_query(
                cypher_query, 
                database_="neo4j", 
                result_transformer_=lambda r: r.data()
            )
            return str(results)
        except Exception as e:
            return f"Query failed: {e}"

# Global instance
graph = GraphManager()
