## How to run

- refers to Makefile

### run

`$ poetry run nohup uvicorn opendevin.server.listen:app --port $(BACKEND_PORT) > logs/backend_$(shell date +'%Y%m%d\_%H%M%S').log 2>&1 &`

### VS code interpreter setting

cmd + p > interpreter

`apps/api/.venv/bin/python`

### Generate Requirements.txt

Generate requirements.txt using Poetry package manager:

```
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

Python monorepo info:
https://medium.com/@ashley.e.shultz/python-mono-repo-with-only-built-in-tooling-7c2d52c2fc66
