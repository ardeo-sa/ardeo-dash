import os
import sys
import importlib
import pkgutil
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

# ensure project root is on sys.path so `import app` works when running the script
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()  # load .env so env vars like SERVICES_DB_* are available

# Determine DATABASE_URL, fallback to constructing from SERVICES_DB_* or sqlite
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    user = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASS")
    host = os.getenv("METRICS_DB_HOST", "localhost")
    name = os.getenv("METRICS_DB_NAME")
    port = os.getenv("METRICS_DB_PORT", "5432")
    if user and password and name:
        # create a sync psycopg2 URL for create_engine if Postgres vars are present
        DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    else:
        DATABASE_URL = "sqlite:///./dev.db"

# normalize async driver URLs to sync driver for create_engine
if DATABASE_URL.startswith("postgresql+asyncpg"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
logger.info("Using database URL: %s", DATABASE_URL)
engine: Engine = create_engine(DATABASE_URL, connect_args=connect_args)

# locate Base
Base = None
candidate_modules = [
    "app.db.base_class",
    "app.db.base",
    "app.database.base_class",
    "app.database.base",
    "app.db.base_model",
    "app.models",
    "app.models.base",
    "models",
]

for mod_path in candidate_modules:
    try:
        mod = importlib.import_module(mod_path)
    except Exception as exc:
        logger.debug("Skipping %s: import failed: %s", mod_path, exc)
        continue
    if hasattr(mod, "Base"):
        candidate = getattr(mod, "Base")
        if hasattr(candidate, "metadata"):
            Base = candidate
            logger.info("Found Base in %s", mod_path)
            break

def import_models_from(pkg_names):
    for pkg_name in pkg_names:
        try:
            pkg = importlib.import_module(pkg_name)
        except Exception as exc:
            logger.debug("Could not import package %s: %s", pkg_name, exc)
            continue
        if hasattr(pkg, "__path__"):
            for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
                try:
                    importlib.import_module(name)
                except Exception as exc:
                    # record which modules fail to import; they may have extra deps / side effects
                    logger.debug("Failed to import model module %s: %s", name, exc)

# import likely model packages (avoid importing app.main)
import_models_from([
    "app.models",
    "app.database.models",
    "app.db.models",
    "models",
    "app.calendar.models",
    "app.patients.models"
])

# fallback scan already-imported modules
if Base is None:
    for mod_name, mod in list(sys.modules.items()):
        try:
            if mod and hasattr(mod, "Base"):
                candidate = getattr(mod, "Base")
                if hasattr(candidate, "metadata"):
                    Base = candidate
                    logger.info("Found Base in already-imported module %s", mod_name)
                    break
        except Exception:
            continue

if Base is None:
    logger.error(
        "Could not locate SQLAlchemy Base. Ensure  is defined in a module such as "
        "`app.db.base_class` or that your models register a Base."
    )
    sys.exit(2)

def create_tables() -> None:
    """Create database tables for all registered models."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created.")
    except SQLAlchemyError as exc:
        logger.error("Failed to create tables: %s", exc)
        raise

if __name__ == "__main__":
    create_tables()