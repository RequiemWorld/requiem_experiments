terraform {
  required_providers {
    # at the time of writing, no IDE support in helping writing this
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.66.0"
    }
  }
}

variable "do_token" {
  type = string
}

variable "existing_ssh_key_id" {
  type = number
}
provider "digitalocean" {
  token = var.do_token
}
import {
  to = digitalocean_ssh_key.my_ssh_key
  id = var.existing_ssh_key_id
}

resource "digitalocean_ssh_key" "my_ssh_key" {
  name       = "name"
  public_key = file("~/.ssh/id_rsa.pub")
}
resource "digitalocean_droplet" "nginx_droplet" {
  name = "ubuntu-nginx"
  image = "ubuntu-24-04-x64"
  size  = "s-1vcpu-2gb-intel"
  ssh_keys = [
    digitalocean_ssh_key.my_ssh_key.id,
  ]
  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = file("~/.ssh/id_rsa")
  }
  provisioner "remote-exec" {
    inline = [
      "apt update -y",
      "apt install nginx -y",
    ]
  }
  provisioner "local-exec" {
    command = "bash wait_for_2xx_response_curl.sh http://${self.ipv4_address}"
  }

}