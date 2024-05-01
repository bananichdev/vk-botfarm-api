def check_response_status_code(
    expect_status_code: list[int] | int, response_status_code: int, response_body: dict | None
):
    if type(expect_status_code) is int:
        expect_status_code = [expect_status_code]

    if response_status_code not in expect_status_code:
        response_body_message = "Response body is empty"
        if type(response_body) is dict:
            response_body_message = response_body["detail"]
        raise AssertionError(f"[{response_status_code}] {response_body_message}")

    assert response_status_code in expect_status_code
