# In‑Depth Lesson: Mastering Grafana

---

## 1. Introduction
Grafana is an **open‑source analytics & observability platform** that lets you query, visualize, alert on, and understand your metrics, logs, and traces no matter where they are stored. Originally built for time‑series metrics, Grafana has evolved into a full “single‑pane‑of‑glass” with support for over 80 data sources and rich plugins.

By the end of this lesson you will be able to:
1. Install and configure Grafana in multiple environments.
2. Connect diverse data sources (Prometheus, PostgreSQL, Loki, etc.).
3. Build dynamic dashboards with variables, transformations, and advanced panels.
4. Configure the unified alerting system and notification channels.
5. Manage users, organizations, and secure your deployment.
6. Automate provisioning with code and integrate Grafana into CI/CD.
7. Scale Grafana for high availability and performance.

> **Prerequisites**: Familiarity with Linux command line, basic understanding of metrics/logs, and access to at least one data source (Prometheus, SQL DB, or sample data).

---

## 2. Architecture & Core Components

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Frontend** | React/TypeScript SPA | Dashboards, Explore, Alerting UI |
| **Backend** | Go HTTP server (`grafana‑server`) | API, auth, data source proxies, alerting engine |
| **Database** | SQLite (default) / MySQL / PostgreSQL | Stores dashboards, users, alert rules, etc. |
| **Data Sources** | Plugins or built‑ins | Prometheus, Loki, PostgreSQL, Elasticsearch, CloudWatch, … |
| **Plugins** | Panels, apps, data sources | Extend functionality (e.g., WorldMap, Zabbix) |
| **Renderer** | `grafana-image-renderer` | Generates PNG/PDF for reporting |

Grafana **does not** store your metrics/logs by default—it queries them on demand and caches results in memory.

---

## 3. Installation Options

### 3.1 Docker (Quick Start)
```bash
docker run -d --name=grafana \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=secret" \
  grafana/grafana-oss:10.2.3
```
*Browse* `http://localhost:3000` → user **admin / secret**.

### 3.2 Linux Packages (Deb/RPM)
```bash
# Debian/Ubuntu
sudo apt-get install -y apt-transport-https software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt update && sudo apt install grafana
sudo systemctl enable --now grafana-server
```

### 3.3 Helm on Kubernetes
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set adminPassword=secret \
  --set persistence.enabled=true
```

### 3.4 Grafana Cloud
Sign up at <https://grafana.com> for a hosted instance (free tier includes 10k metrics, 50GB logs, 50GB traces).

---

## 4. Configuration Basics (`grafana.ini`)
*Location*: `/etc/grafana/grafana.ini` or override with `GF_` env vars.

Key sections:
```ini
[server]
protocol = http
http_port = 3000
root_url = %(protocol)s://grafana.example.com/

[database]
;sqlite3, mysql, postgres
type = postgres
host = 127.0.0.1:5432
database = grafana
user = grafana
password = supersecret

[security]
admin_user = admin
admin_password = change_me

[auth]
disable_login_form = false
```
Restart service after changes.

---

## 5. Data Sources Deep Dive

### 5.1 Adding via UI
1. **Gear icon → Data sources → Add data source**.
2. Pick a type (e.g., *Prometheus*).
3. Enter URL, access mode (server/browser), and credentials.
4. Click **Save & Test**.

### 5.2 Popular Sources & Nuances
| Source | Query Language | Notable Features |
|--------|---------------|------------------|
| **Prometheus / Mimir** | PromQL | Native alert rules, auto‑completion, metric math |
| **Loki** | LogQL | Regex & label filtering, derived metrics |
| **PostgreSQL / MySQL** | SQL | Use macros like `__$timeFilter(column)__` and `__$interval__` |
| **Elasticsearch / OpenSearch** | Lucene / PPL | Multi‑bucket aggregations |
| **CloudWatch** | AWS APIs | Cross‑account via AssumeRole |

### 5.3 Macros & Time Series Conversion (SQL example)
```sql
SELECT
  $__time(created_at)   AS time,
  avg(response_ms)      AS avg_latency
