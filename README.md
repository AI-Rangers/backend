# backend
backend

### Windwos

[Install python (pyenv) on WSL (Ubuntu)](https://www.techtronic.us/install-python-pyenv-on-wsl-ubuntu/)

```shell
# 安裝
$ sudo apt-get install git gcc make openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev zlib1g-dev libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev

$ curl https://pyenv.run | bash
```
### Mac

```
brew update
brew install pyenv
```
### Setup

```shell
# 修改 ~/.profile
$ vim ~/.profile

# 修改 ~/.bashrc
$ vim ~/.bashrc
```

```shell
# 在 .profile 和 .bashrc 檔案的最後面加入這段
# pyenv
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

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
$ pip install -r requirements.txt
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
