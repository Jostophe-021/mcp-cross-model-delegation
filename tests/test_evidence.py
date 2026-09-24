from evidence import EvidenceVerifier, source_hash


def test_exact_span_and_hash():
    result = EvidenceVerifier().verify("12 tickets", "Monday: 12 tickets.")
    assert (result.verification_status, result.start, result.end) == ("exact", 8, 18)
    assert result.source_sha256 == source_hash("Monday: 12 tickets.")


def test_normalized_ambiguous_and_missing():
    verifier = EvidenceVerifier()
    assert verifier.verify("red blue", "red\n  blue").verification_status == "normalized"
    assert verifier.verify("red", "red and red").verification_status == "ambiguous"
    assert verifier.verify("green", "red").verification_status == "not_found"
    assert verifier.verify("", "red").verification_status == "not_found"
