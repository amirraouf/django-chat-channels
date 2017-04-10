from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView

from users.models import LoggedIn

User = get_user_model()

@login_required(login_url='/login/')
def user_list(request):
    try :
        LoggedIn.objects.create(user=request.user)
    except IntegrityError:
        pass
    users = User.objects.select_related('loggedin')
    for user in users:
        user.status = 'Online' if hasattr(user, 'loggedin') else 'Offline'

    return render(request, 'registration/list.html', {'users': users})


log_in = LoginView.as_view()


class MsgLogoutView(LogoutView):
    next_page = 'msgs:log_in'

    def dispatch(self, request, *args, **kwargs):
        user = getattr(request, 'user', None)
        try:
            loggedin_user = LoggedIn.objects.get(user=user)
            loggedin_user.delete()
        except LoggedIn.DoesNotExist:
            pass
        logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)
log_out = MsgLogoutView.as_view()
