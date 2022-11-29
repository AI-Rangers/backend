# backend
backend

### Windwos

[Install python (pyenv) on WSL (Ubuntu)](https://www.techtronic.us/install-python-pyenv-on-wsl-ubuntu/)

### Mac

```
brew update
brew install pyenv
```
### Setup

```shell
$ pyenv install -v 3.8.15
# 設定全域的 Python 版本
$ pyenv global 3.8.15

$ git clone git@github.com:AI-Rangers/backend.git                           ─╯
$ cd backend
# 設定區域的 Python 版本
$ pyenv local 3.8.15
# Check Python 版本
$ python --version
$ pip install --upgrade pip setuptools wheel
$ pip install -r requirements
# copy .env
$ cp .env.sample .env
# test on http://localhost:8000/docs
$ uvicorn app.main:app --reload --port 8000
```

### VScode
- Win : Ctrl + Shift + P
- Mac : fn + F1
    - `>Python: Select Interpreter`
    - `3.8.15`
