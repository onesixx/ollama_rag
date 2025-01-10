# ollama_rag
is platform that allow you to run LLM locally

restart sixxos
apt update && apt upgrade -y
apt upgrade curl
apt install pciutils
apt install lshw

설치
curl -fsSL https://ollama.com/install.sh | sh
# ollama --version

systemctl status ollama
/usr/local/lib/ollama

ollama API Docker
~$ docker exec -it ollama bash

# curl 172.17.0.2:11434
root@ec76aea8e38b:/# ollama run llama3.3

Start the Ollama service:
# ollama serve

# ollama create james -f ./Modelfile
# ollama list
# ollama run james



## Using `curl` to interact with the Ollama REST API
1. Generate a response using the Ollama API:
# curl --silent http://localhost:11434/api/generate --data '{ "model": "llama3.2", "prompt": "Why is the sky blue?"}' | jq -r '.response'
2. Generate a response with streaming disabled:
# curl http://localhost:11434/api/generate -d '{
    "model": "llama3.2",
    "prompt": "Why is the sky blue?",
    "stream":false
}'

3. Chat with the Ollama API:
# curl http://localhost:11434/api/chat --data '{
    "model": "llama3.2",
    "messages": [{
        "role": "user",
        "content": "Tell me a fun fact about Portugal"
    }],
    "fomat": "json",
    "stream": false
}'

# 참고
https://github.com/ollama/ollama/blob/main/docs/api.md


2. Python과 SQLite 버전 매핑
Python은 특정 버전의 SQLite를 내장하고 있으며, 아래는 주요 Python 버전과 포함된 SQLite 버전의 관계입니다:

Python 버전	내장 SQLite 버전
Python 3.9	SQLite 3.33.0
---------------------------------
Python 3.10	SQLite 3.35.4
Python 3.11	SQLite 3.37.2
Python 3.12+	최신 SQLite 버전 포함
# install sqlite3
# wget https://www.sqlite.org/2024/sqlite-autoconf-3470200.tar.gz
# tar xvfz sqlite-autoconf-3470200.tar.gz
# cd sqlite-autoconf-3470200

# ./configure --prefix=/usr/local
# make
# sudo make install