FROM api_logs
WHERE $__timeFilter(created_at)
GROUP BY 1
ORDER BY 1
```

---

## 6. Building Dashboards & Panels

### 6.1 Anatomy
* **Dashboard** → JSON document containing rows & panels.
* **Panel** → visualization + data query + options.
* **Visualization Types**: Time series, Bar gauge, Stat, Table, Pie, Heatmap, Geomap, Candlestick, Node graph, Trace view, Logs.

### 6.2 Creating a Panel
1. **+ → Dashboard → Add new panel**.
2. Choose data source & craft query.
3. Select visualization.
4. Configure **Panel options**: axes, units, thresholds, legend, transformations.
5. **Apply**.

### 6.3 Transformations
Chain post‑processing without altering the source:
* **Add field from calculation**
* **Organize fields**
* **Filter data by values**
* **Outer join** multiple queries

---

## 7. Variables & Templating

Variables make dashboards dynamic.
```text
$__interval   Auto step size (ms)
$region       Custom or query variable
```

### 7.1 Types
| Type | Example |
|------|---------|
| **Query** | `label_values(up{job="api"}, instance)` (PromQL) |
| **Interval** | `1m,5m,15m,1h` |
| **Custom** | `prod, staging, dev` |
| **Constant** | Fixed string |

### 7.2 Cascading Variables
Use `$region` in another variable’s query to filter dependent lists.

### 7.3 Repeating Rows/Panels
Enable **Repeat for variable** → one panel per variable value.

---

## 8. Unified Alerting System (Grafana 9+)

### 8.1 Concepts
* **Contact Point** – where to send notifications (Slack, Email, PagerDuty, Webhook).
* **Notification Policy** – routing tree (severity, labels).
* **Alert Rule** – evaluates queries & conditions.
* **Silence** – mute alerts by matcher labels for a period.

### 8.2 Creating an Alert Rule
1. Edit panel → **Alert** tab → **Create alert rule from this panel**.
2. Define queries (A, B…) and condition (e.g., `avg() of A > 0.9` for 5m).
3. Assign labels (service=api, severity=critical).
4. Save – rule stored in backend & evaluated server‑side.

### 8.3 Contact Points & Policies
Configuration → **Alerting → Contact points** & **Notification policies**.

### 8.4 Best Practices
* Keep evaluation interval ≥ scrape interval.
* Add `for` duration to reduce flapping.
* Use labels for routing & silencing.

---

## 9. Explore Mode & Ad‑hoc Troubleshooting
* Lightning bolt icon → **Explore**.
* Run instant queries, switch between Metrics & Logs.
* Correlate: **Logs → Metrics** or **Metrics → Logs** jump links.

---

## 10. Annotations & Events
Add context (deploys, incidents) over graphs.
```bash
curl -X POST http://localhost:3000/api/annotations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"v1.2 deployed","tags":["deploy","prod"]}'
```

---

## 11. Plugins Ecosystem

### 11.1 Installing a Plugin (CLI)
```bash
grafana-cli plugins install grafana-worldmap-panel
systemctl restart grafana-server
```

### 11.2 Plugin Types
| Type | Example |
|------|---------|
| **Panel** | Worldmap, Clock, Diagram |
| **Data Source** | Snowflake, Google BigQuery |
| **App** | Kubernetes App (combines pages, panels, backend) |

---

## 12. Provisioning as Code

### 12.1 Data Sources (`datasources.yaml`)
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```
Place under `/etc/grafana/provisioning/datasources/`.

### 12.2 Dashboards (`dashboards.yaml`)
```yaml
apiVersion: 1
dashboardProviders:
  - name: default
    folder: Infrastructure
    type: file
    options:
      path: /var/lib/grafana/dashboards
```
Put JSON dashboards in the path and Grafana auto‑loads them.

### 12.3 Alerting (`alerting.yaml`)
Grafana 10 supports provisioning contact points and policies via YAML.

