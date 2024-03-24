"""Extract United States FDIC-insured banking institution websites from the BankFind API
and write them to a .txt allowlist
"""

import ipaddress
import logging
import math
import re
import socket
import datetime

import requests
import tldextract

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(message)s")


def current_datetime_str() -> str:
    """Current time's datetime string in UTC

    Returns:
        str: Timestamp in strftime format "%d_%b_%Y_%H_%M_%S-UTC".
    """
    return datetime.datetime.now(datetime.UTC).strftime("%d_%b_%Y_%H_%M_%S-UTC")


def clean_url(url: str) -> str:
    """Remove zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes from a URL

    Args:
        url (str): URL.

    Returns:
        str: URL without zero width spaces, leading/trailing whitespaces, trailing slashes,
    and URL prefixes.
    """
    removed_zero_width_spaces = re.sub(r"[\u200B-\u200D\uFEFF]", "", url)
    removed_leading_and_trailing_whitespaces = removed_zero_width_spaces.strip()
    removed_trailing_slashes = removed_leading_and_trailing_whitespaces.rstrip("/")
    removed_https = re.sub(r"^[Hh][Tt][Tt][Pp][Ss]:\/\/", "", removed_trailing_slashes)
    removed_http = re.sub(r"^[Hh][Tt][Tt][Pp]:\/\/", "", removed_https)

    return removed_http


def extract_urls() -> set[str]:
    """Extract United States FDIC-insured banking institution websites from the BankFind API

    Returns:
        set[str]: Unique United States FDIC-insured banking institution URLs.
    """
    url_column_names: list[str] = ["TE%sN528" % str(i + 1).zfill(2) for i in range(10)]

    try:
        # Get total entries
        res: requests.Response = requests.get(
            "https://banks.data.fdic.gov/api/institutions", timeout=30
        )
        res.raise_for_status()
        max_entries_per_call: int = 10000
        total: int = res.json().get("meta", 0).get("total", 0)
        num_pages: int = int(math.ceil(total / max_entries_per_call))

        # Get active institutions
        institutions = []
        for page in range(num_pages):
            res = requests.get(
                "https://banks.data.fdic.gov/api/institutions?filters=ACTIVE:1&fields=NAME,"
                f"{','.join(url_column_names)}&limit={max_entries_per_call}&offset={page*max_entries_per_call}",
                timeout=60,
            )
            if res.status_code != 200:
                continue
            institutions.extend(
                [y for x in res.json().get("data", []) if (y := x.get("data", None))]
            )

        institutions_with_urls = []
        for institution in institutions:
            institution_name: str = institution.get("NAME", "").strip()
            institution_urls = sorted(
                set(institution.get(col, "").strip() for col in url_column_names)
                - set([""])
            )
            if institution_name and institution_urls:
                institutions_with_urls.append((institution_name, institution_urls))

        urls: set[str] = set()
        for _, institution_urls in institutions_with_urls:
            for url in institution_urls:
                urls.add(clean_url(url))
        return urls
    except Exception as error:
        logger.error(error)
        return set()


if __name__ == "__main__":
    urls: set[str] = extract_urls()
    ips: set[str] = set()
    non_ips: set[str] = set()
    fqdns: set[str] = set()

    if not urls:
        raise ValueError("Failed to scrape URLs")
    for url in urls:
        res = tldextract.extract(url)
        domain, fqdn = res.domain, res.fqdn
        if domain and not fqdn:
            # Possible IPv4 Address
            try:
                socket.inet_pton(socket.AF_INET, domain)
                ips.add(domain)
            except socket.error:
                # Is invalid URL and invalid IP -> skip
                pass
        elif fqdn:
            non_ips.add(url)
            fqdns.add(fqdn.lower())

    if not non_ips and not ips:
        logger.error("No content available for allowlists.")
    else:
        non_ips_timestamp: str = current_datetime_str()
        non_ips_filename = "urls.txt"
        with open(non_ips_filename, "w") as f:
            f.writelines("\n".join(sorted(non_ips)))
            logger.info(
                "%d non-IPs written to %s at %s",
                len(non_ips),
                non_ips_filename,
                non_ips_timestamp,
            )

        ips_timestamp: str = current_datetime_str()
        ips_filename = "ips.txt"
        with open(ips_filename, "w") as f:
            f.writelines("\n".join(sorted(ips, key=ipaddress.IPv4Address)))
            logger.info(
                "%d IPs written to %s at %s", len(ips), ips_filename, ips_timestamp
            )

        fqdns_timestamp: str = current_datetime_str()
        fqdns_filename = "urls-pihole.txt"
        with open(fqdns_filename, "w") as f:
            f.writelines("\n".join(sorted(fqdns)))
            logger.info(
                "%d FQDNs written to %s at %s",
                len(fqdns),
                fqdns_filename,
                fqdns_timestamp,
            )
