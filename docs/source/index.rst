:description: Operating documentation for the Cryptnox Shamir card system — split a master secret across smart cards with Shamir Secret Sharing, run the key ceremony, test backups and recover with a k-of-n quorum.

.. meta::
   :description: Operating documentation for the Cryptnox Shamir card system — split a master secret across smart cards with Shamir Secret Sharing, run the key ceremony, test backups and recover with a k-of-n quorum.

===============
Cryptnox Shamir
===============

.. only:: html

   `Download this documentation as PDF <https://docs.cryptnox.com/cryptnox-shamir/cryptnox-shamir.pdf>`__

   *Cryptnox Shamir* splits a single master secret — a Bitcoin treasury key, an HSM
   wrapping key, a recovery seed — across ``n`` tamper-resistant smart cards, of which
   any ``k`` are enough to reconstruct it. No single card, and no single person, ever
   holds the secret. It is built for institutional custody: corporate Bitcoin
   treasuries, funds, exchanges, and any organisation that needs verifiable,
   quorum-based control over a high-value cryptographic secret.


   Getting started
   ===============

   .. raw:: html

      <div class="card-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="5" width="20" height="14" rx="2"/>
          <line x1="2" y1="10" x2="22" y2="10"/>
          <line x1="6" y1="15" x2="10" y2="15"/>
        </svg>
      </div>

   What the system is, how Shamir Secret Sharing works on the cards, and how to set up the tool.

   * **Overview** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/overview.html>`__] — who the system is for and why the sensitive operations run on the cards
   * **Concepts** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/concepts.html>`__] — shares, threshold, the orchestrator, and how the seed is wrapped for an HSM
   * **Cards** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/hardware.html>`__] — the Orchestrator, Storage and Admin cards and what to write on each
   * **Installation** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/installation.html>`__] — requirements, installing ``shamir-cli`` and checking the reader

   Operating procedures
   ====================

   .. raw:: html

      <div class="card-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
      </div>

   The custody lifecycle step by step: the key ceremony, recovery, periodic backup tests and governance.

   * **Cheat sheet** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/cheatsheet.html>`__] — the essential commands on one page
   * **The Ceremony** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/ceremony.html>`__] — generate or import the secret, split it onto the cards and wrap it for the HSM
   * **Recovery** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/recovery.html>`__] — reconstruct the secret from any ``k`` storage cards
   * **Backup Test** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/backup_test.html>`__] — prove the cards still recover the secret without exposing it
   * **Choosing Parameters** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/parameters.html>`__] — picking ``k``, ``n``, seed size and seed type
   * **Custody Governance & Checklists** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/governance.html>`__] — roles, the lifecycle and the checklists for each event
   * **Printable Checklist** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/printable_checklist.html>`__] — a condensed sign-off version of the custody controls, to print and keep with the custody log

   Reference
   =========

   .. raw:: html

      <div class="card-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        </svg>
      </div>

   The security model, every command and option, and what to do when something goes wrong.

   * **Security Model** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/security_model.html>`__] — what each component protects against, and the operator's responsibilities
   * **Command Reference** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/cli_reference.html>`__] — every ``shamir-cli`` command and option
   * **Troubleshooting** [`HTML <https://docs.cryptnox.com/cryptnox-shamir/troubleshooting.html>`__] — common errors and status codes, and how to resolve them

.. only:: latex

   This system lets an organisation split a single master secret — a Bitcoin
   treasury key, an HSM wrapping key, a recovery seed — into ``n``
   tamper-resistant smart cards, of which any ``k`` are sufficient to
   reconstruct it. No single card, and no single person, ever holds the secret.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Getting started

   overview
   concepts
   hardware
   installation

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Operating procedures

   cheatsheet
   ceremony
   recovery
   backup_test
   parameters
   governance
   printable_checklist

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Reference

   security_model
   cli_reference
   troubleshooting

.. toctree::
   :hidden:
   :maxdepth: 1
   :caption: About

   license

.. only:: html

   Other resources
   ===============

   * `Cryptnox Product Documentation <https://docs.cryptnox.com/>`_
   * `Cryptnox Website <https://www.cryptnox.com>`_
   * `Cryptnox on GitHub <https://github.com/cryptnox>`_
   * `Contact Cryptnox <https://cryptnox.com/contact/>`_
