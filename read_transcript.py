import json

files = ["meeting.json", "meeting2.json"]

for file in files:

    with open(file) as f:
        data = json.load(f)

    transcript = data["results"]["transcripts"][0]["transcript"]

    print("\nFile:", file)
    print("Transcribed Text:\n")
    print(transcript)