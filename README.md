# Media tools

_(under construction)_

A set of scripts that extracts samples from arbitrary media, extracts features from those samples, and recombines them in various ways. For example, this will sort an audio file by frequency:

```
python sort_audio.py -in "media/sample/sonata.mp3" -sort "hz=asc" -out "output/sonata_sorted_by_hz.mp3"
```

Where `sort` can be one of: [tsne](https://lvdmaaten.github.io/tsne/) (spectral similarity), `hz` (frequency), `power` (volume), `clarity` (clear harmonic bands), `dur` (clip duration)

## Requirements

These are the requirements for the full workflow below, but each individual script has it's own subset of requirements.

- [Python](https://www.python.org/) (I developed using 2.7, but should be compatible with 3.6+ too)
- [SciPy](https://www.scipy.org/) for math functions (probably already installed)
- [FFmpeg](https://www.ffmpeg.org/) for working with media files
- [LibROSA](https://librosa.github.io/librosa/) for audio analysis
- [Pydub](http://pydub.com/) for audio manipulation
- [SoX](http://sox.sourceforge.net/) and [pysndfx](https://pypi.org/project/pysndfx/) for audio effects like reverb
- [MoviePy](https://zulko.github.io/moviepy/) for programmatic video editing
- [scikit-learn](https://scikit-learn.org/stable/) for statistics and machine learning features (e.g. TSNE, clustering, classification)
- _(optional)_ [PyOpenCL](https://mathema.tician.de/software/pyopencl/) for GPU-accelerated video processing

## Large collection workflow

The scripts in this repository were mostly designed for analyzing/visualizing very large collections of media. Here's an example workflow:

### Metadata retrieval

Download all movie metadata from Internet Archive that are in the [Fedflix collection](https://archive.org/details/FedFlix) and created by the [National Archives](https://archive.org/details/FedFlix?and[]=creator%3A%22national+archives+and+records+administration%22) and save to CSV file:

```
python scrapers/internet_archive/download_metadata.py -query " collection:(FedFlix) AND mediatype:(movies) AND creator:(national archives and records administration)" -out "tmp/ia_fedflixnara.csv"
```

By default, the above script will look for the largest .mp4 asset and associate it with the `filename` property. You can change this format by adding a flag, e.g. `-format .mp3`. If each record has multiple assets associated with it, add a flag `-multi 1` and each asset with the indicated format will be retrieved and saved as its own row (the record metadata will be the same, except for `filename`)

### Asset download

Next, you can download the assets from each of the movies retrieved from the previous step. You can add a flag to indicate how many parallel downloads to run, e.g. `-threads 3`. Make sure output directory has plenty of space. This particular collection has a 100GB+ of files.

```
python scrapers/internet_archive/download_media.py -in "tmp/ia_fedflixnara.csv" -out "tmp/downloads/ia_fedflixnara/"
```

### Get file features

Then retrieve the file features: video duration, has audio track, has video track. By default, it opens the file to get an accurate duration. You can speed this up by just looking at the metadata (less accurate) by adding flag `-acc 0`.

```
python get_file_features.py -in "tmp/ia_fedflixnara.csv" -dir "tmp/downloads/ia_fedflixnara/"
```

Note that checking for an audio track doesn't guarantee to catch all silent films since some video files may have a silent audio track. These cases will be captured in the next step.

### Audio analysis

Now we analyze each movie file's audio track for "samples." These essentially are clips of audio that have a distinct [onset](https://en.wikipedia.org/wiki/Onset_(audio)) and release. This could be thought of as a distinct sonic "pulse" or syllable in the case of speech. The `-features 1` flag adds an analysis step that looks for each sample's volume (`power`) and pitch (`hz` or frequency.) `note` and `octave` are added for convenience, and the `clarity` feature attempts to measure how distinct a particular note is (i.e. very clear harmonic bands.) Samples with high clarity values should be good candidates for musical notes.

```
python audio_to_samples.py -in "tmp/ia_fedflixnara.csv" -dir "tmp/downloads/ia_fedflixnara/" -out "tmp/sampledata/ia_fedflixnara/%s.csv" -features 1
```

The above command will save _all_ samples to .csv files, where each media file will have one .csv file with its respective sample data. This will take a long time for large collections.

### Audio analysis metadata

Next we will update the original metadata .csv file with metadata about the samples per file, e.g. number of samples, median volume, median pitch. This will help identify which movies are silent or have unusable audio, e.g. if a file has few samples or its `medianPower` is very low.

```
python get_sample_features.py -in "tmp/ia_fedflixnara.csv" -dir "tmp/sampledata/ia_fedflixnara/"
```

### Inspecting audio analysis

Optionally, you can view the stats of the samples you created:

```
python stats.py -in "tmp/ia_fedflixnara.csv" -plot "duration,samples,medianPower,medianHz,medianClarity,medianDur"
```

Or view more detailed stats of an individual file's samples:

```
python stats.py -in "tmp/sampledata/ia_fedflixnara/gov.archives.111-tv-221.mp4.csv"
```

Or view two properties as a scatter plot:

```
python plot.py -in "tmp/sampledata/ia_fedflixnara/gov.archives.111-tv-221.mp4.csv" -props "power,hz"
```

### Visualizing audio

TODO


## Small collection workflow

TODO
