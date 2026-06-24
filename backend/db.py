#!/usr/bin/env python
"""
Utility script for database operations
"""

import sys
import subprocess
from pathlib import Path

def run_migrations():
    """Run database migrations"""
    print("Running database migrations...")
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
    print("✅ Migrations completed")


def create_migration(message: str):
    """Create a new migration"""
    print(f"Creating migration: {message}")
    subprocess.run(
        [sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", message],
        check=True
    )
    print("✅ Migration created")


def downgrade_migrations(steps: int = 1):
    """Downgrade migrations"""
    print(f"Downgrading {steps} migration(s)...")
    for _ in range(steps):
        subprocess.run([sys.executable, "-m", "alembic", "downgrade", "-1"], check=True)
    print("✅ Migrations downgraded")


def init_database():
    """Initialize database"""
    print("Initializing database...")
    from app.db.database import create_db_and_tables, init_db
    
    create_db_and_tables()
    init_db()
    print("✅ Database initialized")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db.py [command]")
        print("Commands:")
        print("  migrate            - Run migrations")
        print("  makemigration MSG  - Create new migration")
        print("  downgrade [STEPS]  - Downgrade migrations")
        print("  init              - Initialize database")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "migrate":
        run_migrations()
    elif command == "makemigration" and len(sys.argv) > 2:
        create_migration(sys.argv[2])
    elif command == "downgrade":
        steps = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        downgrade_migrations(steps)
    elif command == "init":
        init_database()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
