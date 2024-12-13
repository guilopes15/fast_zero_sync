from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import Todo, User
from tests.conftest import TodoFactory


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(username='gui', email='test@test.com', password='123')
        session.add(user)
        session.commit()
        # session.refresh(user)
        result = session.scalar(
            select(User).where(User.email == 'test@test.com')
        )
        assert asdict(result) == {
            'id': 1,
            'username': 'gui',
            'password': '123',
            'email': 'test@test.com',
            'created_at': time['created_at_time'],
            'updated_at': time['updated_at_time'],
        }


def teste_create_todo(session, token, user, mock_db_time):
    with mock_db_time(model=Todo) as time:
        todo = TodoFactory(user_id=user.id)
        session.add(todo)
        session.commit()

        new_todo = session.scalar(select(Todo).where(Todo.user_id == user.id))

    assert asdict(new_todo) == {
        'id': 1,
        'title': todo.title,
        'description': todo.description,
        'state': todo.state,
        'created_at': time['created_at_time'],
        'updated_at': time['updated_at_time'],
        'user_id': 1,
    }
