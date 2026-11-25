The Ceremony
============

The **ceremony** is the one-time event in which you generate a master secret,
split it into shares, and write each share to a storage card. It is the most
important procedure in the system and should be performed deliberately, under
controlled conditions.

.. note::

   **Generate vs import.** In ``full-ceremony`` (this page) the seed is
   **generated on the orchestrator** — you never enter it, and it never exists
   off the card. This is the most secure option and the recommended default.
   To back up a key that **already exists** (for example a treasury key you
   hold elsewhere), use the **import ceremony** instead — see
   :ref:`ceremony:importing-an-existing-seed`.

Throughout this page we use a **2-of-3** ceremony (three cards, any two
recover) with a 256-bit seed **purely as a worked example**. It is not a fixed
or recommended value — substitute your own ``-n``, ``-k`` and ``-s`` for any
supported configuration (:doc:`parameters`).

.. note::

   **2-of-3 is just an example.** The system supports ``n`` from 2 to 12 and
   ``k`` from 2 to 7. Choose the quorum that matches your custody policy.

.. important::

   **The provisioned count is a ceiling, not a quota.** A set ships with a fixed
   number of storage cards — that is the **maximum** ``n``. At the ceremony you
   choose **any** valid ``k``-of-``n`` with ``n`` ≤ the cards you hold: you may
   use fewer and leave the spares unused. You only cannot set ``n`` *higher* than
   the number of cards. The k-of-n is **not** marked at the factory — you write
   it on the cards (see :ref:`ceremony:labelling`), so you are free to decide it
   right up to the ceremony.

.. figure:: _static/ceremony_flow.*
   :alt: Ceremony steps: generate, split, load shares, backup test, wrap to HSM
   :align: center
   :width: 100%

   The ceremony at a glance — the seed is generated and split on the
   orchestrator, distributed to the storage cards, verified by a backup test,
   then exported RSA-wrapped to the HSM.

Before you begin
----------------

Prepare:

- **1 orchestrator card** in state ``0x00`` (reset if needed — see below).
- **``n`` storage cards** from the same set, in state ``0x00`` (3 for this
  example).
- The **RSA public key of your HSM**, exported to a file (e.g.
  ``hsm_pubkey.pem``). This is the key the seed will be wrapped for.
- The **factory blessing bundle** for this set (``*.bundle.json``). It lets
  the orchestrator accept the storage cards of this set. It is produced when the cards are
  enrolled at the factory. Only ``--test-mode`` runs without one.

.. admonition:: Production checklist
   :class: important

   - Perform the ceremony on a **trusted, offline machine** in a controlled
     location, ideally with multiple officers present (four-eyes principle).
   - Use your real **HSM RSA public key** via ``--rsa-key-file``. Without it,
     the tool generates a throwaway test key and the resulting wrapped seed
     is **not usable** in production.
   - **Write each card's share number as you load it** (#1, #2, #3 …) and keep
     the cards in that order. The card cannot report its own share index, so
     recovery relies on what you write on the back. See :ref:`ceremony:labelling`.

Running the ceremony
--------------------

.. code-block:: bash

   shamir-cli workflow full-ceremony \
     -n 3 \
     -k 2 \
     -s 32 \
     -t f \
     --blessings-bundle ./batch.bundle.json \
     --rsa-key-file hsm_pubkey.pem \
     --output-dir ./ceremony-output

.. note::

   ``--blessings-bundle`` may be **omitted** only if exactly one
   ``*.bundle.json`` sits in the working directory — it is then auto-discovered.
   A real ceremony always consumes one; only ``--test-mode`` runs without a
   bundle.

Options:

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Option
     - Meaning
   * - ``-n, --total``
     - Total number of storage cards / shares (2–12).
   * - ``-k, --threshold``
     - Minimum cards required to recover (2–7, ``k ≤ n``).
   * - ``-s, --seed-size``
     - Seed size in bytes: ``16 | 32 | 48 | 64 | 66 | 128``.
   * - ``-t, --seed-type``
     - ``f`` random · ``r`` EC r1 key · ``k`` secp256k1 key.
   * - ``--blessings-bundle``
     - Factory blessing bundle for this card set (``*.bundle.json``).
       Auto-discovered in the working dir if omitted.
   * - ``--wallet-hsm``
     - Use a Cryptnox wallet on this reader as the HSM: the seed is imported
       straight into it, nothing on disk. The wallet must be initialised and
       hold no seed (``NO_SEED``). See :ref:`ceremony:hsm`.
   * - ``--wallet-pin``
     - PIN of the wallet used with ``--wallet-hsm`` (default ``0000``).
   * - ``--rsa-key-file``
     - HSM RSA public key (PEM/DER) used to wrap the seed.
   * - ``--kms-key-id``
     - AWS KMS asymmetric RSA key used to wrap the seed. Pass the **full ARN**
       of an existing key. See :ref:`ceremony:hsm`.
   * - ``--kms-region``
     - AWS region for ``--kms-key-id`` (default ``eu-north-1``).
   * - ``--output-dir``
     - Where to write the wrapped seed file.

