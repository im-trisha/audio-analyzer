
### Audio analyzer

I don't really have much time at the moment to write a proper readme honestly. Very briefly:

This program does the following:
- Extract every audio to wav format from videos in the sources directory
- Get their audio data (For speech recognition) and save it inside the audiodata.pickle file
- Recognize speech for every audio and save it inside the cache/speeches directory
- Find in every video's text the text that has been specified by the -s parameter in the command line and tell you approximately where it was found

Now that everything is cached (For a total of 20GB of videos I had to leave it for about 4 hours on the first run), following runs will take about 3 to 4 seconds at max.

### Usage

Download dependencies: `poetry install`

You'll need to download the VOSK model. To do so, just use the integrated script:
To downloda: `poetry run python -m audio_analyzer.download_vosk some-vosk-model`

Just use poetry and run the program like such: `poetry run python -m audio_analyzer -s "TextTo Search caSe doesn't Matter" --vosk-model some-vosk-model`

### Notes
- As the part where the audio was found is an approximation, its not reliable. Surely the video is not 100% speaking and will have blank parts, meaning that if the approximation says the audio was found at 00:05:25 you can safely skip 10 or 20 seconds at least.
- There are junk packages in the pyproject.toml if you want to use any other recognition model, you're free to, just edit the code, I saved myself from that hassle.