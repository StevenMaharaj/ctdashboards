# In‑Depth Lesson: Basics of SQL & PostgreSQL

---

## 1. Introduction
SQL (Structured Query Language) is the standard language for interacting with relational databases. PostgreSQL (often abbreviated **Postgres**) is an advanced, open‑source, object‑relational database system that implements the SQL standard and adds many powerful features of its own. In this lesson you will:

1. Understand core relational concepts.
2. Install and configure PostgreSQL locally.
3. Master essential SQL commands (CRUD).
4. Learn PostgreSQL‑specific data types and features.
5. Practice writing queries involving filtering, aggregation, joins, and subqueries.
6. Explore constraints, indexes, and transactions.
7. Perform basic administrative tasks (backup/restore).
8. Apply knowledge through hands‑on exercises.

---

## 2. Relational Database Fundamentals

| Concept | Description |
|---------|-------------|
| **Table** | A collection of rows (records) with the same columns (fields). |
| **Row** | A single record. |
| **Column** | A named attribute of the data with a specific data type. |
| **Primary Key (PK)** | A column (or set of columns) that uniquely identifies each row. |
| **Foreign Key (FK)** | A column that references a primary key in another table, creating a relationship. |
| **Schema** | A namespace that contains tables, views, functions, etc. |
| **SQL Statement** | A command sent to the database engine. |

Relational databases enforce **ACID** properties (Atomicity, Consistency, Isolation, Durability) to guarantee reliable transactions.

---

## 3. Installing PostgreSQL

To install and postgres with  provided docker compose file 
Run
```
docker compose up -d
```
We can access postgres using gui tool like pgadmin or vscode code extension. Also, psql is a command line tool that lets us make queries to a postgress database. Since we're running postgres in Docker we have to use psql from the Docker container.

```bash
docker compose exec postgres psql -U admin -d grafana
```

---

## 4. PostgreSQL CLI Basics (`psql`)

| Command | Purpose |
|---------|---------|
| `\l` | List databases |
| `\c dbname` | Connect to a database |
| `\dt` | List tables in current schema |
| `\d tablename` | Describe table structure |
| `\q` | Quit `psql` |

`psql` also supports tab‑completion and command history for productivity.

---

## 5. Creating a Database & Schema
```sql
-- As superuser or a role with CREATEDB privilege
CREATE DATABASE bookstore;
\c bookstore

-- Optional: create a dedicated schema
CREATE SCHEMA sales AUTHORIZATION postgres;
SET search_path TO sales;
```

---

## 6. Data Types Cheat Sheet

| Category | Examples |
|----------|----------|
| Numeric | `smallint`, `integer`, `bigint`, `numeric`, `decimal`, `real`, `double precision` |
| Character | `char(n)`, `varchar(n)`, `text` |
| Date/Time | `date`, `timestamp`, `timestamptz`, `interval` |
| Boolean | `boolean` |
| Enumerated | `CREATE TYPE mood AS ENUM ('sad','ok','happy');` |
| Binary | `bytea` |
| Geometric | `point`, `line`, `polygon` |
| JSON | `json`, `jsonb` (binary JSON) |
| Array | `integer[]`, `text[]`, etc. |
| UUID | `uuid` |

PostgreSQL’s rich type system enables powerful modeling.

---

## 7. Creating Tables
```sql
CREATE TABLE authors (
    author_id  serial PRIMARY KEY,
    name       text NOT NULL,
    country    text,
    birth_year int
);

CREATE TABLE books (
    book_id     serial PRIMARY KEY,
    title       text NOT NULL,
    author_id   int  REFERENCES authors(author_id),
    published   date,
    price       numeric(8,2) CHECK (price >= 0),
    in_stock    boolean DEFAULT true
);
```

---

## 8. CRUD Operations

### 8.1 INSERT
```sql
INSERT INTO authors (name, country, birth_year)
VALUES ('Haruki Murakami', 'Japan', 1949),
       ('Ursula K. Le Guin', 'USA', 1929)
RETURNING *;  -- handy Postgres extension
```

### 8.2 SELECT
```sql
-- all columns
SELECT * FROM authors;

-- specific columns & filtering
SELECT name, country
FROM authors
WHERE country = 'USA';

-- sorting & limiting
SELECT *
FROM books
ORDER BY published DESC
LIMIT 5;
```

### 8.3 UPDATE
```sql
UPDATE books
SET price = price * 0.9
WHERE published < '2000-01-01';
```

### 8.4 DELETE
```sql
DELETE FROM books
WHERE in_stock = false;
```

---

## 9. Filtering & Expressions
```sql
SELECT title,
       price,
       price * 0.85 AS discounted_price
FROM books
WHERE price BETWEEN 10 AND 40
  AND title ILIKE '%wind%';  -- case‑insensitive pattern
```

Common operators: `= <> < > <= >=`, logical `AND OR NOT`, pattern matching `LIKE ILIKE`, set membership `IN (...)`.

---

## 10. Aggregate Functions & GROUP BY
```sql
SELECT country,
       COUNT(*)          AS authors,
       AVG(birth_year)   AS avg_birth
FROM authors
GROUP BY country
HAVING COUNT(*) > 1;
```
Built‑in aggregates: `COUNT, SUM, AVG, MIN, MAX, STRING_AGG`, etc.

