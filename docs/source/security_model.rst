Security Model
==============

This page is written for **risk, security, and compliance teams**. It
describes what the system protects, what each actor can see, and the
assumptions you must uphold for the guarantees to hold.

The core guarantee
------------------

The secret is split with Shamir's Secret Sharing into ``n`` shares with
threshold ``k``:

- **Any ``k`` shares** reconstruct the secret exactly.
- **Any ``k - 1`` shares** reveal **nothing** — this is information-theoretic,
  not merely "computationally hard". Fewer than ``k`` shares are as useless as
  zero shares.

On top of this, the hardware ensures the secret and the individual shares are
**never present in plaintext on the host PC**.

What each actor can see
-----------------------

**The host PC** (running ``shamir-cli``) only ever handles:

- non-secret public values exchanged between the cards,
- **encrypted** shares (unreadable outside the cards),
- the **RSA-wrapped** seed (readable only by the HSM's private key).

The host **never** sees the seed in plaintext, a share in plaintext, or any
private key.

**A single storage card** holds exactly one **encrypted** share, behind a PIN.

**The orchestrator card** is the only place the seed exists in plaintext, and
only transiently in volatile memory during a ceremony or recovery. It is
erased on reset and after export.

What a stolen card reveals
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Attacker has…
     - …and learns
   * - One storage card — back markings
     - The bundle ID and a **share number** only. The total ``n`` and threshold
       ``k`` are **not** on the card (custody log only), so a found card does
       not reveal the scheme.
   * - One storage card, no PIN
     - Nothing. The share is encrypted and PIN-gated.
   * - One storage card, with PIN
     - One share — **useless alone**. ``k`` cards are still required.
   * - ``k - 1`` storage cards, all PINs
     - **Nothing about the secret** (Shamir guarantee).
   * - ``k`` storage cards, all PINs
     - The secret. This is the quorum you defined — protect at least
       ``n - k + 1`` cards from any single adversary.

.. note::

   Choose ``k`` so that no single individual, site, or failure can assemble
   ``k`` cards. Distribute the cards across **independent** custodians and
   locations.

PIN protection
--------------

- Each storage card is protected by a **4-character PIN**.
- **Three** consecutive wrong PINs **lock** the card.
- Change a card's PIN with ``shamir-cli storage change-pin``.
- The factory default PIN is ``0000`` — **change it** before going to
  production.

Card sets
---------

The orchestrator and its storage cards form a **matched set**: an orchestrator
only works with storage cards that belong to the same set, and rejects any
card from outside it. This prevents an attacker from slipping a rogue storage
card into a ceremony or recovery.

.. note::

   In production, the cards you receive are already provisioned as a set — you
   do not configure this. Simply use the cards that were delivered together.

Seed wrapping (transport to the HSM)
------------------------------------

When the orchestrator outputs the seed it always encrypts it with the HSM's
**RSA public key**. Only the HSM holding the matching private key can open the
resulting ``wrapped_seed.bin``. Provide that key with ``--rsa-key-file``.

.. warning::

   If you omit ``--rsa-key-file``, the tool generates a **throwaway** key for
   convenience during evaluation, and the wrapped file cannot be opened once
   the process exits. **Never** do this with a real secret — always supply
   your HSM's public key in production.

Audit: the export counter
-------------------------

Every real share read during a recovery increments a non-volatile **counter**
inside the storage card. Inspect it:

.. code-block:: bash

   shamir-cli storage read-counter

A counter higher than your records expect means a share was read outside a
sanctioned recovery — investigate. (The :doc:`backup_test` does **not**
increment this counter, so routine checks do not pollute the audit trail.)

Assumptions you must uphold
---------------------------

For the guarantees above to hold:

#. The **ceremony host is trusted** and offline at ceremony time.
#. **Cards and PINs are distributed** so no single adversary can gather ``k``.
#. The **HSM RSA public key** used for wrapping is authentic (verify its
   fingerprint out-of-band).
#. The **physical card labels** (share indices) are recorded and protected —
   recovery relies on inserting cards in share-index order
   (:ref:`ceremony:labelling`).

.. seealso::

   - :doc:`concepts` — the HSM and wrapped seed in plain terms.
   - :doc:`parameters` — translating policy into ``k`` and ``n``.
   - :doc:`ceremony` — the operational controls in practice.
