from django.urls import path
from main.views import index, redy_to_test, test, checktest, new_question, new_test
from main.users_view import signup

urlpatterns = [
    # BOSH SAHIFA
    path('', index, name='index'),
    # USER URL
    path('accounts/signup/', signup, name='signup'),
    # TEST URL
    path('<int:test_id>/redy_to_test', redy_to_test, name='redy_to_test'),
    path('<int:test_id>/test', test, name='test'),
    path('<int:checktest_id>/checktest', checktest, name='checktest'),
    # TEST YARATISH UCHUN URL
    path('new_test', new_test, name='new_test'),
    path('<int:test_id>/new_question', new_question, name='new_question'),
]