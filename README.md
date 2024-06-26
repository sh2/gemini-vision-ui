# gemini-vision-ui

Simple Web UI to try out Gemini Vision.

## Setup

An example of the setup procedure is shown below.

```bash
git clone https://github.com/sh2/gemini-vision-ui.git
cd gemini-vision-ui/src
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
cp template_script.sh script.sh
vim script.sh
./script.sh
```

## Usage

First, upload your image files.
The format is JPEG or PNG, and each file can be up to 20 MB.
Large images will be automatically scaled down.
You may upload multiple files.

![alt text](img/usage_1.png)

Next, ask a question about the image,
Gemini will then return a message.

![alt text](img/usage_2.png)
