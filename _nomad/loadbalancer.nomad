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

    task "init-dir" {
      driver = "exec"

      config {
        command = "/bin/mkdir"
        args    = ["-p", "/var/log/app-redirect-balancer"]
      }

      lifecycle {
        hook = "prestart"
      }

      resources {
        cpu    = 100
        memory = 64
      }
    }

    task "loadbalancer" {
      driver = "docker"

      config {
        image = "wkwtfigo/load-balancer:latest"
        ports = ["http", "communication"]
        volumes = [
          "/var/log/app-redirect-balancer/:/app/.logs/"
        ]
      }

      env {
        DEBUG = "true"
      }

      resources {
        cpu    = 1000
        memory = 512
      }
    }

    network {
      port "http" {
        static = 8000
        to     = 8000
      }
      port "communication" {
        static = 8001
        to     = 8001
      }
    }
  }
}
