job "wazuh-agent" {
  datacenters = ["dc1"]
  type = "system"

  group "wazuh" {
    task "agent" {
      driver = "docker"

      config {
        image = "wazuh/wazuh-agent:4.7.0"
        privileged = true
        volumes = [
          "/proc:/host/proc:ro",
          "/sys:/host/sys:ro",
          "/var/run/docker.sock:/var/run/docker.sock"
        ]
      }

      env {
        MANAGER_IP        = "${WAZUH_MANAGER_IP}"
        REGISTER_PASSWORD = "${AGENT_REG_PASSWORD}"
      }

      resources {
        cpu    = 200
        memory = 200
      }
    }
  }
}
