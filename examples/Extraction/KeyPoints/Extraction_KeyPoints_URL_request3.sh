curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'include_context=true' \
  -F 'source_type=url' \
  -F 'extraction_type=key_points' \
  -F 'text=' \
  -F 'url=https://www.espn.com/soccer/' \
  -F 'custom_instructions='