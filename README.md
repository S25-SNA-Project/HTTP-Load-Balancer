# Reverse Proxy Load Balancer System

---
## Overview

This system simulates a reverse proxy (load balancer) that distributes incoming requests to backend servers based on the least number of active connections. The backend servers simulate long-lived sessions or compute-intensive endpoints. The project is designed to handle HTTP-based web service requests and efficiently distribute them using a front-end load balancer.

---
## Demo
![](demo.gif)
---
## System Components

1. **Load Balancer (Gateway)**: This component is responsible for distributing incoming HTTP requests to backend servers based on their load.
2. **Backend Servers**: These servers handle requests from the load balancer. They simulate long-lived sessions or compute-intensive tasks.

---
## Key Features

- **Iterative Request Redirection**: Unlike traditional proxy systems, this solution uses an iterative approach to redirect clients to the backend server with the least active connections.
- **High Traffic Scalability**: The system optimizes resource utilization and improves scalability for high-traffic environments.
- **Centralized Control**: Despite the distributed backend architecture, the system maintains centralized control for optimal routing decisions.

---
# Technologies Used

- <img src="https://img.shields.io/badge/-FastAPI-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI" style="vertical-align: middle;"/>: Chosen for its lightweight and high-performance asynchronous HTTP server capabilities.


- <img src="https://img.shields.io/badge/-httpx-5F5B5B?style=flat&logo=httpx&logoColor=white" alt="httpx" style="vertical-align: middle;"/>, <img src="https://img.shields.io/badge/-aiohttp-2C3E50?style=flat&logo=aiohttp&logoColor=white" alt="aiohttp" style="vertical-align: middle;"/>: Libraries for making asynchronous HTTP requests.


- <img src="https://img.shields.io/badge/-Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker" style="vertical-align: middle;"/>: The system is containerized using Docker to ensure easy deployment and environment consistency.

---

## Deployment

Instead of using the local Docker-based setup, the system was deployed in a production-like environment using **Nomad** for container orchestration.

### 🧩 Infrastructure Setup

- **Nomad** was used as the orchestrator across all machines.
- On **each node** in the cluster:
  - 🛡 **Wazuh Agent** was installed to collect logs and monitor security.
  - 📦 **Loki** was deployed to aggregate and store logs from the containers.
- The application code (load balancer and backend services) was deployed **only on designated nodes** using Nomad job files with constraints.
- Each component was managed through a declarative `.nomad` job specification.

### 📡 Observability

All logs from the services are:
- collected by **Wazuh Agent**,
- streamed via **Promtail** (optional),
- stored and visualized through **Loki** and **Grafana** on the central monitoring server.

### 🔗 Live Demo

You can view the deployed system in action here:  
👉 **[Live Demo Link](https://demo-url.com)**

---

> 💡 This deployment strategy ensures better scalability, security, and separation of concerns between logging, orchestration, and service logic.

### Contributing

Feel free to fork this repository and submit pull requests. Any contributions to improve the system, such as adding new features, enhancing performance, or improving security, are welcome!

---
>## Contacts
>
>>### Artem Ostapenko
>>- Telegram: [@ostxxp](https://t.me/ostxxp)
>>- Email: [a.ostapenko@innopolis.university](mailto:a.ostapenko@innopolis.university)
>
>>### Aliya Sagdieva
>>- Telegram: [@aliyushka_sgdv](https://t.me/aliyushka_sgdv)
>>- Email: [a.sagdieva@innopolis.university](mailto:a.sagdieva@innopolis.university)
>
>>### Ivan Lobazov
>>- Telegram: [@XriXis](https://t.me/XriXis)
>>- Email: [i.lobazov@innopolis.university](mailto:i.lobazov@innopolis.university)


---

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.