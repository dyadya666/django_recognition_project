from io import BytesIO
from PIL import Image
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import UploadedImage


def small_png_bytes():
    buf = BytesIO()
    img = Image.new('RGBA', (1,1), (255, 0, 0, 0))
    img.save(buf, format='PNG')

    return buf.getvalue()


class UploadViewTests(TestCase):
    def setUp(self):
        self.url = reverse('recognition_images:home')
    
    @patch('recognition_images.views.classify_image')
    def test_successful_upload_saves_model_and_result(self, mock_classify):
        result_mock_value = "cat (99.00%)"
        mock_classify.return_value = result_mock_value
        img = SimpleUploadedFile('test.png', small_png_bytes(), content_type='image/png')

        resp = self.client.post(self.url, {'image': img}, follow=True)

        # Перевірка відповіді і створення об'єкта
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(UploadedImage.objects.count(), 1)
        
        # Отримуємо result з мок-значенням
        obj = UploadedImage.objects.first()
        self.assertIsNotNone(obj)

        # Перевіряємо що result містить те, що повернув mock
        self.assertEqual(obj.result, result_mock_value)
        # Перевіряємо що сторінка показує строку результату
        self.assertContains(resp, result_mock_value)

    def test_invalid_form_no_file_shows_errors(self):
        resp = self.client.post(self.url, {}, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(UploadedImage.objects.exists())
        self.assertContains(resp, 'Завантажити')
    
    @patch('recognition_images.views.classify_image')
    def test_classify_error_is_saved_in_result(self, mock_classify):
        failed_str = 'model failed'
        error_str = 'Error:'
        mock_classify.side_effect = RuntimeError(failed_str)
        img = SimpleUploadedFile('test.png', small_png_bytes(), content_type='image/png')
        
        resp = self.client.post(self.url, {'image': img}, follow=True)
        self.assertEqual(resp.status_code, 200)

        obj = UploadedImage.objects.first()
        self.assertIsNotNone(obj)
        self.assertTrue(obj.result.startswith(error_str))
        self.assertIn(failed_str, obj.result)
        self.assertContains(resp, error_str)
