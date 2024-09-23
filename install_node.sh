#!/bin/bash

# Update system packages
sudo apt-get update

# Install necessary packages for Node.js
sudo apt-get install -y ca-certificates curl gnupg

# Add Node.js signing key and repository
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# Add Node.js version 20 to the package manager
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list

# Update and install Node.js
sudo apt-get update
sudo apt-get install -y nodejs

# Check the installed Node.js version
node -v
