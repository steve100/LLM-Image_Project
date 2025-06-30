# LLM_Image-Project

## A lightweight set of programs to:
-  Setup a Python Virtual Environment
-  Read and Extract the metadata (EXIF) from images in an imaage directory
-  Send the Image to a Local LLM model using LM Studio
-  Send the image to a a foundational LLM model using ChatGPT
-  Geocode and Draw a Map

## Testing
Tested Under Windows 11 pro
Should run Under Linux - change the .bat files to .sh files

## Overall
Reactions: 
Surprised at the speed locally and in hte cloud
Pleased it fit in vRAM.
Pleasently pleased that the Local Model had memory of the 5 images I sent and I could prompt for more info.

Disapointed by the local descriptions. However these are small-ish 7b models.

## Pre-Configuration

``
Choose an OS
  Windows 11 currently works better at running models with any program I have found than Linux for non-NVIDIA graphics cards.

Install your graphics card drivers
  I happen to have an AMD Raedon 780m iGPU.

Install LM Studio
  https://lmstudio.ai/download?os=win32

  Allow LM Studio to accept API
  command line: lms server start
  gui: use the developer tab .. but it is a bit difficult to find.

  More info
  https://lmstudio.ai/docs/app/api/tools

  Install a Vision Enabled model - bakllava1-mistralllava-7b was recommended, fits in my vRAM, gives an ok Result.
   Fullname: AI-Engine/BakLLaVA1-MistralLLaVA-7B-GGUF

   I did not have to change the model configuration

Configure it to accept API Requests
 
 Obtain an OpenAI Key
   Free API Keys are NOT available at this time 
   Limit your account to $20 so you do not spend too much money
   https://community.openai.com/t/how-do-i-get-my-api-key/29343
   https://platform.openai.com/docs/models
   https://platform.openai.com/usage

   Images used to be far more expensive than they are today
   Still - if will process a lot of images - locally is the way to go.
   48 images  / 30,000 input tokens / 24 images it cost  $0.08 with model "gpt-4o" 


## Configuration:

```
windows-setup.bat

Make sure the Python Virtual Environment is installed correctly.
  create-virtual-enviroment.txt
  activate.txt
  python-requrements.bat
    requirements.txt
    test-pyexiftool.py
    note pyexiftool==0.4.13  because get_metadata_batch is not in the new version 


Put your API_key and LLM information into the Python .env file
edit .env
```

## Usage:

```
Opional
 dothumbs.bat      
```

## Read the Images:
``
doreadimages.bat
``

## Send the Images to an LLM
``
dodescription-local.bat
dodescription-openai.bat

These programs will create two files captions*

``

Draw and Display A map
domap.bat
This program will create an index.html


Python Code:

``generate_gallery_with_thumbs.py
read_fromimage_metadata.py
description_via_local.py
description_via_openai.py
draw-map-image-metadata.py
``

##Support Files and directories

``
PreLoaded with 1 image
./images
./images/thumbs


output:
Retained for reading.  Will be regenerated with your own images.
  captions_log.txt      - Human Readable    Descriptions/Captions
  captions_output.csv   - Computer Readable Descriptions/Captions

  index.html            - index file for mapping


Errata:
   domap.bat will crash if an image does not have a lat/log
   exercise for later.

   The .env could have image and output directories.
   The .csv could have a unique time stamp to avoid overwriting.

``