With a single reader, the tool prompts you to insert and swap cards:

.. code-block:: text

   Insert Orchestrator card and press Enter...
   Insert Storage card #1 and press Enter...
   Swap back to Orchestrator card and press Enter...
   Insert Storage card #2 and press Enter...
   ...

.. tip::

   With **two readers** you can keep the orchestrator in one and only change
   the storage card in the other, which reduces card swaps considerably.

.. _ceremony:hsm:

Where the seed goes (the HSM)
-----------------------------

The generated seed never touches the disk in the clear — it is RSA-wrapped
inside the orchestrator and handed to **exactly one** recipient (the "HSM").
Choose one of:

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Recipient
     - How
   * - **Cryptnox wallet**
     - ``--wallet-hsm <reader>`` (+ ``--wallet-pin``). The seed is imported
       straight into the wallet on-card; nothing is written to disk. The wallet
       must be initialised and ``NO_SEED``. Both wallet generations are
       accepted (the SDK reports either ``Basic`` or ``BasicG1``).
   * - **AWS KMS**
     - ``--kms-key-id <arn>`` (+ ``--kms-region``). The seed is wrapped to an
       AWS KMS asymmetric RSA key; KMS holds the private half and can decrypt
       it later. The wrapped blob is written to ``--output-dir``.
   * - **External RSA HSM**
     - ``--rsa-key-file <pem>``. The seed is wrapped to that public key and
       written to ``--output-dir`` as ``wrapped_seed.bin``.

.. _ceremony:kms:

AWS KMS — credentials and key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The KMS recipient talks to AWS through **boto3**. No secret is stored in this
tool; credentials come from the standard AWS chain:

#. Environment variables — ``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``,
   ``AWS_DEFAULT_REGION``; or
#. a shared profile written by ``aws configure`` (``~/.aws/credentials`` +
   ``~/.aws/config``); or
#. an IAM role (when running on an EC2 instance / container).

Create an access key in the AWS console under
**IAM → Users → <user> → Security credentials → Access keys → Create access
key** (use case *Command Line Interface*). The **Secret Access Key is shown only
once** — save it. Then::

   aws configure          # Access Key ID + Secret + region (e.g. eu-north-1)
   aws sts get-caller-identity   # verify: prints your ARN, not an error

.. important::

   Pass the **full key ARN** to ``--kms-key-id``, e.g.
   ``arn:aws:kms:eu-north-1:<account>:key/<key-id>``. A **bare key-id** (just the
   UUID) is interpreted as an *alias name* and the tool will try to **create** a
   key — which fails with ``AccessDeniedException`` on ``kms:CreateKey`` unless
   you hold that permission. An ``alias/<name>`` is also accepted and is created
   on first use (needs ``kms:CreateKey`` + ``kms:CreateAlias``).

   The key must be an **asymmetric RSA** key with usage *ENCRYPT_DECRYPT*
   (RSA-2048 or larger). Minimum permissions to use an existing key:
   ``kms:GetPublicKey`` (to wrap) and ``kms:Decrypt`` (to recover / verify).

On success the ceremony wraps the seed to KMS, writes
``kms_wrapped_seed.bin``, and re-decrypts it through KMS to confirm the
checksum matches the on-card seed (``KMS decrypt check: checksum match =
True``).

How it works
------------

1. **Reset the orchestrator** to a clean state and enter Ceremony mode.
2. **Register each storage card.** Each card and the orchestrator
   authenticate one another, and the orchestrator records the card.
3. **Load the HSM RSA wrapping key.**
4. **Generate the seed** inside the orchestrator. It returns a *checksum*
   (a short fingerprint) — **write it down**.
5. **Export each share**, encrypted for its specific storage card, and load
   it into that card.
6. **Backup test.** The orchestrator reads the shares back and confirms they
   reconstruct the original seed. (All ``n`` shares are exercised.)
7. **Export the RSA-wrapped seed** to ``ceremony-output/wrapped_seed.bin``.

A successful run ends with a summary panel:

.. code-block:: text

   ╭──────────────────────── Summary ─────────────────────────╮
   │ Ceremony Complete                                        │
   │   Shares: 3 total, 2 required                            │
   │   Seed: 256-bit, type=f                                  │
   │   Seed checksum: 33 F4 A2 59 31 57 9D 19                 │
   │   Wrapped seed: wrapped_seed.bin                         │
   ╰──────────────────────────────────────────────────────────╯

.. _ceremony:labelling:

Card order (share numbers)
--------------------------

The card backs are a **printed form** — the factory does not mark the k-of-n.
As you run the ceremony, **you write** on each storage card's back:

- the **bundle name** (the set identifier),
- this card's **share number** — card #1 first, #2 second, and so on, written as
  you load it, so each label matches the share it actually stores.

