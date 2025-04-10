curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'include_context=true' \
  -F 'source_type=url' \
  -F 'extraction_type=entities' \
  -F 'text=' \
  -F 'url=https://www.microsoft.com/en-us/investor/events/fy-2025/earnings-fy-2025-q2?msockid=1577e198d53e6c9137c9f558d4c36d59' \
  -F 'custom_instructions='