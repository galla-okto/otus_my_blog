from main import get_posts_by_id_user


class TestMain:
    def test_get_posts_by_id_user(self, user):
        res = get_posts_by_id_user(user)
        for row in res:
            assert row.user_id == user
