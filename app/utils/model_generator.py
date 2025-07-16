"""
This module provides utilities to generate SQLAlchemy ORM model classes
from an existing database schema by reflecting the database metadata.

Functions:
    - generate_models_to_files(database_url, output_folder):
        Generates model class files for each table in the database schema.

    - get_column_type(column):
        Maps SQLAlchemy reflected column types to corresponding
        SQLAlchemy column type strings used in model declarations.
"""
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def generate_models_to_files(database_url, output_folder="app/models/primary"):
    """
        Generate SQLAlchemy ORM model class files from the database schema.

        Connects to the database specified by `database_url`, reflects the schema,
        and writes a Python file per table into the specified output folder.
        Each file contains a SQLAlchemy declarative model class representing the table,
        including columns and relationships inferred from foreign keys.

        Args:
            database_url (str): SQLAlchemy-compatible database URL to connect to.
            output_folder (str, optional): Directory path where generated model files
                will be saved. Defaults to "app/models/primary".

        Side Effects:
            Creates or overwrites Python files representing each table model
            in the `output_folder`.
            Also generates an `__init__.py` file importing all model classes.

        Prints:
            Status messages indicating which files have been generated.
    """
    engine = create_engine(database_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    os.makedirs(output_folder, exist_ok=True)

    base_imports = (
        "from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime\n"
        "from sqlalchemy.ext.declarative import declarative_base\n"
        "from sqlalchemy.orm import relationship\n\n"
        "Base = declarative_base()\n\n"
    )

    model_class_names = []

    for table_name, table in metadata.tables.items():
        class_name = ''.join(word.capitalize() for word in table_name.split('_'))
        file_path = os.path.join(output_folder, f"{class_name}.py")
        model_class_names.append(class_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(base_imports)
            f.write(f"class {class_name}(Base):\n")
            f.write(f"    __tablename__ = '{table_name}'\n\n")

            for column in table.columns:
                col_type = get_column_type(column)
                args = []
                if column.foreign_keys:
                    fk = list(column.foreign_keys)[0]
                    args.append(f"ForeignKey('{fk.target_fullname}')")
                if column.primary_key:
                    args.append('primary_key=True')
                if not column.nullable:
                    args.append('nullable=False')
                if column.default is not None:
                    args.append(f"default={column.default.arg}")
                args_string = ", ".join([col_type] + args)
                f.write(f"    {column.name} = Column({args_string})\n")

            added_relationships = set()
            for column in table.columns:
                if column.foreign_keys:
                    fk = list(column.foreign_keys)[0]
                    referred_table = fk.column.table.name
                    rel_name = referred_table

                    if rel_name not in added_relationships:
                        f.write(f"    {rel_name} = relationship('{referred_table.capitalize()}')\n")
                        added_relationships.add(rel_name)
            print(f" Generated: {file_path}")

    init_file_path = os.path.join(output_folder, "__init__.py")
    with open(init_file_path, "w", encoding="utf-8") as f:
        for class_name in model_class_names:
            f.write(f"from .{class_name} import {class_name}\n")
    print(f"Generated: {init_file_path}")


def get_column_type(column):
    """
        Map a reflected SQLAlchemy column to its corresponding SQLAlchemy type string.

        Args:
            column (sqlalchemy.Column): Reflected SQLAlchemy column object.

        Returns:
            str: The SQLAlchemy column type name as a string,
            such as 'Integer', 'String', 'Float', 'Boolean', or 'DateTime'.
            Defaults to 'String' if no type match is found.
    """
    col_type = str(column.type)
    if "INTEGER" in col_type:
        return "Integer"
    if "VARCHAR" in col_type or "TEXT" in col_type:
        return "String"
    if "FLOAT" in col_type or "NUMERIC" in col_type:
        return "Float"
    if "BOOLEAN" in col_type:
        return "Boolean"
    if "DATETIME" in col_type or "TIMESTAMP" in col_type:
        return "DateTime"
    return "String"
