# docker image to compare lock files for poetry 1.8.5 and poetry 2.0.0
# used to assess the impact of poetry 2

FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git \
    && apt-get clean \
    && python3 -m pip install --upgrade pip pipx \
    && python3 -m pipx ensurepath


# Add pipx's binary path to the PATH environment variable
ENV PATH=$PATH:/root/.local/bin

RUN pip install --upgrade pip virtualenv
RUN pipx install --suffix=@1.8.5 poetry==1.8.5
RUN pipx install --suffix=@2.0.0 poetry==2.0.0

WORKDIR /app

COPY . .

RUN cp poetry.lock poetry185.lock \
    && poetry@1.8.5 show --tree > poetry185-tree.txt \
    && poetry@2.0.0 lock \
    && poetry@2.0.0 show --tree > poetry-tree.txt

CMD ["/bin/bash"]

# run the container and run these commands:
# git diff --no-index poetry185.lock poetry.lock
# git diff --no-index poetry185-tree.txt poetry-tree.txt
