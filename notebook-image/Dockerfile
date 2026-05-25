FROM jupyter/base-notebook:latest
USER root
RUN apt-get update && apt-get install -y git
USER ${NB_UID}
RUN pip install numpy pandas scikit-learn matplotlib requests
COPY default.ipynb /srv/default.ipynb
