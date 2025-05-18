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

      env {
        DEBUG = "true"
      }

      resources {
        cpu    = 1000
        memory = 512
      }

      service {
        name = "loadbalancer"
        port = "http"
        tags = ["loadbalancer"]
        
        check {
          name     = "alive"
          type     = "http"
          path     = "/health"
          interval = "10s"
          timeout  = "2s"
          
          check_restart {
            limit = 3
            grace = "90s"
            ignore_warnings = false
          }
        }
      }
    }

    network {
      port "http" {
        static = 8000
        to     = 8000
      }
    }
  }
}
