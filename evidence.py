"""Locate model quotations in the exact caller-supplied context."""

from __future__ import annotations

import hashlib
import re

from contracts import EvidenceVerification


def source_hash(context: str) -> str:
    return hashlib.sha256(context.encode("utf-8")).hexdigest()


class EvidenceVerifier:
    def verify(self, evidence: str, context: str) -> EvidenceVerification:
        digest = source_hash(context)
        if not evidence or not evidence.strip():
            return EvidenceVerification(evidence, "not_found", None, None, digest)
        exact = list(re.finditer(re.escape(evidence), context))
        if len(exact) > 1:
            return EvidenceVerification(evidence, "ambiguous", None, None, digest)
        if len(exact) == 1:
            match = exact[0]
            return EvidenceVerification(evidence, "exact", match.start(), match.end(), digest)
        tokens = evidence.split()
        if not tokens:
            return EvidenceVerification(evidence, "not_found", None, None, digest)
        pattern = r"\s+".join(re.escape(token) for token in tokens)
        normalized = list(re.finditer(pattern, context))
        if len(normalized) > 1:
            return EvidenceVerification(evidence, "ambiguous", None, None, digest)
        if len(normalized) == 1:
            match = normalized[0]
            return EvidenceVerification(evidence, "normalized", match.start(), match.end(), digest)
        return EvidenceVerification(evidence, "not_found", None, None, digest)
