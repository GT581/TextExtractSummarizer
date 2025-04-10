curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'include_context=true' \
  -F 'source_type=url' \
  -F 'extraction_type=custom' \
  -F 'text=' \
  -F 'url=https://en.wikipedia.org/wiki/Cat' \
  -F 'custom_instructions=What countries have the most cats as pets?'