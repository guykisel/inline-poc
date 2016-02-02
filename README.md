# inline-poc
Quick proof of concept for https://github.com/guykisel/inline-plz


# testing
* `prospector --strictness veryhigh -M > output.txt`
* `python inline-cli.py --owner guykisel --repo inline-poc --filename output.txt --user guykisel --token <token> --pr 2`