.. important::

   **Keep the total and threshold off the cards.** Write only the share number;
   record the full ``k``-of-``n`` in your **custody log**. A single lost or
   stolen card should not reveal how many cards exist or how many are needed.

   The card does not report its share number electronically, so recovery relies
   on the number **you wrote**: at recovery, insert the cards in the same order.
   Inserting them out of order reconstructs the **wrong** secret (the checksum
   will not match). Write legibly and double-check.

Annotate the back of each card
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The back of each card is a printed form with empty fields. In addition to the
set parameters above, fill in a short, **non-identifying** custody marker in the
**Notes** area (see :ref:`hardware:card-backs`):

- **Orchestrator card** — the **Bundle** name, the **administrator's operator
  code**, and the **ceremony date**.
- **Each storage card** — the **custodian code** (assigned by the
  administrator; the scheme is up to your organisation, e.g. ``C-03``) and the
  **ceremony date**.

.. warning::

   Keep the cards **anonymous**: put **no full name and no handwritten
   signature on the card** — both identify a person and make them a target for
   **coercion**. The acknowledgement of receipt (the holder's signature
   against their code) and the **code → name** mapping live **only in your
   custody log**, stored securely.

This keeps each card's role readable at a glance while keeping the people
involved un-targetable from the card alone; accountability lives in the log.

After the ceremony
------------------

You now hold:

- **``n`` storage cards**, each in state ``0x02`` (loaded) and labelled.
  Store them in **separate, secure locations** (different safes / sites).
- **One** ``wrapped_seed.bin`` **file** — import it into your HSM using your
  standard RSA key-import procedure. After import, **destroy the file**; it
  is only an encrypted transport artifact.
- **One orchestrator card**, reset and reusable.

.. tip::

   Before sealing each card in its safe, you can spot-check it on its own with
   ``shamir-cli storage pedersen-verify`` — it confirms that one card holds a
   valid share for this set, without needing the others. See
   :ref:`single-card-verify`.

Record, in your custody log: the **seed checksum**, the ``k`` / ``n``
parameters, the seed size/type, and the physical location assigned to each
labelled card.

.. warning::

   The seed is **never** exported in plaintext. The orchestrator destroys its
   in-memory copy on reset and after export. The only way to recover the seed
   later is the wrapped seed (via the HSM private key) **or** a
   :doc:`recovery` from ``k`` storage cards.

Resetting a card before a ceremony
----------------------------------

If a card is not in state ``0x00``:

.. code-block:: bash

   # Orchestrator
   shamir-cli orchestrator reset

   # Storage (PIN required)
   shamir-cli storage reset --pin 0000

See :doc:`troubleshooting` if a reset is refused.

.. _ceremony:importing-an-existing-seed:

Importing an existing seed
--------------------------

Use **import** when the secret you want to protect **already exists** (for
example a treasury key generated elsewhere) — rather than letting the
orchestrator generate a fresh one. It is the very same ``full-ceremony`` command
with one extra flag: ``--secret-file`` (or ``--secret``).

You **must** supply the secret to import, either as a file (recommended) or as a
hex string:

.. code-block:: bash

   shamir-cli workflow full-ceremony \
     -n 3 \
     -k 2 \
     -s 32 \
     --orch-reader "<orchestrator reader>" \
     --storage-readers "<reader1>,<reader2>,<reader3>" \
     --blessings-bundle ./cards.bundle.json \
     --secret-file ./treasury.hex

- ``--secret-file <file>`` — a file holding the secret. It may be **hex text**
  (e.g. ``00112233…``) or **raw bytes**; either way its length must equal ``-s``.
- ``--secret <hex>`` — the secret inline as hex. Prefer ``--secret-file`` so the
  secret never lands in your shell history.

Everything else is identical to a normal ceremony — the same real cards, the same
factory bundle, the same on-card VSS split and per-card verification — **except**:

- the seed is **imported** (RSA-encrypted to the orchestrator) instead of
  generated on-card; and
- it is **not** re-wrapped to an HSM (you already hold it), so the HSM options
  (``--wallet-hsm`` / ``--rsa-key-file`` / ``--kms-key-id``) do not apply.

.. note::

   ``workflow ceremony-import`` is a separate, **software-only** command (virtual
   storage cards, throwaway test material) kept for simulator demos. For real
   enrolled cards, use ``full-ceremony --secret-file`` as above.

.. important::

   The secret is **required**. ``ceremony-import`` exists precisely to protect a
   key you already hold — it never invents a random one. If you want a fresh
   random seed, use ``full-ceremony`` instead: it generates it **on-card** with
   the smart card's hardware TRNG, which is stronger than any host-side generator.

.. note::

   The secret is imported in **encrypted** form (wrapped to the orchestrator's
   RSA key); it is never sent to the card in the clear, and the orchestrator
   never exposes it. The secret is not printed to the console — only its length
   and the resulting checksum are shown.

.. seealso::

   - :doc:`parameters` — choosing ``n``, ``k``, seed size and type.
   - :doc:`backup_test` — confirm the backup is healthy afterwards.
   - :doc:`recovery` — restore the seed from ``k`` cards.
   - :doc:`security_model` — what a stolen card reveals, PINs, audit.
