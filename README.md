# MySQL Data Layer

This module centralizes all interactions between the application modules and the relational database (MariaDB/MySQL).

## Responsibilities

- **Connection Management:** `DBbaseline.py` securely manages connections to the database using credentials loaded from the global `.env`.
- **Schema Management:** 
  - Contains `.sql` files to safely construct, define, and reset tables (`classes`, `connections`, `documents`, `iplist`, `personal`, `qresults`, `registration_tokens`, `users`).
  - Utilizes `CHAR(36)` UUIDs to manage `user_id` strictly, ensuring perfect referential integrity.
- **CRUD Operations:** Separates database logic into dedicated Python files (`DBinsertTables.py`, `DBupdateTables.py`, `DBdeleteTables.py`, `DBcreateTables.py`) for clean, predictable imports by other modules.
- **Configuration Parsing:** Resolves complex environment variables and secrets via `config.py` tailored for the database layer.

## Architecture Notes
- Completely stateless interface. Modules simply import the necessary getter/setter functions.
- Highly resilient to schema errors—includes debugging layers that bubble up precise `errno: 150` foreign key constraints to the terminal console during application initialization.