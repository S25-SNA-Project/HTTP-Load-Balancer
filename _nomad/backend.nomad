job "backend" {
  datacenters = ["dc1"]
  type = "service"

  group "backend-group" {
    count = 3

    constraint {
      attribute = "${meta.role}"
      operator = "="
      value = "backend"
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

    task "backend" {
      driver = "docker"

      config {
        image = "wkwtfigo/backend-service:latest"
        ports = ["http"]
        volumes = [
          "/var/log/app-redirect-balancer:/app/.logs"
        ]
      }

      resources {
        cpu    = 500
        memory = 256
      }
    }

    network {
      mode = "host"
      port "http" {
        static = 8080
        to = 8080
      }
    }
  }
}
