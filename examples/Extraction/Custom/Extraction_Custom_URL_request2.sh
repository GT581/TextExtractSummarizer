curl -X 'POST' \
  'http://localhost:8000/api/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'include_context=true' \
  -F 'source_type=url' \
  -F 'extraction_type=custom' \
  -F 'text=' \
  -F 'url=https://www.espn.com/soccer/scoreboard/_/date/20250406' \
  -F 'custom_instructions=What were the scores for the english, spanish, and italian league games on this date? Identify who played who.'