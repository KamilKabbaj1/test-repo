"""Tests for the hospital package (run with `pytest -v`)."""

import pytest

from hospital import (
    Cash,
    Check,
    CreditCard,
    Organizer,
    PaymentMethod,
    PaymentStatus,
    ProblemStatus,
    User,
)


# A fixture builds the same starting point for every test that asks for it.
@pytest.fixture
def platform():
    organizer = Organizer("O-001", "Olga", "admin")
    patient = organizer.register_patient("Paul", "secret", "paul@mail.com")
    doctor = organizer.register_doctor("Dr. House", "vicodin", "diagnostics")
    return organizer, patient, doctor


def deliver_prescription(organizer, patient, doctor, fee=50.0):
    """Helper: run steps 1 to 4 and return the delivered prescription."""
    problem = patient.submit_problem("headache for 3 days")
    organizer.assign(problem, doctor)
    prescription = doctor.prescribe(problem, "paracetamol 1g, 3 times a day", fee)
    organizer.send_prescription(prescription)
    return prescription


# ---------------------------------------------------------------- users
def test_user_is_abstract():
    with pytest.raises(TypeError):
        User("U-1", "nobody", "pwd")


def test_login_and_logout(platform):
    _, patient, _ = platform
    assert patient.login("wrong") is False
    assert patient.login("secret") is True
    assert patient.logged_in
    patient.logout()
    assert not patient.logged_in


def test_organizer_issues_unique_ids(platform):
    organizer, patient, _ = platform
    other = Organizer("O-002", "Otto", "admin").register_patient("Lea", "pwd", "lea@mail.com")
    assert patient.id.startswith("P-")
    assert other.id != patient.id
    assert patient.role == "patient"


# ---------------------------------------------------------------- workflow
def test_full_workflow(platform):
    organizer, patient, doctor = platform
    problem = patient.submit_problem("headache for 3 days")
    assert problem.status is ProblemStatus.PENDING

    organizer.assign(problem, doctor)
    assert problem.status is ProblemStatus.IN_REVIEW

    prescription = doctor.prescribe(problem, "paracetamol", 50.0)
    organizer.send_prescription(prescription)
    assert problem.status is ProblemStatus.RESOLVED
    assert patient.prescription_history == [prescription]

    payment = patient.pay(prescription, CreditCard("4970123412341234"))
    assert payment.status is PaymentStatus.RECEIVED
    assert payment.amount == 50.0
    assert prescription.is_paid

    organizer.forward_payment(payment)
    assert payment.status is PaymentStatus.FORWARDED
    assert doctor.earnings == 50.0


def test_status_cannot_go_backwards(platform):
    organizer, patient, doctor = platform
    prescription = deliver_prescription(organizer, patient, doctor)
    with pytest.raises(ValueError):
        organizer.assign(prescription.problem, doctor)  # already resolved


def test_only_assigned_doctor_can_prescribe(platform):
    organizer, patient, doctor = platform
    other_doctor = organizer.register_doctor("Dr. Who", "tardis", "general")
    problem = patient.submit_problem("cough")
    organizer.assign(problem, doctor)
    with pytest.raises(ValueError):
        other_doctor.prescribe(problem, "syrup", 20.0)


# ---------------------------------------------------------------- payments
@pytest.mark.parametrize(
    ("method", "expected_receipt"),
    [
        (Cash(), "50.00 EUR paid in cash"),
        (Check("0042"), "50.00 EUR paid by check n°0042"),
        (CreditCard("4970123412341234"), "50.00 EUR paid by credit card ****1234"),
    ],
)
def test_payment_methods_are_polymorphic(platform, method, expected_receipt):
    organizer, patient, doctor = platform
    prescription = deliver_prescription(organizer, patient, doctor)
    assert isinstance(method, PaymentMethod)
    assert patient.pay(prescription, method).receipt == expected_receipt


def test_cannot_pay_twice(platform):
    organizer, patient, doctor = platform
    prescription = deliver_prescription(organizer, patient, doctor)
    patient.pay(prescription, Cash())
    with pytest.raises(ValueError):
        patient.pay(prescription, Cash())


def test_cannot_pay_undelivered_prescription(platform):
    organizer, patient, doctor = platform
    problem = patient.submit_problem("back pain")
    organizer.assign(problem, doctor)
    prescription = doctor.prescribe(problem, "rest", 30.0)  # not sent yet
    with pytest.raises(ValueError):
        patient.pay(prescription, Cash())


def test_cannot_forward_twice(platform):
    organizer, patient, doctor = platform
    payment = patient.pay(deliver_prescription(organizer, patient, doctor), Cash())
    organizer.forward_payment(payment)
    with pytest.raises(ValueError):
        organizer.forward_payment(payment)
    assert doctor.earnings == 50.0


def test_card_number_is_not_stored_in_full():
    card = CreditCard("4970123412341234")
    assert "4970123412341234" not in str(vars(card))
