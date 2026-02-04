import pandas as pd
from pandas import DataFrame
from typing import Tuple

import sqlite3
import os

class MatchingUtilities:

    def __init__(self, path: str = "db.sqlite3", table_name: str = "applicant"):
        self.path = path
        self.table_name = table_name

    def connect_db_and_get_table(self, table_name: str) -> DataFrame:
        """
        Connects to a SQLite database and retrieves all data from the specified table.

        Args:
            path (str): The file path to the SQLite database.
            table_name (str): The name of the table to retrieve data from.

        Returns:
            pd.DataFrame: A pandas DataFrame containing all data from the specified table.
        """
        with sqlite3.connect(self.path) as db:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", db)
        return df

    def filter_applicant(self, data: DataFrame) -> DataFrame:
        """
        Filters out applicants who have either quit or are marked for exclusion.
        Args:
            data (DataFrame): The input DataFrame containing applicant data.
                            It must have columns "quitted" and "exclude" with boolean values.
        Returns:
            DataFrame: A DataFrame containing only the applicants who have not quit and are not marked for exclusion.
        """
        df = data
        if "quitted" in data.columns:
            df = df[df["quitted"] == 0]
        if "exclude" in data.columns:
            df = df[df["exclude"] == 0]
        if "payment_id" in data.columns:
            df = df[~df["payment_id"].isnull()]
        if "grade" in data.columns:
            df = df[
                ~df["grade"].isin(["PROF", "GRAD"])
            ]  # exclude professors and graduated participants
        df = df.drop(columns=["quitted", "exclude", "payment_id"])
        return df

    def prepare_data(self, data: DataFrame) -> DataFrame:
        """
        Prepares the input DataFrame by converting the created_at column to the local timezone,
        and converting the timezone column to the local timezone.
        Args:
            data (DataFrame): The input DataFrame containing applicant data.
        Returns:
            DataFrame: A DataFrame containing the prepared data.
        """
        df = data[
            [
                "id",
                "sex",
                "grade",
                "wxid",
                "school",
                "timezone",
                "location",
                "mbti_ei",
                "mbti_sn",
                "mbti_tf",
                "mbti_jp",
                "preferred_sex",
                "preferred_grades",
                "preferred_schools",
                "max_time_difference",
                "same_location_only",
                "preferred_mbti_ei",
                "preferred_mbti_sn",
                "preferred_mbti_tf",
                "preferred_mbti_jp",
                "preferred_wxid",
                "continue_match",
                # "message_to_partner",
                "comment",
                "hobbies",
                "fav_movies",
                "wish",
                "why_lamp_remembered_your_name",
                "weekend_arrangement",
                "reply_frequency",
                "expectation",
            ]
        ]
        df["timezone"] = data["timezone"].map(lambda x: int(x[3:]))
        df["preferred_grades"] = data["preferred_grades"].map(lambda x: x.split(" | "))
        df["preferred_schools"] = data["preferred_schools"].map(
            lambda x: x.split(" | ")
        )
        df["hobbies"] = data["hobbies"].map(lambda x: [text.strip() for text in x.split(" | ")])
        df["fav_movies"] = data["fav_movies"].map(lambda x: [text.strip() for text in x.split(" | ")])
        
        return df

    def separate_groups(
        self, data: DataFrame
    ) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
        """
        Separates the input DataFrame into four groups based on sex and preferred sex.

        Args:
            data (DataFrame): The input DataFrame containing user data with at least two columns:
                            'sex' and 'preferred_sex'.

        Returns:
            Tuple[DataFrame, DataFrame, DataFrame, DataFrame]: A tuple containing four DataFrames:
                - heterosexual_female_list: Users who are female and prefer males.
                - heterosexual_male_list: Users who are male and prefer females.
                - homosexual_female_list: Users who are female and prefer females.
                - homosexual_male_list: Users who are male and prefer males.
        """
        FM_df = data[
            (data["sex"] == "F") & (data["sex"] != data["preferred_sex"])
        ].reset_index(drop=True)
        MF_df = data[
            (data["sex"] == "M") & (data["sex"] != data["preferred_sex"])
        ].reset_index(drop=True)
        FF_df = data[
            (data["sex"] == "F") & (data["sex"] == data["preferred_sex"])
        ].reset_index(drop=True)
        MM_df = data[
            (data["sex"] == "M") & (data["sex"] == data["preferred_sex"])
        ].reset_index(drop=True)
        return FM_df, MF_df, FF_df, MM_df

    def reshuffle_data(self, data: DataFrame) -> DataFrame:
        """
        Reshuffles the input DataFrame to ensure that the data is not sorted by any column.
        """
        return data.sample(frac=1).reset_index(drop=True)

    def load_and_clean_data(self) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
        """
        Loads and cleans the data from the input path.
        Args:
            path (str): The path to the data file.
        Returns:
            Tuple[DataFrame, DataFrame, DataFrame, DataFrame]: A tuple containing four DataFrames:
                - heterosexual_female_list: Users who are female and prefer males.
                - heterosexual_male_list: Users who are male and prefer females.
                - homosexual_female_list: Users who are female and prefer females.
                - homosexual_male_list: Users who are male and prefer males.
        """
        df = self.connect_db_and_get_table(self.table_name)
        df = self.filter_applicant(df)
        df = self.prepare_data(df)
        # df = self.reshuffle_data(df)
        return self.separate_groups(df)

class DataLoader:
    def __init__(self, path: str = "./embedded_data/"):
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
    
    def load_data(self, name: str) -> DataFrame:
        return pd.read_pickle(self.path + name + ".pkl")
    
    def save_data(self, df: DataFrame, name: str) -> None:
        df.to_pickle(self.path + name + ".pkl")
        print(f"Saved DataFrame to {self.path + name + ".pkl"}")
        return df