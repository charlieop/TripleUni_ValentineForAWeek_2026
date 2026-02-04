from sentence_transformers import SentenceTransformer
import pandas as pd
from pandas import DataFrame
import numpy as np

class EmbeddingUtilities:
    def __init__(self, model: SentenceTransformer):
        
        self.model = model

    def transform(self, df: DataFrame) -> DataFrame:
        df = self._get_embeddings_for_column_list(df, "hobbies")
        df = self._get_embeddings_for_column_list(df, "fav_movies")
        df = self._get_embeddings_for_column(df, "why_lamp_remembered_your_name")
        df = self._get_embeddings_for_column(df, "expectation")
        df = self._get_embeddings_for_column(df, "weekend_arrangement")
        df = self._get_embeddings_for_column(df, "wish")
        return df
    
    def _find_unique_texts_from_column(self, df: pd.Series, column: str) -> set[str]:
        print(f"Finding unique texts from column {column}")
        all_texts = set()
        for texts in df[column]:
            all_texts.update(texts)
        print(f"Found {len(all_texts)} unique texts")
        return all_texts
        
    def _get_embeddings(self, texts: list[str]) ->np.ndarray:
        return self.model.encode(texts)
    
    def _get_embeddings_for_column_list(self, df: DataFrame, column: str) -> DataFrame:
        print(f"Getting embeddings for column {column}")
        all_texts = list(
            self._find_unique_texts_from_column(df, column)
        )
        all_texts_embeddings = self._get_embeddings(all_texts)
        texts_to_index = {text: index for index, text in enumerate(all_texts)}
        
        df[f"{column}_embeddings"] = df[column].map(
            lambda x: np.array([all_texts_embeddings[texts_to_index[text]] for text in x])
        )
        print(f"Saved embeddings to column {f"{column}_embeddings"}")
        return df
    
    def _get_embeddings_for_column(self, df: DataFrame, column: str) -> DataFrame:
        print(f"Getting embeddings for column {column}")
        texts = [text.strip() for text in df[column]]
        texts_embeddings = self._get_embeddings(texts)  # shape (n_rows, embedding_dim)
        df[f"{column}_embeddings"] = [np.asarray(texts_embeddings[i]) for i in range(len(texts_embeddings))]
        print(f"Saved embeddings to column {f"{column}_embeddings"}")
        return df
    