from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack


class Test(TestCase):
    def test_snack_lists(self):
        url=reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'snack_list.html')

    def setUp(self):
        self.user= get_user_model().objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )
        self.snack=Snack.objects.create(
            title='Test',
            purchaser=self.user,
            description='test',
            img_url='test.png',
        )

    def test_str_method(self):
        self.assertEqual(str(self.snack), 'Test')

    def test_snack_details(self):
        url=reverse('snack_detail',args=[self.snack.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'snack_detail.html')
    
    def test_snack_create(self):
        data={
            'title': 'Test2',
            'purchaser': self.user.id,
            'description': 'test2',
            "img_url": 'test2.png',
        }
        url=reverse('snack_create')
        response= self.client.post(path=url, data=data,follow=True)
        self.assertEqual(len(Snack.objects.all()), 2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'snack_detail.html')
        self.assertRedirects(response, reverse('snack_detail',args=[2]))

    def test_snack_delete(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)

    def test_snack_update(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "chocolate","description":"yummy","purchaser":self.user.id}
        )