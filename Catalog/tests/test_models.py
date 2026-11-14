from django.test import TestCase
from django.db import IntegrityError
from Catalog.tests.helpers import InitProducts
from Catalog.models import (
    ProductVariant,
    Attribute,
    AttributeValue,
    VariantAttributeValue
)





class TestProductVariantModel(TestCase):
    
    def setUp(self):
        self.product, _ = InitProducts()
        self.colour = Attribute.objects.create(name='Colour')
        self.size = Attribute.objects.create(name="Size")
        self.red = AttributeValue.objects.create(attribute=self.colour, value="Red")
        self.large = AttributeValue.objects.create(attribute=self.size, value="Large")
        self.variant = ProductVariant.objects.create(
            product=self.product,
            # name='',
            price=27000,
            stock_quantity=10,
            is_active=True
        )

    def test_variant_name_defaults_to_product(self):
        self.assertEqual(self.variant.name, self.product.name)

        # print('-'*50)
        # print(self.variant.name, self.product.name)
        # print('-'*50)

    def test_variant_name_updates_when_attribute_added(self):
        VariantAttributeValue.objects.create(variant=self.variant, attribute=self.colour, attribute_value=self.red)
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.name, f"{self.product.name} - Red")

    def test_name_joins_attributes_sorted_by_attribute_name(self):
        VariantAttributeValue.objects.create(variant=self.variant, attribute=self.colour, attribute_value=self.red)
        VariantAttributeValue.objects.create(variant=self.variant, attribute=self.size, attribute_value=self.large)
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.name, f"{self.product.name} - Red/Large")
        
    def test_variant_name_updates_when_attribute_removed(self):
        val = VariantAttributeValue.objects.create(variant=self.variant, attribute=self.colour, attribute_value=self.red)
        val.delete()
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.name, f"{self.product.name}")

    def test_variant_cannot_have_two_values_of_same_attribute(self):
        blue = AttributeValue.objects.create(attribute=self.colour, value='Blue')
        VariantAttributeValue.objects.create(variant=self.variant, attribute=self.colour, attribute_value=self.red)
        self.assertRaises(
            IntegrityError,
            VariantAttributeValue.objects.create,
            variant=self.variant,
            attribute=self.colour,
            attribute_value=blue
        )









