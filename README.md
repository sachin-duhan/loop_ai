# Loop.xyz

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

## Using Docker

```bash
docker build -t loop -f Docker/Dockerfile .
docker run -p 5000:5000 loop
```

## Author
- Sachin duhan
- <strong>CV</strong> : https://drive.google.com/file/d/1d3BZjr1GyaBTdrjzL5TJMuF106Wd2k3t/view?usp=sharing
- Linkdin : https://www.linkedin.com/in/sachin-duhan/
