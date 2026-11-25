<p align="center">
  <img src="https://github.com/user-attachments/assets/6ce54a27-8fb6-48e6-9d1f-da144f43425a"/>
</p>

<h3 align="center">cryptnox-shamir</h3>
<p align="center">Documentation for the Cryptnox Shamir Secret Sharing card system</p>

<br/>

[![Documentation status](https://img.shields.io/badge/docs-latest-blue)](https://docs.cryptnox.com/cryptnox-shamir/)
[![PDF](https://img.shields.io/badge/PDF-download-blue)](https://docs.cryptnox.com/cryptnox-shamir/cryptnox-shamir.pdf)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

`cryptnox-shamir` is the operating documentation for the **Cryptnox Shamir
card system**: a hardware-backed scheme that splits a single high-value secret
(a Bitcoin treasury key, an HSM wrapping key, a recovery seed) into `n` shares
held on tamper-resistant smart cards, any `k` of which are enough to
reconstruct it. No single card, and no single person, ever holds the secret.

The seed is generated, split and reconstructed **inside the cards**: the host
PC never sees it in plaintext. The system is built for **institutional
custody** (corporate Bitcoin treasuries, funds, exchanges) and for the typical
**disaster-recovery backup** of a key that lives in an HSM.

The documentation is published on the
[Cryptnox documentation portal](https://docs.cryptnox.com/cryptnox-shamir/),
with a [PDF manual](https://docs.cryptnox.com/cryptnox-shamir/cryptnox-shamir.pdf)
built at every deploy.

---

## Supported hardware

### Cryptnox Shamir smart cards

| Card | Role | Per set |
|------|------|---------|
| **Orchestrator** (blue) | Generates the seed, splits it, and reconstructs it during recovery. Holds no share at rest | 1 |
| **Storage** (teal) | Holds exactly one encrypted share, protected by a PIN | 2 to 12 |
| **Admin** (gold) | Resets the PIN of a storage card; itself PIN-protected | 1 |

### Smart card readers

The Shamir applets work over the **contact** interface only (contactless/NFC is
rejected): use a PC/SC contact reader and insert the card.

| Reader | Type | Connector |
|--------|------|-----------|
| Any PC/SC contact reader, e.g. the [Cryptnox® Smartcard Reader](https://shop.cryptnox.com/product/cryptnox-smartcard-reader/) | Contact (ISO/IEC 7816) | USB |

---

## Build locally

```bash
pip install -r requirements.txt
sphinx-build -b html docs/source docs/_build/html
```

Then open `docs/_build/html/index.html` in your browser.

For the PDF (requires a LaTeX installation with latexmk):

```bash
sphinx-build -M latexpdf docs/source docs/_build
```

---

## Documentation

The generated documentation for this project is available [here](https://docs.cryptnox.com/cryptnox-shamir/).

Order card sets through the [Shamir Secret Sharing Cards page](https://cryptnox.com/shamir-secret-sharing-cards/);
readers are at [shop.cryptnox.com](https://shop.cryptnox.com).

---

## License

`cryptnox-shamir` documentation is licensed under [CC BY-NC-ND 4.0](LICENSE):

- **Attribution** for appropriate credit to Cryptnox SA
- **NonCommercial** for non-commercial use only
- **NoDerivatives** for unmodified redistribution only

The `shamir-cli` software and the card applets are proprietary to Cryptnox SA
and are not covered by this license.

For inquiries, contact: contact@cryptnox.com
