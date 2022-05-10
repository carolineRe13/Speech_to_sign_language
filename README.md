# Project description
This is the backend for a speech-to-signLanguage app making use of Natural Language Processing and the Google 
speech-to-text API. The final translation is shown as a video with subtitles. If a word is not available in the database 
then the word is displayed on a black screen.

The [frontend](https://imagemagick.org/script/download.php) is written in React.

# Getting started 
The following guide explains how to set up this project.
## Set up the database

### Prerequisites
- Install [ImageMagick](https://imagemagick.org/script/download.php) as it is needed to write texts with the moviepy 
  library.
- Clone [WLASL Git repository](https://github.com/dxli94/WLASL.git)

##### Note: [WLASL Git repository](https://github.com/dxli94/WLASL.git) is used to retrieve the open-source videos for the database.

### Download database content
To get the database you must configure your parameters first. The first needed parameter is your local file path to 
WLASL_v0.3.json from [WLASL Git repository](https://github.com/dxli94/WLASL.git). The second parameter is the file path
to the required database destination. Finally, run the DatabaseBuilder.py in the start_kit folder under code.

## Run project
### Prerequisites
- Install the database as described above.
- Place your googleCloud key under codeBase/keys.

### Final step

Run the [frontend](https://imagemagick.org/script/download.php) and main.py under codeBase.

## Run tests
To run test, please add your own audio files.