from django import forms

class NewProductForm(forms.Form):
    productName = forms.CharField(label='Product Name', max_length=250, required=True)
    productDescription = forms.CharField(label='Product Description', required=True)
    productPrice = forms.DecimalField(label='Product Price', max_digits=5, decimal_places=2, required=True)
    productImage = forms.ImageField(label='image', required=False)

class AddImageForm(forms.Form):
    newImage = forms.ImageField(label='image', required=False)