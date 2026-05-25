Output docs/assets/demo.gif

Require curl
Require python3

Set Shell "bash"
Set FontSize 16
Set Width 1180
Set Height 720
Set Theme "Catppuccin Mocha"
Set Padding 28
Set Margin 12
Set MarginFill "#11111b"
Set BorderRadius 10
Set WindowBar "Colorful"
Set TypingSpeed 30ms

Hide
Type "cd /Users/omarelsergany/Projects/borsa"
Enter
Type "export PS1='borsa $ '"
Enter
Type "curl -s http://localhost:8000/v1/quote/COMI >/dev/null"
Enter
Type "clear"
Enter
Show

Sleep 500ms
Type "# borsa: self-hosted EGX market data API"
Enter
Sleep 700ms

Type "# Start the app with Docker, then call the API:"
Enter
Type "# docker compose up --build"
Enter
Sleep 1000ms

Type "# python3 -m json.tool only formats the JSON output"
Enter
Sleep 700ms

Type "# Check that borsa is running"
Enter
Type "curl -s http://localhost:8000/v1/health | python3 -m json.tool"
Enter
Sleep 2300ms

Type "# Get one live EGX quote"
Enter
Type "curl -s http://localhost:8000/v1/quote/COMI | python3 -m json.tool"
Enter
Sleep 4200ms

Type "# Explore the rest at http://localhost:8000/docs"
Enter
Sleep 1600ms

Sleep 1s
