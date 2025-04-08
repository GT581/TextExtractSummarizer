curl -X 'POST' \
  'http://127.0.0.1:8000/api/summarize' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'max_length=500' \
  -F 'source_type=url' \
  -F 'url=https://en.wikipedia.org/wiki/Cat'