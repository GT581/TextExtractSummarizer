curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'include_context=true' \
  -F 'source_type=url' \
  -F 'extraction_type=entities' \
  -F 'text=' \
  -F 'url=https://finance.yahoo.com/news' \
  -F 'custom_instructions='