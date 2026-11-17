import pytest


@pytest.mark.asyncio
async def test_get_all_payments(client, seeded_payments) -> None:
    response = await client.get("/payments/")

    assert response.status_code == 200
    assert len(response.json()) == len(seeded_payments)


@pytest.mark.asyncio
async def test_get_payment_by_id(client, seeded_payments) -> None:
    payment = seeded_payments[0]

    response = await client.get(f"/payments/{payment.id}")

    assert response.status_code == 200
    assert response.json()["id"] == payment.id
    assert response.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_get_payments_by_user_id(client, seeded_payments) -> None:
    payment = seeded_payments[0]

    response = await client.get(f"/payments/users/{payment.user_id}")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_payment_by_order_id(client, seeded_payments) -> None:
    payment = seeded_payments[0]

    response = await client.get(f"/payments/orders/{payment.order_id}")

    assert response.status_code == 200
    assert response.json()["order_id"] == payment.order_id


@pytest.mark.asyncio
async def test_get_payment_not_found_returns_404(client) -> None:
    response = await client.get("/payments/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_payment_returns_pending(client) -> None:
    response = await client.post(
        "/payments/create",
        json={"order_id": 1, "user_id": 1, "amount": 100.0},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_pay_payment_sets_paid(client, seeded_payments) -> None:
    payment = seeded_payments[0]

    response = await client.post(f"/payments/{payment.id}/pay")

    assert response.status_code == 200
    assert response.json()["status"] == "paid"


@pytest.mark.asyncio
async def test_pay_paid_payment_returns_409(client, seeded_payments) -> None:
    payment = seeded_payments[0]
    await client.post(f"/payments/{payment.id}/pay")

    response = await client.post(f"/payments/{payment.id}/pay")

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_fail_payment_sets_failed(client, seeded_payments) -> None:
    payment = seeded_payments[0]

    response = await client.post(f"/payments/{payment.id}/fail")

    assert response.status_code == 200
    assert response.json()["status"] == "failed"


@pytest.mark.asyncio
async def test_cancel_payment_sets_cancelled(client, seeded_payments) -> None:
    payment = seeded_payments[0]

    response = await client.post(f"/payments/{payment.id}/cancel")

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancel_paid_payment_returns_409(client, seeded_payments) -> None:
    payment = seeded_payments[0]
    await client.post(f"/payments/{payment.id}/pay")

    response = await client.post(f"/payments/{payment.id}/cancel")

    assert response.status_code == 409
