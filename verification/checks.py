#!/usr/bin/env python3
"""Finite matrix diagnostics for the trace estimator; these are not proofs.

Run from the repository root:
    python verification/checks.py --output verification/results.json
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import block_diag, schur

SEED = 20261031
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
H = (X + Z) / np.sqrt(2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def paulis(n: int) -> list[np.ndarray]:
    result = []
    for word in itertools.product((I2, X, Y, Z), repeat=n):
        matrix = np.ones((1, 1), dtype=complex)
        for factor in word:
            matrix = np.kron(matrix, factor)
        result.append(matrix)
    return result


def random_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(matrix)
    return q @ np.diag(np.diag(r) / np.abs(np.diag(r)))


def twirl(a: np.ndarray, generators: tuple | list) -> np.ndarray:
    b = a.copy()
    for g in generators:
        b = (b + g.conj().T @ b @ g) / 2
    return b


def variance(a: np.ndarray) -> float:
    d = len(a)
    return float(np.linalg.norm(a - np.trace(a) * np.eye(d) / d, "fro") ** 2 / d)


def ensemble_checks(rng: np.random.Generator) -> list[dict]:
    reports = []
    for n, s in ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2)):
        d = 2 ** n
        z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        a = (z + z.conj().T) / 2
        a /= np.linalg.norm(a, 2)
        observed = np.mean([variance(twirl(a, gs))
                            for gs in itertools.product(paulis(n), repeat=s)])
        predicted = variance(a) / 2 ** s
        error = abs(observed - predicted)
        require(error < 1e-12, "Exact ensemble identity failed")
        reports.append({"n": n, "s": s, "seeds_enumerated": 4 ** (n * s),
                        "observed_variance": float(observed),
                        "predicted_variance": predicted, "absolute_error": float(error)})
    return reports


def walk_check(u: np.ndarray, generators: list[np.ndarray], name: str) -> dict:
    d, s = len(u), len(generators)
    m = 2 ** s
    a = (u + u.conj().T) / 2
    products = []
    for label in range(m):
        p = np.eye(d, dtype=complex)
        for j, g in enumerate(generators):
            if (label >> j) & 1:
                p = g @ p
        products.append(p)
    wa = np.block([[np.zeros((d, d)), u.conj().T], [u, np.zeros((d, d))]])
    prepare = H.copy()
    for _ in range(s):
        prepare = np.kron(H, prepare)
    prepare = np.kron(prepare, np.eye(d))
    select = block_diag(*[np.kron(I2, p) for p in products])
    w = prepare.conj().T @ select.conj().T @ np.kron(np.eye(m), wa) @ select @ prepare
    b = sum(p.conj().T @ a @ p for p in products) / m
    dimension = len(w)
    projector = np.zeros((dimension, dimension))
    projector[:d, :d] = np.eye(d)
    q = (2 * projector - np.eye(dimension)) @ w
    triangular, vectors = schur(q, output="complex")
    eigenvalues = np.diag(triangular)
    weights = np.sum(np.abs(vectors[:d, :]) ** 2, axis=0) / d
    cosines = eigenvalues.real
    tau = float(np.trace(a).real / d)
    residuals = {
        "signal_block": float(np.linalg.norm(w[:d, :d] - b)),
        "hermitian_involution": float(np.linalg.norm(w @ w - np.eye(dimension))),
        "walk_unitarity": float(np.linalg.norm(q.conj().T @ q - np.eye(dimension))),
        "schur_off_diagonal": float(np.linalg.norm(triangular - np.diag(eigenvalues))),
        "weight_normalization": float(abs(np.sum(weights) - 1)),
        "trace_mean": float(abs(np.dot(weights, cosines) - tau)),
        "spectral_variance": float(abs(np.dot(weights, (cosines - tau) ** 2) - variance(b))),
    }
    for label, error in residuals.items():
        require(error < 1e-10, name + ": " + label + " failed")
    # A branchwise phase change of SELECT cancels against its true adjoint.
    phases = np.diag(np.exp(1j * np.arange(m)))
    rephased = np.kron(phases, np.eye(2 * d)) @ select
    w_rephased = (prepare.conj().T @ rephased.conj().T @ np.kron(np.eye(m), wa)
                  @ rephased @ prepare)
    phase_residual = float(np.linalg.norm(w_rephased - w))
    require(phase_residual < 1e-10, "Matching-adjoint phase invariance failed")
    residuals["branch_phase_invariance"] = phase_residual
    return {"case": name, "target_dimension": d, "generators": s,
            "full_walk_dimension": dimension, "residuals": residuals}


def qpe_checks() -> dict:
    m = 128
    phases = np.linspace(0, 1, 4097, endpoint=False)
    min_two_bin_mass = 1.0
    max_normalization_error = 0.0
    for phase in phases:
        distance = (phase - np.arange(m) / m + 0.5) % 1 - 0.5
        probabilities = (np.sinc(m * distance) / np.sinc(distance)) ** 2
        max_normalization_error = max(max_normalization_error, abs(probabilities.sum() - 1))
        mass = float(probabilities[np.abs(distance) <= 1 / m + 1e-14].sum())
        min_two_bin_mass = min(min_two_bin_mass, mass)
    require(max_normalization_error < 1e-11, "QPE probability normalization failed")
    require(min_two_bin_mass >= 8 / np.pi ** 2 - 1e-11, "QPE two-bin bound failed")
    return {"clock_dimension": m, "phases_checked": len(phases),
            "minimum_two_bin_mass": min_two_bin_mass,
            "analytic_lower_bound": float(8 / np.pi ** 2),
            "maximum_normalization_error": float(max_normalization_error)}


def amplification_checks(rng: np.random.Generator) -> list[dict]:
    reports = []
    w = 4
    d = 2 ** w
    v = random_unitary(d, rng)
    q = np.diag([1] * (d // 2) + [0] * (d // 2))
    z = 2 * q - np.eye(d)
    for k in (1, 2, 3):
        dirty_dimension = 2 ** (w - k)
        p0 = np.diag([1] * dirty_dimension + [0] * (d - dirty_dimension))
        acceptance = float(np.trace(q @ v @ p0 @ v.conj().T).real / dirty_dimension)
        # Two independently written signal representations of the same acceptance.
        reflection_product = z @ v @ (2 * p0 - np.eye(d)) @ v.conj().T
        trace_value = np.trace(reflection_product) / d
        predicted = 2 ** (1 - k) * (2 * acceptance - 1)
        h = v.conj().T @ z @ v
        direct_trace = np.trace(h[:dirty_dimension, :dirty_dimension]) / dirty_dimension
        error = float(max(abs(trace_value - predicted), abs(direct_trace - (2 * acceptance - 1))))
        require(error < 1e-12, "Acceptance-to-trace representation failed")
        reports.append({"total_qubits": w, "initial_clean_qubits": k,
                        "acceptance": acceptance, "maximum_identity_error": error})
    return reports


def boundary_checks() -> dict:
    # The guarantee is over seeds: a commuting seed can be entirely uninformative.
    bad_seed_b = twirl(Z, [Z] * 11)
    require(np.linalg.norm(bad_seed_b - Z) == 0, "Bad-seed boundary changed")
    # Uncontrolled channel accuracy cannot specify a normalized unitary trace.
    u = I2
    v = -I2
    channel_difference = np.linalg.norm(np.kron(u, u.conj()) - np.kron(v, v.conj()))
    controlled_difference = np.linalg.norm(block_diag(I2, u) - block_diag(I2, v), 2)
    require(channel_difference == 0 and controlled_difference == 2, "Control-phase boundary failed")
    return {"bad_seed_eigenvalues": [-1.0, 1.0], "bad_seed_trace": 0.0,
            "uncontrolled_channel_difference": float(channel_difference),
            "controlled_unitary_difference": float(controlled_difference)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("verification/results.json"))
    args = parser.parse_args()
    rng = np.random.default_rng(SEED)
    ensemble = ensemble_checks(rng)
    generators = [paulis(2)[j] for j in (1, 6, 11)]
    cases = [("generic_unitary", random_unitary(4, rng)),
             ("positive_endpoint", np.eye(4)),
             ("negative_endpoint", -np.eye(4)),
             ("scalar_complex_phase", np.exp(0.37j) * np.eye(4))]
    report = {
        "status": "pass", "seed": SEED,
        "scope": "Finite numerical diagnostics; analytical proofs and literature novelty are separate.",
        "environment": {"numpy": np.__version__, "scipy": scipy.__version__},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "ensemble_identity": ensemble,
        "coherent_walk": [walk_check(u, generators, name) for name, u in cases],
        "phase_estimation": qpe_checks(),
        "acceptance_reductions": amplification_checks(rng),
        "boundaries": boundary_checks(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "report": str(args.output),
                      "maximum_ensemble_error": max(x["absolute_error"] for x in ensemble),
                      "walk_cases": len(cases),
                      "minimum_qpe_two_bin_mass": report["phase_estimation"]["minimum_two_bin_mass"]}))


if __name__ == "__main__":
    main()
