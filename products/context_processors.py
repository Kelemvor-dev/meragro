from .forms import CreateProductForm, EditProductForm


def crateProductForm(request):
    crateProduct_form = CreateProductForm()
    editProduct_form = EditProductForm()

    return {
        'crateProduct_form': crateProduct_form,
        'editProduct_form': editProduct_form,
    }
