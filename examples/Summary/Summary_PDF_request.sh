curl -X 'POST' \
  'http://127.0.0.1:8000/api/summarize' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@Peter_Lynch_one-up-on-wall-street.pdf;type=application/pdf' \
  -F 'max_length=1000'