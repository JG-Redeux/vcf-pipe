FROM python:3.12
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]

COPY requirements.txt /app/requirements.txt

RUN apt-get update \
&& apt-get install -y build-essential \
&& apt-get install -y wget \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*



# Install miniconda
ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
/bin/bash ~/miniconda.sh -b -p /opt/conda \
conda install --yes --file /app/requirements.txt

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH