from http import HTTPStatus


# import colocado dentro da função para que a importação seja feita só depois do Freezegun estar setado  # noqa: E501
# issue: https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
def test_list_todos__fields_shoul_be_equal(
    session, client, user, token, mock_db_time
):
    from tests.factories import TodoModelFactory  # noqa: PLC0415

    todo = TodoModelFactory.create(
        user_id=user.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    expected_todo = {
        'created_at': mock_db_time,
        'updated_at': mock_db_time,
        'description': todo.description,
        'id': todo.id,
        'state': todo.state.value,
        'title': todo.title,
    }
    assert response.json()['todos'] == [expected_todo]
