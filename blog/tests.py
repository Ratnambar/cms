from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from blog.models import Post, Category
from account.models import Profile
from blog.forms import PostForm
from django.urls import reverse

# Create your tests here.


class PostCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testuser2'
        )
        print(self.user.username)

        self.profile = Profile.objects.get(user=self.user)
        self.profile.display_name = 'testuser2_profile'
        self.profile.bio = 'testuser2_bio'
        self.profile.save()

        self.category = Category.objects.create(
            name='testcategory2',
            description='testcategory2_description'
        )
        
        add_post_permission = Permission.objects.get(codename='add_post')
        self.user.user_permissions.add(add_post_permission)

        self.client = Client()
        self.client.login(username='testuser2', password='testuser2')

    def test_post_creation(self):
        """Test that a post can be created with all required fields"""
        add_post = Post.objects.create(
            title='testpost2',
            content='testpost2_content',
            status='P',
            category=self.category,
            author=self.profile
        )

        self.assertEqual(add_post.title, 'testpost2')
        self.assertEqual(add_post.status, 'P')
        self.assertEqual(add_post.category, self.category)
        self.assertEqual(add_post.author, self.profile)
        self.assertEqual(add_post.content, 'testpost2_content')
        self.assertEqual(add_post.author.user.username, 'testuser2')


class PostFormViewTestCase(TestCase):
    def setUp(self):
        password = 'testuser'
        self.user = User.objects.create_user(
            username='testuser', password=password
        )
        self.profile = Profile.objects.get(user=self.user)
        self.category = Category.objects.create(name='testcategory',
        description='testcategory_description')

        add_post_permission = Permission.objects.get(codename='add_post')
        self.user.user_permissions.add(add_post_permission)

        self.client = Client()
        self.client.login(username=self.user.username, password=password)
        self.url = reverse('post')

    def test_get_post_creation_page(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'blog/post.html')
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_creation_success(self):
        form_data = {
            'title': 'testpost',
            'content': 'testpost_content',
            'status': 'P',
            'category': self.category.id,
            'author': self.profile.id
        }

        response = self.client.post(self.url, form_data)

        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'testpost')
        self.assertEqual(post.content, 'testpost_content')
        self.assertEqual(post.status, 'P')
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.author, self.profile)


class PostFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser')
        self.profile = Profile.objects.get(user=self.user)
        self.category = Category.objects.create(name='testcategory', description='testcategory_description')

    def test_post_form_valid(self):
        form_data = {
            'title': 'testpost',
            'content': 'testpost_content',
            'status': 'P',
            'category': self.category.id,
            'author': self.profile.id
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_missing_title(self):
        form_data = {
            'content': 'testpost_content',
            'status': 'P',
            'category': self.category.id,
            'author': self.profile.id
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_post_form_missing_content(self):
        form_data = {
            'title': 'testpost',
            'status': 'P',
            'category': self.category.id,
            'author': self.profile.id
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_post_form_missing_category(self):
        form_data = {
            'title': 'testpost',
            'content': 'testpost_content',
            'status': 'P',
            'author': self.profile.id
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        
        
    