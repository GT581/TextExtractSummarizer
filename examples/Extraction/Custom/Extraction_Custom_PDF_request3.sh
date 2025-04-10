curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@code-charles-petzold.pdf;type=application/pdf' \
  -F 'include_context=true' \
  -F 'source_type=pdf' \
  -F 'extraction_type=custom' \
  -F 'text=' \
  -F 'url=' \
  -F 'custom_instructions=What are the chapter names in this book, and what is each about?'