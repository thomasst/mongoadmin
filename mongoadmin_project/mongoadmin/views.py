from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView, FormView
from django.shortcuts import get_object_or_404

from pymongo.objectid import ObjectId
from pymongo import json_util

import json

from ..common.utils import ellipsize
from . import models, forms

class ConnectionDetailMixin(object):
    model = models.MongoConnection

    def setup_connection(self):
        self.connection = get_object_or_404(models.MongoConnection, name=self.kwargs['connection_name'])
        if 'database_name' in self.kwargs:
            self.database = self.connection.get_connection()[self.kwargs['database_name']]
            if 'collection_name' in self.kwargs:
                self.collection = self.database[self.kwargs['collection_name']]

    """
    def get_context_data(self, **kwargs):
        context = super(ConnectionDetailMixin, self).get_context_data(**kwargs)
        self.connection = get_object_or_404(models.MongoConnection, name=self.kwargs['connection_name'])
        context['connection'] = self.connection
        return context
    """

class ConnectionView(ConnectionDetailMixin, TemplateView):
    template_name = 'mongoadmin/connection.html'

    def get_context_data(self, **kwargs):
        context = super(ConnectionView, self).get_context_data(**kwargs)
        self.setup_connection()
        databases = self.connection.get_connection().database_names()
        context.update({
            'connection': self.connection,
            'databases': databases,
        })
        return context


class DatabaseView(ConnectionDetailMixin, TemplateView):
    template_name = 'mongoadmin/database.html'

    def get_context_data(self, **kwargs):
        context = super(DatabaseView, self).get_context_data(**kwargs)
        self.setup_connection()
        collections = self.database.collection_names()
        context.update({
            'connection': self.connection,
            'database': self.kwargs['database_name'],
            'collections': collections,
        })
        return context


class CollectionView(ConnectionDetailMixin, TemplateView):
    template_name = 'mongoadmin/collection.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)

        self.setup_connection()

        documents = self.collection.find()

        def prepare_document(document):
            del document['_id']
            return ellipsize(json.dumps(document, default=json_util.default), 120)

        documents_list = [(document['_id'], prepare_document(document)) for document in documents]

        context.update({
            'connection': self.connection,
            'database': self.kwargs['database_name'],
            'collection': self.kwargs['collection_name'],
            'documents': documents_list,
        })
        return context


class BaseDocumentView(ConnectionDetailMixin, FormView):
    template_name = 'mongoadmin/document.html'
    form_class = forms.DocumentForm

    def form_valid(self, form):
        obj = form.cleaned_data['json']
        id = form.cleaned_data['id']
        if id and '_id' not in obj:
            obj['_id'] = ObjectId(id)
        print obj
        id = self.collection.save(obj)
        messages.success(self.request, 'The document %s was saved successfully.' % id)
        if '_continue' in self.request.POST:
            return HttpResponseRedirect('../%s/' % id)
        elif '_addanother' in self.request.POST:
            return HttpResponseRedirect('../new/')
        else:
            return HttpResponseRedirect('../')

    def get(self, request, *args, **kwargs):
        self.setup_connection()
        self.document = self.get_document()
        return super(BaseDocumentView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.setup_connection()
        self.document = self.get_document()
        return super(BaseDocumentView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseDocumentView, self).get_context_data(**kwargs)
        context.update({
            'connection': self.connection,
            'database': self.kwargs['database_name'],
            'collection': self.kwargs['collection_name'],
            'document_id': self.document and str(self.document['_id']) or '',
        })
        return context

class CreateDocumentView(BaseDocumentView):
    def get_document(self):
        return None

    def get_initial(self):
        return {
            'json': '{}',
            'id': '',
        }

class UpdateDocumentView(BaseDocumentView):
    def get_document(self):
        document = self.collection.find_one({'_id': ObjectId(self.kwargs['pk'])})
        return document

    def get_initial(self):
        # document = self.document.copy()
        # del document['_id']
        # json_data = json.dumps(document, default=json_util.default)
        json_data = json.dumps(self.document, default=json_util.default)
        return {
            'json': json_data,
            'id': str(self.document['_id']),
        }
