# FDIC-insured banking institution websites

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

[![LICENSE](https://img.shields.io/badge/LICENSE-BSD--3--CLAUSE-GREEN?style=for-the-badge)](LICENSE)
[![scraper](https://img.shields.io/github/actions/workflow/status/elliotwutingfeng/FDIC-insured-banking-institution-websites/scraper.yml?branch=main&label=SCRAPER&style=for-the-badge)](https://github.com/elliotwutingfeng/FDIC-insured-banking-institution-websites/actions/workflows/scraper.yml)
![Total Allowlist URLs](https://tokei-rs.onrender.com/b1/github/elliotwutingfeng/FDIC-insured-banking-institution-websites?label=Total%20Allowlist%20URLS&style=for-the-badge)

Machine-readable `.txt` allowlist of websites belonging to banking institutions insured by the [United States FDIC (Federal Deposit Insurance Corporation)](https://fdic.gov), updated once a day.

Data is sourced from the public domain [FDIC BankFind API](https://banks.data.fdic.gov).

**Disclaimer:** _This project is not sponsored, endorsed, or otherwise affiliated with the United States Government._

## Allowlist download

| File | Download |
|:-:|:-:|
| urls.txt | [:floppy_disk:](urls.txt?raw=true) |
| urls-pihole.txt | [:floppy_disk:](urls-pihole.txt?raw=true) |
| ips.txt | [:floppy_disk:](ips.txt?raw=true) |

## Requirements

- Python 3.12+

## Setup instructions

`git clone` and `cd` into the project directory, then run the following

```bash
python3 -m venv venv
venv/bin/python3 -m pip install --upgrade pip
venv/bin/python3 -m pip install -r requirements.txt
```

## Usage

```bash
venv/bin/python3 scraper.py
```

## Libraries/Frameworks used

- [tldextract](https://github.com/john-kurkowski/tldextract)

&nbsp;

<sup>These files are provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, arising from, out of or in connection with the files or the use of the files.</sup>

<sub>Any and all trademarks are the property of their respective owners.</sub>
