from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='gui', email='test@test.com', password='123')
    session.add(user)
    session.commit()
    # session.refresh(user)
    result = session.scalar(select(User).where(User.email == 'test@test.com'))
    assert result.id == 1
