Backup Test
===========

A **backup test** confirms that your shares still reconstruct the seed —
**without ever exporting the seed**. It is the safest routine to run on a
schedule (for example annually, or whenever cards are moved between sites) to
prove that your custody backup is still healthy.

.. note::

   This is the recommended periodic health check. It needs no HSM key, does
   **not** export the secret, and does **not** consume the storage cards'
   read budget.

What you need
-------------

- **1 orchestrator card** in state ``0x00``.
- **``k`` storage cards** with valid shares.

Running a backup test
---------------------

.. code-block:: bash

   shamir-cli workflow backup-test -k 2 --pin 0000

.. option:: -k, --threshold

   Number of shares to test (must equal the deployment's threshold).

.. option:: --pin

   Storage card PIN (default ``0000``).

How it works
------------

1. The orchestrator is reset and enters **Test** mode (``0x30``).
2. For each of the ``k`` cards, the share is read back in a **test-only read**
   that bumps the card's dedicated **test counter** — never the export
   (recovery) counter (see :ref:`two-counters`).
3. The orchestrator reconstructs the seed internally and computes its
   checksum.
4. It reports **PASS** or **FAIL**. The seed is **never** exported.

Why a dedicated test mode
-------------------------

Compared to a recovery, the backup test is deliberately safer for routine
use:

- **No PIN spend risk on the audit counter** — the test read does **not**
  increment the recovery export counter.
- **The seed cannot leave the card** — Test mode has no export capability, so
  even a compromised host cannot exfiltrate the secret during a check.
- **Non-destructive** — it only reads; shares are untouched.

.. _two-counters:

The two counters
----------------

Every storage card keeps **two independent, monotonic counters** (each only ever
goes up, never resets except on a full card reset):

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Counter
     - Meaning
   * - **Export counter**
     - Bumped on every **real recovery** read, when the share is re-encrypted out
       for reconstruction and the seed is exported. This is the audit metric for
       genuine exports — a backup test **never** moves it.
   * - **Test counter**
     - Bumped on every **backup test** read. The share *is* re-encrypted during a
       test, so it is worth recording; the test counter leaves an append-only
       trace of tests **without polluting the export counter**.

Read either at any time:

.. code-block:: bash

   shamir-cli storage read-counter        # export counter (real recoveries)
   shamir-cli storage read-test-counter   # backup-test counter

So you can run a backup test as often as you like: the **export counter stays
put**, while the **test counter** grows — a clean separation between "this card
has been recovered N times" and "this card has been test-verified M times".

Interpreting the result
-----------------------

- **PASS** — the tested shares reconstruct correctly. Your backup is healthy.
- **FAIL** — the shares did not reconstruct. Investigate immediately: a card
  may be damaged, or you may have collected cards from different ceremonies.

.. tip::

   Rotate which ``k`` cards you test over successive checks, so that every
   card is exercised over time — not just the same ``k`` each year.

.. _single-card-verify:

Checking a single card
----------------------

The backup test above reconstructs the seed and therefore needs ``k`` cards
together. Sometimes you only want to confirm that **one** card is healthy — for
example when a single card comes back from a remote site, or before you re-seal
it in its safe. For that, a storage card can verify **itself**:

.. code-block:: bash

   shamir-cli storage pedersen-verify

The card proves, on its own, that the share it holds is a genuine part of this
set's split — **without reconstructing the seed** and **without gathering the
other cards**. It reports the card's **share number** and a **set fingerprint**
(shown as ``PID``) that identifies which ceremony the card belongs to.

.. note::

   A single card is enough: this is a per-card cryptographic check, not a
   reconstruction. It exports nothing, needs no HSM key, and does **not** move
   either counter.

Checking a whole set at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With one card per reader you can verify a whole set in a single command, and
confirm the cards are mutually consistent:

.. code-block:: bash

   shamir-cli storage pedersen-verify --readers "<reader-1>,<reader-2>,<reader-3>"

The result is a per-card table followed by an overall verdict:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Verdict
     - Meaning
   * - **BATCH OK**
     - Every card verified, all report the **same** set fingerprint, and each
       carries a **distinct** share number. The set is coherent.
   * - **MISMATCH**
     - A card reports a **different** fingerprint — it belongs to another
       ceremony. Check you have not mixed cards from different sets.
   * - **FAILED**
     - A card failed its check, or **two cards carry the same share number**
       (a possible copy). Investigate immediately.

.. tip::

   Run a single-card check whenever a card changes hands or location — it is
   quick, needs only that one card, and surfaces a mixed-up or duplicated card
   long before a recovery would.

.. seealso::

   - :doc:`recovery` — the full restore (exports the seed to a new HSM).
   - :doc:`ceremony` — where the shares were created.
