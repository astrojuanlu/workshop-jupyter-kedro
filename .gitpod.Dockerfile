FROM gitpod/workspace-python:2023-04-14-07-10-23

RUN pyenv install 3.10.9 \
    && pyenv global 3.10.9
