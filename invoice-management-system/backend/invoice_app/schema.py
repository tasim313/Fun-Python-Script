# invoice_app/schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Invoice
from .ocr_utils import extract_invoice_data

class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice

class Query(graphene.ObjectType):
    invoices = graphene.List(InvoiceType)

    def resolve_invoices(self, info):
        return Invoice.objects.all()

class UploadInvoice(graphene.Mutation):
    class Arguments:
        file = graphene.String(required=True)

    invoice = graphene.Field(InvoiceType)

    def mutate(self, info, file):
        data = extract_invoice_data(file)
        invoice = Invoice.objects.create(**data)
        return UploadInvoice(invoice=invoice)

class Mutation(graphene.ObjectType):
    upload_invoice = UploadInvoice.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)