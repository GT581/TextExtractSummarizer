curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'include_context=true' \
  -F 'source_type=url' \
  -F 'extraction_type=key_points' \
  -F 'text=' \
  -F 'url=https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=100' \
  -F 'custom_instructions='