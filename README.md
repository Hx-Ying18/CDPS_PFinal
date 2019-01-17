# DEPLOY

Deploy is a Python CLI for deploying [QUIZ](https://github.com/CORE-UPM/quiz_2019) web app in a reliable and scalable arquitecture.

## Installation

Install click and activate the venv; the command will work on the directory pfinal/.

```bash
python3 installClick.py
. venv/bin/activate
cd /pfinal
```

## Usage

In the directory pfinal/.
```bash
. venv/bin/activate
cd /pfinal
deploy up # Complete deployment, followed by questions.
deploy destroy # Destroy the arquitecture.
deploy restart # Restart the arquitecture.

```
If type (y) it will be continue, if no the system will be destroy.
In this way, through atomic operations is achieved the idempotent deploy.

Specific commands info:

```bash
deploy --help
```

For fast deployment:
```bash
yes | deploy up 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)




