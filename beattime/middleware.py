from django.conf import settings
from django.contrib import auth
import time
from datetime import datetime, timedelta


class AutoLogout:
    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        t = datetime.now()
        t_inseconds = time.mktime(t.timetuple())
        # import ipdb; ipdb.set_trace()
        try:
            # date = datetime.strptime(request.session['last_touch'], '%Y-%m-%d %H:%M:%S')
            if (
                t_inseconds - request.session['last_touch'] >
                settings.AUTO_LOGOUT_DELAY
                # timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0)
            ):
                auth.logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = t_inseconds
