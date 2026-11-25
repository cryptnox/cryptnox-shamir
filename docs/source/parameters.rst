Choosing Parameters
===================

Before a ceremony you choose three things: the **quorum** (``k`` of ``n``),
the **seed size**, and the **seed type**. This page helps you pick values
that match your custody policy.

The quorum: ``k`` of ``n``
--------------------------

- **``n``** is the total number of cards (and shares).
- **``k``** is how many of them are required to reconstruct the secret.

The intuition:

- A larger **``n``** gives more **redundancy** — you can afford to lose more
  cards (you can lose up to ``n - k`` and still recover).
- A larger **``k``** gives more **security** — an attacker must compromise
  more cards — at the cost of needing more people/locations to recover.

.. note::

   The two are independent. ``3-of-5`` survives the loss of 2 cards **and**
   requires 3 to recover; ``2-of-5`` survives 3 losses but only needs 2 to
   recover (weaker). Pick ``k`` from your security policy, then ``n`` from
   how much redundancy you want on top.

Typical configurations:

.. list-table::
   :header-rows: 1
   :widths: 26 8 8 58

   * - Use case
     - ``n``
     - ``k``
     - Notes
   * - Personal / small treasury
     - 3
     - 2
     - Three sites, any two recover. Survives one loss.
   * - Small team / four-eyes
     - 5
     - 3
     - Majority required; survives two losses.
   * - Enterprise
     - 7
     - 4
     - Robust to multiple losses and absentees.
   * - Maximum distribution
     - 12
     - 7
     - The system's hard limits.

**Constraints:** ``n`` ∈ [2, 12], ``k`` ∈ [2, 7], and ``k ≤ n``.

.. note::

   ``n`` is also capped by the **number of storage cards you hold**: a set's
   card count is the maximum ``n``. You may use fewer (leaving spares unused),
   but never more. The k-of-n is your choice at the ceremony — it is not marked
   at the factory. See :ref:`ceremony:labelling`.

.. warning::

   ``k = 1`` is **not** supported (and would be insecure — a single card
   would reveal the secret). The minimum threshold is ``2``.

Seed size
---------

The seed size is given in **bytes** with ``-s``. Choose it to match the
secret you are protecting.

.. list-table::
   :header-rows: 1
   :widths: 12 12 76

   * - Size
     - Bits
     - Typical use
   * - ``16``
     - 128
     - A 128-bit AES key; BIP-39 minimum entropy.
   * - ``32``
     - 256
     - **Most common.** secp256k1 / NIST P-256 private key,
       BIP-32/39 seed material, 256-bit symmetric key.
   * - ``48``
     - 384
     - NIST P-384 private key.
   * - ``64``
     - 512
     - BIP-39 maximum, HMAC-SHA-512 key.
   * - ``66``
     - 521
     - NIST P-521 private key.
   * - ``128``
     - 1024
     - Very large secrets.

.. note::

   For a Bitcoin treasury key, the common choice is ``-s 32`` (256-bit). For
   an HSM AES wrapping key, choose the size of that key (``16`` or ``32``).

Seed type
---------

The seed type (``-t``) tells the orchestrator how to generate or interpret
the secret:

.. option:: -t f

   **Fully random** bytes with no structure. The most flexible choice — use
   it for AES keys, HMAC keys, or any opaque secret.
   Valid sizes: ``16, 32, 48, 64, 128``.

.. option:: -t r

   A **NIST EC "r1" private key** (a valid scalar for P-256 / P-384 / P-521).
   Use when the secret must be a valid EC private key on those curves.
   Valid sizes: ``32, 48, 66``.

.. option:: -t k

   A **secp256k1 private key** — the Bitcoin / Ethereum curve.
   Valid size: ``32``.

.. tip::

   If you are protecting a **Bitcoin** key, use ``-t k -s 32``. If you just
   need a random secret (e.g. an HSM wrapping key), use ``-t f``.

.. seealso::

   - :doc:`ceremony` — where these parameters are supplied.
   - :doc:`security_model` — how the quorum maps to your threat model.
