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

## Installation

To get started with this system, you’ll need to clone the repository and build the Docker images. Follow these steps:

### Prerequisites

- Docker installed on your machine. You can download Docker from [here](https://www.docker.com/get-started).
- Docker Compose installed for orchestration of multi-container environments.

### Clone the Repository

```bash
git clone https://github.com/yourusername/reverse-proxy-load-balancer.git
cd reverse-proxy-load-balancer
```
### Build the Docker Images
This project’s Docker images are available on Docker Hub. You can pull the images directly from Docker Hub, or you can build them locally if needed.

### To pull the images from Docker Hub:
```
docker pull yourusername/load-balancer
docker pull yourusername/backend-service
```
If you want to build the Docker images locally, you can run:
```
docker-compose build
```
### Start the Services
Use Docker Compose to start the load balancer and backend services:
```
docker-compose up
```
This command will start all necessary services in the background.

## Usage

Once the system is running, the load balancer will handle incoming HTTP requests and distribute them to the backend servers based on the least active connections. To test the system's functionality, you can use ApacheBench (ab) to simulate traffic:

---

## Simulate Traffic with ApacheBench
### Install ApacheBench if you don’t have it:
```
sudo apt install apache2-utils
```
### Then, run a test:
```
ab -n 1000 -c 10 http://localhost:8000/your-endpoint
```
This command will send 1000 requests with a concurrency of 10 to the load balancer, simulating traffic.

---
## Configuration

You can configure various parameters of the system, such as the backend servers and the load balancer settings, by modifying the config.py file.

###  Example Configuration
```
# config.py
BACKEND_SERVERS = [
    'http://backend1:8001',
    'http://backend2:8002',
    'http://backend3:8003'
]
LOAD_BALANCER_PORT = 8000
```
This configuration file defines the backend servers and the port on which the load balancer will run.

### Security Considerations

While the current implementation is optimized for performance, it is essential to consider security, especially in production environments. Future improvements may include a security verification layer on backend servers to validate redirected requests and prevent unauthorized access.


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