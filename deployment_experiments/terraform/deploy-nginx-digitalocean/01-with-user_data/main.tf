# A minimum example of using terraform, with a single file, and setup of a droplet through user data.
terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}
variable "do_token" {}
provider "digitalocean" {
  token = var.do_token # Use a variable for your DigitalOcean API token
}
resource "digitalocean_droplet" "nginx-droplet" {
  # referenced from: https://slugs.do-api.dev/
  name  = "nginx-droplet"
  image = "ubuntu-24-04-x64"
  size  = "s-1vcpu-2gb-intel"
  user_data = "#!/bin/bash\napt update -y\napt install -y nginx\n"
}