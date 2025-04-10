curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@Peter_Lynch_one-up-on-wall-street.pdf;type=application/pdf' \
  -F 'include_context=true' \
  -F 'source_type=pdf' \
  -F 'extraction_type=key_points' \
  -F 'text=' \
  -F 'url=' \
  -F 'custom_instructions='