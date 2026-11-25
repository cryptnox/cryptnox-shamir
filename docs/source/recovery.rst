Recovery
========

**Recovery** reconstructs the seed from ``k`` storage cards — for example
after the production HSM is lost or destroyed — and re-wraps it for a new HSM.

This page uses a **2-of-3** deployment (any two of the three cards) **purely
as a worked example** — the procedure is identical for any supported threshold
(``k`` from 2 to 7, ``n`` from 2 to 12).

.. note::

   **2-of-3 is just an example.** Recover with whatever ``k`` your deployment
   was created with.

.. figure:: _static/recovery_flow.*
   :alt: Recovery steps: collect k cards, reconstruct seed, wrap to new HSM
   :align: center
   :width: 100%

   Recovery at a glance — *k* storage cards are collected, the seed is
   reconstructed on the orchestrator, then re-wrapped for the new HSM.

Before you begin
----------------

Prepare:

- **1 orchestrator card** (any orchestrator in state ``0x00``; it need not be
  the one used for the ceremony).
- **``k`` storage cards** holding valid shares, with their PINs known.
- The **RSA public key of the new HSM** where the seed will be restored
  (e.g. ``new_hsm_pubkey.pem``).
- Your record of **which physical card holds which share index** (see
  :ref:`ceremony:labelling`).

.. note::

   **Card order.** On current firmware each storage card reports its **own** share
   index, so recovery reconstructs correctly **whatever order you insert the cards**
   in — the tool reads the true index from each card. Insertion order only matters on
   **older cards** that do not expose their index, where the tool falls back to the
   order of insertion (first inserted = share #1, …) and a wrong order silently yields
   the **wrong secret**. Either way, **verify the checksum** (below) before trusting
   the result — it is the definitive check.

Running recovery
----------------

.. code-block:: bash

   shamir-cli workflow full-recovery \
     -k 2 \
     --rsa-key-file new_hsm_pubkey.pem \
     --output-file recovered_seed.bin \
     --pin 0000

Options:

.. list-table::
   :header-rows: 1
   :widths: 26 74

   * - Option
     - Meaning
   * - ``-k, --threshold``
     - Number of shares to collect (must equal the ceremony's ``k``).
   * - ``--rsa-key-file``
     - RSA public key of the **new** HSM to wrap the recovered seed for.
   * - ``--output-file``
     - Where to write the wrapped recovered seed.
   * - ``--pin``
     - Storage card PIN (default ``0000``).

The tool prompts for the orchestrator and then each storage card:

.. code-block:: text

   Insert Orchestrator card and press Enter...
   Insert Storage card #1 and press Enter...
   Swap back to Orchestrator card and press Enter...
   Insert Storage card #2 and press Enter...
   Swap back to Orchestrator card and press Enter...
   Recovery checksum: 33 F4 A2 59 31 57 9D 19
   Wrapped seed saved to recovered_seed.bin

How it works
------------

1. The orchestrator is reset and enters **Recovery** mode.
2. The new HSM RSA wrapping key is loaded; the orchestrator generates an
   ephemeral encryption key.
3. For each of the ``k`` cards:

   - You verify the PIN.
   - The storage card **re-encrypts** its share to the orchestrator's key and
     hands it over. The host only relays opaque ciphertext.
   - The orchestrator decrypts the share internally.

4. The orchestrator reconstructs the seed (Lagrange interpolation, performed
   on-card) and returns a **checksum**.
5. The orchestrator exports the **RSA-wrapped** recovered seed to the output
   file.

Verifying the result
--------------------

**Always compare the** ``Recovery checksum`` **against the seed checksum you
recorded at the ceremony.**

- **Match** → the correct seed was reconstructed. Import
  ``recovered_seed.bin`` into the new HSM, then destroy the file.
- **Mismatch** → you collected the wrong cards, or inserted them in the wrong
  order. Do **not** import the result. Re-run, inserting the correctly
  labelled cards in share-index order.

Operational notes
-----------------

- **Export counter.** Every real share read during a recovery increments a
  counter inside the storage card. Inspect it for audit with
  ``shamir-cli storage read-counter``. An unexpected increase means a share
  was read outside a sanctioned recovery.
- **PIN lockout.** Three consecutive wrong PINs lock the card. Guard the PINs
  and the lockout budget.
- **The PC never sees a plaintext share.** Shares move card-to-card over an
  encrypted channel; the host only relays ciphertext.

.. note::

   Recovery only *reads* the storage cards — it does **not** consume or alter
   the shares. You can recover as many times as needed (each read increments
   the audit counter).

.. seealso::

   - :doc:`ceremony` — how the shares and labels were created.
   - :doc:`backup_test` — verify shares **without** exporting the seed.
   - :ref:`troubleshooting-wrong-pin` — recovering from PIN errors.
   - :doc:`security_model` — what the host can and cannot see.
