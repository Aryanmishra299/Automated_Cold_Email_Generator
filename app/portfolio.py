import pandas as pd
import chromadb
import uuid


class portfolio:

    def __init__(self, file_path='app/resource/My_Skill_Stack.csv'):

        self.file_path = file_path

        self.data = pd.read_csv(file_path)

        self.client = chromadb.PersistentClient('VectorStore')

        self.collection = self.client.get_or_create_collection(
            name="JOB_Applying"
        )

    def load_portfolio(self):

        if self.collection.count() == 0:

            for _, row in self.data.iterrows():

                self.collection.add(
                    documents=[row['Techstack']],
                    metadatas=[{'links': row['Projects']}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):

        skills_text = ", ".join(skills)

        results = self.collection.query(
            query_texts=[skills_text],
            n_results=2
        )

        return results.get('metadatas', [])