Docker Compose file (`docker-compose.yml`) that includes the ports for both Grafana and PostgreSQL:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:latest
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: grafana
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  grafana:
    image: grafana/grafana:latest
    restart: always
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin_password
    depends_on:
      - postgres
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  grafana_data:
```

### Explanation:

- **PostgreSQL (`postgres` service)**:
  - `image`: Specifies the latest PostgreSQL image.
  - `restart`: Ensures the PostgreSQL container restarts automatically if it stops unexpectedly.
  - `ports`: Maps the host port `5432` to the container port `5432`, allowing access to PostgreSQL from outside Docker.
  - `environment`: Sets environment variables for PostgreSQL, including database name (`POSTGRES_DB`), username (`POSTGRES_USER`), and password (`POSTGRES_PASSWORD`).
  - `volumes`: Mounts a Docker volume (`postgres_data`) to persist PostgreSQL data.

- **Grafana (`grafana` service)**:
  - `image`: Specifies the latest Grafana image.
  - `restart`: Ensures the Grafana container restarts automatically if it stops unexpectedly.
  - `ports`: Maps the host port `3000` to the container port `3000`, allowing access to Grafana's web interface.
  - `environment`: Sets environment variables for Grafana, including admin username (`GF_SECURITY_ADMIN_USER`) and password (`GF_SECURITY_ADMIN_PASSWORD`).
  - `depends_on`: Specifies that the Grafana service depends on the PostgreSQL service being up and running before starting.
  - `volumes`: Mounts a Docker volume (`grafana_data`) to persist Grafana data.

- **Volumes**: Defines Docker volumes (`postgres_data` and `grafana_data`) used to persist data for PostgreSQL and Grafana respectively.

### Running the Docker Compose File:

1. Save the above YAML content into a file named `docker-compose.yml`.
2. Navigate to the directory containing `docker-compose.yml`.
3. Run the following command to start both services in detached mode (background):

   ```bash
   docker-compose up -d
   ```

4. Access Grafana via `http://localhost:3000` in your web browser. Use the admin credentials (`admin/admin_password` by default) to log in.