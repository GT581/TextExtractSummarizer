curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@Peter_Lynch_one-up-on-wall-street.pdf;type=application/pdf' \
  -F 'include_context=true' \
  -F 'source_type=pdf' \
  -F 'extraction_type=custom' \
  -F 'text=' \
  -F 'url=' \
  -F 'custom_instructions=In this book, what were some of the author'\''s most successful trades where he made the most money in his time as the manager? Include the company, return, and details.'