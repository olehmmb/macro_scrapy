FROM mambaorg/micromamba


#RUN mkdir requirements
COPY --chown=$MAMBA_USER:$MAMBA_USER .devcontainer/environment.yaml /tmp/environment.yaml
RUN micromamba install -y -n base -f /tmp/environment.yaml 
ARG MAMBA_DOCKERFILE_ACTIVATE=1 