curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'include_context=true' \
  -F 'source_type=url' \
  -F 'extraction_type=key_points' \
  -F 'text=' \
  -F 'url=https://seekingalpha.com/market-news' \
  -F 'custom_instructions='