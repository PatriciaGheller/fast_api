from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine

from src.config import settings
from src.database import metadata  # apenas o metadata, não o engine
from src.models.post import posts  # noqa

# Configuração do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata

def run_migrations_offline() -> None:
    url = settings.database_url.replace("sqlite+aiosqlite", "sqlite")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    sync_url = settings.database_url.replace("sqlite+aiosqlite", "sqlite")
    connectable = create_engine(sync_url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
