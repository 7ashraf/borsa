Output docs/assets/demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 1100
Set Height 620
Set Theme "Dracula"
Set Padding 20
Set TypingSpeed 40ms

Sleep 500ms

Type "# borsa — EGX market data API"
Sleep 800ms
Enter
Sleep 400ms

Type "curl -s localhost:8000/v1/health | jq ."
Sleep 600ms
Enter
Sleep 2s

Type "curl -s localhost:8000/v1/stocks | jq '{count: .count, first: .symbols[0]}'"
Sleep 600ms
Enter
Sleep 2500ms

Type "curl -s localhost:8000/v1/quote/COMI | jq ."
Sleep 600ms
Enter
Sleep 4s

Sleep 1s