### 12.4 Terraform Provider
```hcl
resource "grafana_dashboard" "cpu" {
  config_json = file("cpu.json")
}
```

---

## 13. User Management & Security

| Concept | Details |
|---------|---------|
| **Organizations** | Multi‑tenant separation; users belong to one org at a time. |
| **Roles** | Admin, Editor, Viewer (plus granular permissions in Enterprise). |
| **Auth Providers** | Basic, OAuth (GitHub, Google), LDAP, SAML, Azure AD. |
| **API Keys** | Programmatic access; scope (Admin, Editor, Viewer). |
| **Folder & Data Source Permissions** | Restrict editing/viewing. |

### 13.1 Enabling GitHub OAuth (example)
```ini
[auth.github]
enabled = true
client_id = GITHUB_ID
client_secret = GITHUB_SECRET
allowed_organizations = myorg
```

---

## 14. Performance & Scaling

1. **Database Backend** – use MySQL/PostgreSQL for HA; replicate & backup.
2. **Caching** – `GF_QUERY_CACHE_*` env vars (Grafana 10+).
3. **Image Renderer** – run as sidecar or remote rendering service.
4. **Horizontal Scaling** – stateless; behind load balancer; shared DB & storage for dashboards.
5. **High Availability Alerting** – enable `cluster` alerting mode and use Redis for message bus.

---

## 15. Observability Stack (Loki, Tempo, Mimir)
Grafana Labs provides **Loki** (logs), **Tempo** (traces), and **Mimir/Prometheus** (metrics). Integrate all three for metrics → logs → traces correlation within a single UI.

---

## 16. Enterprise‑Only Features (FYI)
* **Reporting** – scheduled PDF/PNG emails.
* **Fine‑grained Permissions** – per‑dashboard, per‑data‑source.
* **SAML/SSO**, **Audit Logs**, **Data Source Caching**, **Query Replay**.

---

## 17. CI/CD & GitOps Workflow

1. Store dashboards JSON & provisioning YAML in Git.
2. Use Terraform/Helm to deploy Grafana with versioned configs.
3. PR review → preview environments via separate folders/orgs.

---

## 18. Hands‑On Exercises

1. **Install Grafana** locally with Docker.
2. **Connect Prometheus** (or use `prometheus/demo` data source).
3. **Create a dashboard** showing CPU, memory, and HTTP error rate with thresholds.
4. **Add a query variable** for `$instance` and make panels repeat per instance.
5. **Configure an alert**: HTTP error rate > 5% for 10 minutes → Slack.
6. **Annotate** a deployment event via API and verify it appears on graphs.
7. **Provision** the dashboard and data source via YAML; commit to Git.
8. **Enable GitHub OAuth** and test login.
9. **Install WorldMap plugin** and visualize requests by region using GeoIP.
10. **Scale Grafana** to two replicas in Kubernetes with a shared PostgreSQL backend.

---

## 19. Appendix: Sample Solutions (abridged)

<details>
<summary>Click to expand</summary>

### Exercise 3 – CPU Panel Query (PromQL)
```promql
avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)
```

### Exercise 5 – Alert Rule YAML (provisioned)
```yaml
apiVersion: 1
alertRules:
  - name: high_http_errors
    condition: B
    for: 10m
    annotations:
      summary: "High HTTP 5xx rate"
    labels:
      severity: critical
    queries:
      - ref: A
        expr: sum(rate(http_requests_total{status=~"5.."}[5m]))
      - ref: B
        expr: A / sum(rate(http_requests_total[5m])) > 0.05
```

<!-- more solutions omitted for brevity -->

</details>

---

## 20. Further Resources
* **Official Docs** – <https://grafana.com/docs/>
* **Grafana Labs Tutorials** – dashboard design, alerting, plugins.
* **Play with Grafana** – <https://play.grafana.org> (public sandbox).
* **Awesome‑Grafana** GitHub repo for community plugins and dashboards.

Happy dashboarding! 🎨📈

