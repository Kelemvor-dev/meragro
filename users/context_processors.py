from .forms import UserLoginForm, UserSignUpForm, UserEditProfileForm


def login_form(request):
    login_form = UserLoginForm()
    signup_form = UserSignUpForm()
    edit_form = UserEditProfileForm()
    return {
        'loginForm': login_form,
        'signupForm': signup_form,
        'edit_form': edit_form
    }