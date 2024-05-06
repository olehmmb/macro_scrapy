# alternative install using conda
#FROM continuumio/miniconda3
#COPY .devcontainer/environment.yaml /tmp/environment.yaml
#RUN conda config --remove channels defaults
#RUN conda config --add channels conda-forge
#RUN conda create -n macro_scrapy
#RUN conda env update -n macro_scrapy -f /tmp/environment.yaml
#SHELL ["conda", "run", "-n", "macro_scrapy", "/bin/bash", "-c"]
#RUN playwright install --with-deps chromium



FROM mambaorg/micromamba
COPY --chown=$MAMBA_USER:$MAMBA_USER .devcontainer/environment.yaml /tmp/environment.yaml
RUN micromamba install -y -n base -f /tmp/environment.yaml
ARG MAMBA_DOCKERFILE_ACTIVATE=1 
RUN micromamba config append channels conda-forge
# Install Git
USER root
RUN apt-get update && apt-get install -y git
USER $MAMBA_USER

#RUN playwright install chromium 
#USER root
#RUN playwright install-deps chromium
#USER $MAMBA_USER