curl -X 'POST' \
  'http://127.0.0.1:8000/api/summarize' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'max_length=500' \
  -F 'source_type=url' \
  -F 'url=https://seekingalpha.com/article/4765557-costco-wholesale-corporation-cost-q2-2025-earnings-call-transcript'