import os
from logging.config import fileConfig
from dotenv import load_dotenv

from sqlalchemy import create_engine, pool
from alembic import context

from app import config as app_config
from app.database.metrics import Base

# Load Alembic admin env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env_migrations")
load_dotenv(dotenv_path)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

# Build database URL from environment variables
DB_USER = os.environ.get("METRICS_DB_ADMIN_USER", "admin_user")
DB_PASSWORD = os.environ.get("METRICS_DB_ADMIN_PASSWORD", "admin_password")
DB_HOST = os.environ.get("METRICS_DB_HOST", "192.168.0.218")
DB_PORT = os.environ.get("METRICS_DB_PORT", "5432")
DB_NAME = os.environ.get("METRICS_DB_NAME", "reporting")

METRICS_DB_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise RuntimeError("Missing required DB env variables for Alembic migrations")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=METRICS_DB_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="public",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        METRICS_DB_URI,
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="public",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
