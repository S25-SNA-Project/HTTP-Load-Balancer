job "loadbalancer" {
  datacenters = ["dc1"]
  type = "service"

  group "loadbalancer-group" {
    count = 1

    constraint {
      attribute = "${meta.role}"
      operator  = "="
      value     = "balancer"
    }

    task "loadbalancer" {
      driver = "docker"

      config {
        image = "wkwtfigo/load-balancer:latest"
        ports = ["http"]
        volumes = [
          "/var/log/app-redirect-balancer:/app/.logs"
        ]
      }

      resources {
        cpu    = 500
        memory = 256
      }

      # service {
      #   name = "loadbalancer"
      #   port = "http"
      #   tags = ["loadbalancer"]
      # }
    }

    network {
      port "http" {
        static = 8000
        to     = 8000
      }
    }
  }
}
