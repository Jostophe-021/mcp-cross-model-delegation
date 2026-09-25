"""Verify a synthetic quotation locally."""

from evidence import EvidenceVerifier

context = "Monday: 12 tickets."
verification = EvidenceVerifier().verify("12 tickets", context)
print(verification)
