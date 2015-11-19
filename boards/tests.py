import json

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.test import TestCase

from boards.models import Sticker


class StickerAPITestCase(TestCase):

    fixtures = ['boards/fixtures/fixture.json']

    def setUp(self):
        self.client.post(
            reverse('login'),
            {
                'username': 'u1',
                'password': 'u1',
            }
        )

    def test_get_sticker_api(self):
        Sticker.objects.filter(~Q(pk=1)).delete()
        response = self.client.get(reverse('boards:api-stickers'))
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(
            response_json,
            {
                u'TEST0-1': {
                    u'status': u'OPEN',
                    u'caption': u'stick0',
                    u'description': u'desc0'
                }
            }
        )
