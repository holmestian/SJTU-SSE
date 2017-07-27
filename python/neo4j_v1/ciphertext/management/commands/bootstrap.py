# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.management.base import BaseCommand
from django.db import DatabaseError
import uuid
from ciphertext.models import Ciphertext, Key
from SJTU_SSE_v2 import db

__author__ = 'wangjksjtu'


class Command(BaseCommand):
    help = 'Create a NodeHandle and set handle_id for nodes missing handle_id property'

    def handle(self, *args, **options):
        with db.manager.session as s:
            s.run('CREATE CONSTRAINT ON (k:Key) ASSERT k.handle_id IS UNIQUE')
            s.run('CREATE CONSTRAINT ON (c:Ciphertext) ASSERT c.handle_id IS UNIQUE')

            try:
                q = """
                    OPTIONAL MATCH (c:Ciphertext) WHERE NOT exists(c.handle_id) WITH collect(id(c)) as ciphertexts
                    OPTIONAL MATCH (k:Key) WHERE NOT exists(k.handle_id) WITH ciphertexts, collect(id(k)) as keys
                    RETURN ciphertexts, keys
                    """

                record = s.run(q).single()
                ciphertexts = record['ciphertexts']
                keys = record['keys']
            except IndexError:
                ciphertexts, keys = [], []

        q = 'MATCH (n) WHERE ID(n) = $node_id SET n.handle_id = $handle_id'
        c, k = 0, 0
        ciphertexts_objs = []
        keys_objs = []
        with db.manager.transaction as t:
            try:
                for node_id in ciphertexts:
                    ciphertext = Ciphertext(handle_id=str(uuid.uuid4()))
                    ciphertexts_objs.append(ciphertext)
                    t.run(q, {'node_id': node_id, 'handle_id': ciphertext.handle_id})
                    c += 1
            except Exception as e:
                raise e
            else:
                try:
                    Ciphertext.objects.bulk_create(ciphertexts_objs)
                except DatabaseError as e:
                    raise e

        with db.manager.transaction as t:
            try:
                for node_id in keys:
                    key = Key(handle_id=str(uuid.uuid4()))
                    keys_objs.append(key)
                    t.run(q, {'node_id': node_id, 'handle_id': key.handle_id})
                    k += 1
            except Exception as e:
                raise e
            else:
                try:
                    Key.objects.bulk_create(keys_objs)
                except DatabaseError as e:
                    raise e

        self.stdout.write('Successfully completed! Added %d ciphertexts and %d keys.' % (c, k))
