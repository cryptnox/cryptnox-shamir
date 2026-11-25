<p align="center">
  <img src="https://github.com/user-attachments/assets/6ce54a27-8fb6-48e6-9d1f-da144f43425a"/>
</p>

<h3 align="center">cryptnox-shamir</h3>
<p align="center">Operating documentation for the Cryptnox Shamir card system</p>

<br/>
<br/>

[![docs](https://github.com/cryptnox/cryptnox-shamir/actions/workflows/deploy.yml/badge.svg)](https://github.com/cryptnox/cryptnox-shamir/actions/workflows/deploy.yml)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

Documentation for **Cryptnox Shamir**: a hardware-backed system that splits a
single master secret (a Bitcoin treasury key, an HSM wrapping key, a recovery
seed) across `n` smart cards, any `k` of which are enough to reconstruct it.
No single card, and no single person, ever holds the secret.

Published at
[docs.cryptnox.com/cryptnox-shamir](https://docs.cryptnox.com/cryptnox-shamir/),
part of the [Cryptnox documentation portal](https://docs.cryptnox.com).

---

## Contents

| Section | Pages |
|---------|-------|
| **Getting started** | Overview, Concepts, Cards, Installation |
| **Operating procedures** | Cheat sheet, The Ceremony, Recovery, Backup Test, Choosing Parameters, Custody Governance & Checklists, Printable Checklist |
| **Reference** | Security Model, Command Reference, Troubleshooting |

A single PDF of the whole manual is built with every deploy and linked from the
site's index page.

---

## Building locally

```bash
pip install -r requirements.txt
sphinx-build -W -b html docs/source docs/_build/html
```

For the PDF (requires a LaTeX installation with latexmk):

```bash
sphinx-build -M latexpdf docs/source docs/_build
```

---

## Get your hardware

Cryptnox smart cards and compatible readers are available at
[shop.cryptnox.com](https://shop.cryptnox.com).

---

## License

Copyright (C) 2026 Cryptnox SA.

This documentation is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) (see [`LICENSE`](LICENSE)):

- **Attribution** for appropriate credit to Cryptnox SA
- **NonCommercial** for non-commercial use only
- **NoDerivatives** for unmodified redistribution only

The `shamir-cli` software and the card applets are proprietary to Cryptnox SA
and are not covered by this license.

For inquiries, contact: contact@cryptnox.com
