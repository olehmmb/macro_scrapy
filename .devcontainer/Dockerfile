FROM continuumio/miniconda3
RUN mkdir requirements
COPY .devcontainer/environment.yaml /tmp/environment.yaml

RUN conda config --remove channels defaults
RUN conda config --add channels conda-forge
RUN conda env create -n envname -f /tmp/environment.yaml



# micromamba not used due to not including pip installed packages in environment.yaml files
#FROM mambaorg/micromamba
#RUN mkdir requirements
#COPY --chown=$MAMBA_USER:$MAMBA_USER .devcontainer/environment.yaml /tmp/environment.yaml
#RUN micromamba install -y -n base -f /tmp/environment.yaml 
#ARG MAMBA_DOCKERFILE_ACTIVATE=1 