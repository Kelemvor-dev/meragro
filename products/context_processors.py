from .forms import CreateProductForm


def crateProductForm(request):
    crateProduct_form = CreateProductForm()

    return {
        'crateProduct_form': crateProduct_form,
    }