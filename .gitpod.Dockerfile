FROM gitpod/workspace-python:2023-04-14-07-10-23

RUN pyenv install 3.10.9 \
    && pyenv global 3.10.9

RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc \
    && chmod +x mc \
    && sudo mv mc /usr/local/bin/mc
