# Base image
FROM mcr.microsoft.com/devcontainers/base:jammy

COPY setup_environment_on_ubuntu_22.sh .
COPY requirements.txt .
RUN chmod +x setup_environment_on_ubuntu_22.sh
RUN ./setup_environment_on_ubuntu_22.sh
 
WORKDIR /workspace

CMD ["/bin/bash"]