Concepts
========

This page explains the vocabulary used throughout the rest of the
documentation. Read it once before your first ceremony.

Shamir Secret Sharing (SSS)
---------------------------

A secret is split into ``n`` **shares**. Any ``k`` of them
(the **threshold**) reconstruct the secret exactly; any ``k-1`` reveal
**nothing** about it.

Notation: a **k-of-n** scheme. For example **2-of-3** means three shares
exist and any two of them recover the secret.

The trade-off you choose with ``k`` and ``n``:

- A **larger ``n``** means more redundancy — you can lose more cards.
- A **larger ``k``** means more security — an attacker needs more cards — but
  also more cards required to recover, so less convenience.

See :doc:`parameters` for guidance on choosing them.

.. figure:: _static/shamir_concept.*
   :alt: A secret split into n shares, any k of which rebuild it
   :align: center
   :width: 100%

   Shamir's Secret Sharing — the secret is split into *n* shares; any *k* of
   them reconstruct it exactly, while any fewer reveal nothing.

The two card types
------------------

.. list-table::
   :header-rows: 1
   :widths: 18 52 12

   * - Card
     - Role
     - Quantity
   * - **Orchestrator**
     - Performs all cryptographic operations: generates the seed, splits it,
       exports the encrypted shares, and reconstructs the seed during
       recovery. Holds no share at rest; it is reset and reused between
       operations.
     - 1
   * - **Storage**
     - Securely stores exactly **one** encrypted share, protected by a
       4-character PIN. Performs no secret-sharing computation itself.
     - ``n`` (2–12)

The secret (the "seed")
-----------------------

The protected value is called the **seed**. It can be:

- a Bitcoin / secp256k1 private key,
- a NIST EC private key (P-256 / P-384 / P-521),
- or any random byte string (e.g. an HSM wrapping key, an AES key).

Sizes range from 16 to 128 bytes. See :doc:`parameters`.

The HSM and the "wrapped seed"
------------------------------

In production the live secret is expected to live inside an **HSM**
(Hardware Security Module). The Shamir cards are the **offline backup**.

When the orchestrator outputs the seed, it never does so in plaintext. It
encrypts ("**wraps**") the seed with the HSM's **RSA public key**. The
resulting file — the **wrapped seed** — can only be opened inside the HSM that
holds the matching private key. The machine running ``shamir-cli`` cannot read
it.

.. note::

   You supply the HSM public key with ``--rsa-key-file``. Only the HSM that
   holds the matching private key can later open the wrapped seed; the
   ceremony host never sees the secret in the clear.

The three operations
--------------------

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Operation
     - What it does
   * - **Ceremony**
     - The one-time event that generates a seed, splits it, and writes the
       shares to the storage cards. Afterwards the cards are sealed in safes.
       See :doc:`ceremony`.
   * - **Backup test**
     - A periodic health check that confirms the shares still reconstruct the
       seed — **without ever exporting the seed**. See :doc:`backup_test`.
   * - **Recovery**
     - Gather ``k`` storage cards and reconstruct the seed (e.g. after the
       HSM is lost), re-wrapping it for a new HSM. See :doc:`recovery`.

.. note::

   Beyond the full backup test (which needs ``k`` cards), any **single**
   storage card can verify **itself** — proving its share is genuine and belongs
   to the set — without gathering the others. See :ref:`single-card-verify`.

Card states
-----------

Each card moves through a small state machine. The most relevant states:

**Orchestrator**

- ``0x00`` — Initial (reset). The clean starting point for any operation.
- ``0x11``–``0x14`` — progressing through a ceremony.
- ``0x41``–``0x44`` — progressing through a recovery.

**Storage**

- ``0x00`` — Initial (no share).
- ``0x01`` — Ready (key generated, awaiting a share).
- ``0x02`` — Loaded (holds a share).

You can inspect a card's state at any time with ``shamir-cli orchestrator
info`` or ``shamir-cli storage info``.

.. note::

   Commands must follow each state machine in order. Sending a command that
   the current state does not allow returns ``SW=6985`` ("command not allowed
   in current state"). When in doubt, reset to ``0x00`` and start over.

.. seealso::

   - :doc:`parameters` — how to choose ``k`` and ``n``.
   - :doc:`security_model` — what a stolen card reveals, PINs, audit.
   - :doc:`ceremony` — concepts put into practice.
