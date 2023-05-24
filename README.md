## Loop.xyz

```bash
git clone https://github.com/sachin-duhan26/loop_ai
cd loop_ai

python3 -m venv .venv

cp .env.example .env
# udpate env variables.

source .venv/bin/activate
make install

# install redis if not installed already.
brew install redis

# start redis
redis-server

# run application.
make run
```