---

## 11. Joins
```sql
-- Inner join
SELECT b.title, a.name
FROM books b
JOIN authors a ON a.author_id = b.author_id;

-- Left join (keep all authors)
SELECT a.name, b.title
FROM authors a
LEFT JOIN books b USING (author_id);

-- Self‑join example
SELECT a1.name AS author, a2.name AS peer
FROM authors a1
JOIN authors a2 ON a1.country = a2.country
WHERE a1.author_id <> a2.author_id;
```

### Visualizing Join Types
```
INNER      LEFT      RIGHT      Outer
  ⋂        ⟵         ⟶         ⋃
```

---

## 12. Subqueries & Common Table Expressions (CTEs)
```sql
-- Subquery in WHERE
SELECT *
FROM books
WHERE author_id IN (
    SELECT author_id
    FROM authors
    WHERE country = 'Japan'
);

-- CTE (WITH clause)
WITH pricey AS (
    SELECT * FROM books WHERE price > 30
)
SELECT COUNT(*) FROM pricey;
```

---

## 13. Constraints & Indexes

| Constraint | Purpose |
|------------|---------|
| `PRIMARY KEY` | Uniqueness + not‑null |
| `UNIQUE` | Enforce unique values |
| `NOT NULL` | Disallow NULLs |
| `CHECK` | Custom boolean expression |
| `FOREIGN KEY` | Refer to PK in another table |

Indexes speed up lookups:
```sql
CREATE INDEX idx_books_published ON books (published);
CREATE UNIQUE INDEX idx_authors_name ON authors (name);
```
Postgres automatically creates an index for each primary key and unique constraint.

---

## 14. Transactions
```sql
BEGIN;  -- or START TRANSACTION
UPDATE books SET price = price - 5 WHERE book_id = 1;
UPDATE authors SET country = 'UK' WHERE author_id = 2;
COMMIT;  -- or ROLLBACK;
```
Postgres supports **MVCC** (multi‑version concurrency control) and transaction isolation levels (`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`).

---

## 15. PostgreSQL‑Specific Features

1. **`RETURNING`** clause for DML.
2. **UPSERT** (`INSERT ... ON CONFLICT DO UPDATE`).
3. **JSON/JSONB** operators `->`, `->>`, `#>>`, `@>`, etc.
4. **Arrays** with `ANY`/`ALL` operators.
5. **Window Functions** (`ROW_NUMBER()`, `LAG()`, etc.).
6. **Full‑text Search** with `tsvector`/`tsquery`.
7. **Extensions** (`CREATE EXTENSION pg_trgm;`).

Example UPSERT:
```sql
INSERT INTO authors (author_id, name)
VALUES (1, 'New Name')
ON CONFLICT (author_id)
DO UPDATE SET name = EXCLUDED.name;
```

---

## 16. Basic Administration

### 16.1 Roles & Privileges
```sql
CREATE ROLE analyst LOGIN PASSWORD 's3cret';
GRANT CONNECT ON DATABASE bookstore TO analyst;
GRANT USAGE ON SCHEMA sales TO analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA sales TO analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA sales
  GRANT SELECT ON TABLES TO analyst;
```

### 16.2 Backup & Restore
```bash
# Dump entire database
pg_dump -U postgres -Fc bookstore > bookstore.dump

# Restore
createdb bookstore_restored
pg_restore -U postgres -d bookstore_restored bookstore.dump
```

---

## 17. Exercises

1. **Create Tables**: Design tables for a simple movie database (movies, directors, actors, roles) with appropriate keys and constraints.
2. **Insert Data**: Add at least 5 movies, 3 directors, and 10 actors.
3. **Query**: List all movies released after 2015 with their directors.
4. **Aggregation**: Count how many movies each director has directed.
5. **Update**: Increase ticket price by 15% for movies longer than 120 minutes.
6. **Delete**: Remove actors who have not appeared in any movie.
7. **Index**: Create an index to speed up searches by movie title.
8. **Transaction**: Write a transaction that books two tickets and reduces seat availability atomically.
9. **JSONB**: Store movie metadata (rating, genre list) in a JSONB column and query all action movies rated above 8.
10. **Backup**: Produce a compressed dump of your movie database.

> *Answers & explanations are provided in the appendix.*

---

## 18. Appendix: Exercise Solutions (abridged)

<details>
<summary>Click to reveal solutions</summary>

### 1. Table Design
```sql
CREATE TABLE directors (
  director_id serial PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE movies (
  movie_id serial PRIMARY KEY,
  title text NOT NULL,
  director_id int REFERENCES directors,
  released date,
  duration int, -- minutes
  ticket_price numeric(6,2) CHECK (ticket_price > 0),
  metadata jsonb
);

CREATE TABLE actors (
  actor_id serial PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE roles (
  movie_id int REFERENCES movies,
  actor_id int REFERENCES actors,
  character_name text,
  PRIMARY KEY (movie_id, actor_id)
);
```

### 3. Query Movies & Directors
```sql
SELECT m.title, d.name AS director
FROM movies m
JOIN directors d USING (director_id)
WHERE m.released >= '2015-01-01';
```

<!-- additional solutions omitted for brevity -->

</details>

---