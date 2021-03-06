from django_webtest import WebTest

from django.contrib.auth.models import User

from seimas.website.models import Voting


class ImportVotesTests(WebTest):

    def test_import_votes(self):
        user = User.objects.create_superuser('admin', 'admin@example.com', 'secret')

        self.assertEqual(Voting.objects.count(), 0)

        resp = self.app.get('/admin/website/voting/add/', user='admin')
        resp.form['title'] = 'Balsavimo internetu koncepcijos patvirtinimas'
        resp.form['link'] = 'http://www3.lrs.lt/pls/inter/w5_sale.bals?p_bals_id=18573'
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(Voting.objects.count(), 1)

        voting = Voting.objects.get()

        self.assertEqual(voting.author.pk, user.pk)
        self.assertEqual(voting.vid, '18573')
        self.assertEqual(voting.vote_set.count(), 141)
