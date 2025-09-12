terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "4.0.6"
    }
  }
}
variable "do_token" {
  sensitive = true
}
provider "digitalocean" {
  token = var.do_token
}
# gets stored unencrypted in state file, probably won't be doing this in production.
resource "tls_private_key" "my_ssh_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}
resource "digitalocean_ssh_key" "key_on_account" {
  name       = "key_on_account"
  public_key = tls_private_key.my_ssh_key.public_key_openssh
}
resource "digitalocean_droplet" "arbitrary_droplet" {
  image = "ubuntu-24-04-x64"
  name  = "some-name-for-droplet"
  size  = "s-2vcpu-2gb-intel"
  ssh_keys = [
    digitalocean_ssh_key.key_on_account.id
  ]
  provisioner "local-exec" {
    command = "python3 ./playbook_executor.py -t ${self.ipv4_address} -u root -p ./nginx.yaml"
    environment = {
      # this seems a lot simpler than trying to format the command properly since there's multiple lines in the data
      RSA_PRIVATE_KEY = "${tls_private_key.my_ssh_key.private_key_openssh}\n"
    }
  }
}