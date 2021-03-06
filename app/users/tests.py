from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase

from users.exceptions import RelationNotExist, DuplicateRelationException

User = get_user_model()
# Create your tests here.
class RelationTestCase(TransactionTestCase):
    def create_dummy_user(self, num):
        return [User.objects.create_user(username=f'u{x}') for x in range(num)]

    def test_follow(self):
        """
        특정 유저가 다른 유저를 follow 했을 경우, 정상 작동하는지 확인
        :return:
        """
        # 임의의 유저 2명 생성 (u1,u2)
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        # u1이 u2를 follow하도록 함

        relation = u1.relations_by_from_user.create(to_user=u2, relation_type='f')

        # u1의 following에 u2가 포함되어 있는지 확인

        # if u1.following_relations.exists():
        #     print('True')
        # else:
        #     print('False')
        # self.assertIn(u2, u1.following)
        #
        # # u1의 following_relations에서 to_user가 u2의 Relation이 존재하는지 확인
        # u1.following.filter(pk=u2.pk).exists()
        #
        #
        # # relation이 u1.following_relations에 포힘되어있는지
        # self.assertIn(relation, u1.following_relations)

        # relation = u1.follow(u2)

    def test_follow_only_once(self):
        u1 = User.objects.create_user(username='u1')
        u2 = User.objects.create_user(username='u2')

        # u2로의 follow를 두번 실행한다.
        u1.follow(u2)

        with self.assertRaises(IndentationError):
            u1.follow(u2)

        # u1의 following이 하나인지 확인
        self.assertEqual(u1.following.count(), 1)

    def test_unfollow_if_follow_exist(self):
        u1, u2 = self.create_dummy_user(2)

        #u1이 u2를 follow후 unfollow실행
        u1.follow(u2)
        u1.unfollow(u2)

        # u1의 following에 u2가 없어야함.
        self.assertNotIn(u2, u1.following)

    def test_unfollow_fail_only_follow_exist(self):
        u1, u2 = self.create_dummy_user(2)

        with self.assertRaises(RelationNotExist):
            u1.unfollow(u2)

    def test_unfollow_fail_duplicate(self):
        u1, u2 = self.create_dummy_user(2)

        with self.assertRaises(DuplicateRelationException):
            u1.unfollow(u2)
            u1.unfollow(u2)