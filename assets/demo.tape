# VHS tape file for recording terminal demo
# Install: go install github.com/charmbracelet/vhs@latest
# Run:     vhs assets/demo.tape
# Output:  assets/demo.gif

Output assets/demo.gif

Set FontSize 16
Set Width 1000
Set Height 600
Set Theme "Monokai"
Set Padding 20

Type "pip install promptpressure"
Enter
Sleep 1s
Type "promptpressure --version"
Enter
Sleep 1s
Type "promptpressure list-suites"
Enter
Sleep 3s
Type "promptpressure mock-agent --port 8010 --mode leaky_system_prompt &"
Enter
Sleep 1.5s
Type "promptpressure scan --url http://localhost:8010 --mode quick_check --output-json results.json --fail-on none"
Enter
Sleep 5s
