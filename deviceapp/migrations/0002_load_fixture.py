# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "app_start_data.json")
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'deviceapp.address': {
            'Meta': {'object_name': 'Address'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']", 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {'max_length': '100'})
        },
        u'deviceapp.authorizedbuyernotification': {
            'Meta': {'object_name': 'AuthorizedBuyerNotification', '_ormbases': [u'deviceapp.Notification']},
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'deviceapp.balancedbankaccount': {
            'Meta': {'object_name': 'BalancedBankAccount', '_ormbases': [u'deviceapp.Payment']},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bank_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fingerprint': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'payment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Payment']", 'unique': 'True', 'primary_key': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'deviceapp.balancedcard': {
            'Meta': {'object_name': 'BalancedCard', '_ormbases': [u'deviceapp.Payment']},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cardhash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expiration_month': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'expiration_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'last_four': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            u'payment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Payment']", 'unique': 'True', 'primary_key': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'deviceapp.bankpayout': {
            'Meta': {'object_name': 'BankPayout', '_ormbases': [u'deviceapp.Payout']},
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BalancedBankAccount']"}),
            'events_uri': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'payout_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Payout']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'deviceapp.basicuser': {
            'Meta': {'object_name': 'BasicUser'},
            'balanceduri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'businesstype': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '60'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'payment_method': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paymentmethod'", 'null': 'True', 'to': u"orm['deviceapp.Payment']"}),
            'payout_method': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payoutmethod'", 'null': 'True', 'to': u"orm['deviceapp.Payment']"}),
            'phonenumber': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_rank': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
        },
        u'deviceapp.buyauthorization': {
            'Meta': {'object_name': 'BuyAuthorization'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authorizedbuyer'", 'to': u"orm['deviceapp.BasicUser']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authorizedseller'", 'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.buyerquestionnotification': {
            'Meta': {'object_name': 'BuyerQuestionNotification', '_ormbases': [u'deviceapp.Notification']},
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Question']"})
        },
        u'deviceapp.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'checkout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Checkout']", 'null': 'True', 'blank': 'True'}),
            'dateadded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'price': ('django.db.models.fields.BigIntegerField', [], {}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '4'}),
            'shoppingcart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.ShoppingCart']", 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.category': {
            'Meta': {'object_name': 'Category'},
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Industry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'totalunits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'deviceapp.charity': {
            'Meta': {'object_name': 'Charity'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'deviceapp.checkaddress': {
            'Meta': {'object_name': 'CheckAddress', '_ormbases': [u'deviceapp.Payment']},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Address']"}),
            u'payment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Payment']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'deviceapp.checkout': {
            'Meta': {'object_name': 'Checkout'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Payment']", 'null': 'True', 'blank': 'True'}),
            'purchased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'purchased_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Address']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'deviceapp.checkpayout': {
            'Meta': {'object_name': 'CheckPayout', '_ormbases': [u'deviceapp.Payout']},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.CheckAddress']"}),
            u'payout_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Payout']", 'unique': 'True', 'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'deviceapp.commission': {
            'Meta': {'object_name': 'Commission'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Item']", 'unique': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Payment']"}),
            'price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '12'}),
            'transcation_number': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'deviceapp.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']", 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'photo': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'photo_medium': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'photo_small': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'})
        },
        u'deviceapp.inactiverequest': {
            'Meta': {'object_name': 'InactiveRequest'},
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'reason': ('django.db.models.fields.TextField', [], {})
        },
        u'deviceapp.industry': {
            'Meta': {'object_name': 'Industry'},
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'deviceapp.item': {
            'Meta': {'object_name': 'Item'},
            'charity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'charity_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Charity']", 'null': 'True', 'blank': 'True'}),
            'commission_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'conditiondescription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'conditionquality': ('django.db.models.fields.IntegerField', [], {'default': '3', 'max_length': '10'}),
            'conditiontype': ('django.db.models.fields.CharField', [], {'default': "'preowned'", 'max_length': '20'}),
            'contract': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '40'}),
            'contractdescription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liststage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'liststatus': ('django.db.models.fields.CharField', [], {'default': "'incomplete'", 'max_length': '30', 'db_index': 'True'}),
            'mainimage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mainitemimage'", 'null': 'True', 'to': u"orm['deviceapp.Image']"}),
            'manufacturer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'max_price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'modelyear': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'msrp_price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'offlineviewing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'originalowner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'productdescription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'promo_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PromoCode']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'savedcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'serialno': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'shippingincluded': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sold_online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.SubCategory']"}),
            'tos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'whatsincluded': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'deviceapp.itemreview': {
            'Meta': {'object_name': 'ItemReview'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'itemreview_buyer'", 'to': u"orm['deviceapp.BasicUser']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PurchasedItem']"}),
            'review': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'review_rating': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'itemreview_seller'", 'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.latlong': {
            'Meta': {'object_name': 'LatLong'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '5', 'db_index': 'True'})
        },
        u'deviceapp.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'deviceapp.notification': {
            'Meta': {'object_name': 'Notification'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'deviceapp.order': {
            'Meta': {'object_name': 'Order'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Payment']", 'null': 'True', 'blank': 'True'}),
            'purchase_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Address']", 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'deviceapp.payment': {
            'Meta': {'object_name': 'Payment'},
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']", 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.payout': {
            'Meta': {'object_name': 'Payout'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'cc_fee': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_charity': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'total_commission': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.payoutnotification': {
            'Meta': {'object_name': 'PayoutNotification', '_ormbases': [u'deviceapp.Notification']},
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'}),
            'payout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Payout']", 'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'deviceapp.pricechange': {
            'Meta': {'object_name': 'PriceChange'},
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'new_price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '14'}),
            'original_price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '14'})
        },
        u'deviceapp.promocode': {
            'Meta': {'object_name': 'PromoCode'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'discount': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'factor': ('django.db.models.fields.IntegerField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'promo_text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'promo_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'deviceapp.purchaseditem': {
            'Meta': {'object_name': 'PurchasedItem'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchaseditembuyer'", 'to': u"orm['deviceapp.BasicUser']"}),
            'buyer_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'charity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'charity_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Charity']", 'null': 'True', 'blank': 'True'}),
            'commission': ('django.db.models.fields.BigIntegerField', [], {'max_length': '14'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'item_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Order']"}),
            'paid_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paid_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Payout']", 'null': 'True', 'blank': 'True'}),
            'promo_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PromoCode']", 'null': 'True', 'blank': 'True'}),
            'purchase_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchaseditemseller'", 'to': u"orm['deviceapp.BasicUser']"}),
            'seller_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shipping_included': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'unit_price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'})
        },
        u'deviceapp.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            'dateanswered': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dateasked': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seller'", 'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.remindertoken': {
            'Meta': {'object_name': 'ReminderToken'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '50'}),
            'contact_message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.SellerMessage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'deviceapp.report': {
            'Meta': {'object_name': 'Report'},
            'details': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchased_item': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.PurchasedItem']", 'unique': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'deviceapp.saveditem': {
            'Meta': {'object_name': 'SavedItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.sellermessage': {
            'Meta': {'object_name': 'SellerMessage'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'deviceapp.sellermessagenotification': {
            'Meta': {'object_name': 'SellerMessageNotification', '_ormbases': [u'deviceapp.Notification']},
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'}),
            'sellermessage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.SellerMessage']"})
        },
        u'deviceapp.sellerquestionnotification': {
            'Meta': {'object_name': 'SellerQuestionNotification', '_ormbases': [u'deviceapp.Notification']},
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Question']"})
        },
        u'deviceapp.sellerreview': {
            'Meta': {'object_name': 'SellerReview'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sellerreview_buyer'", 'to': u"orm['deviceapp.BasicUser']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'review_rating': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sellerreview_seller'", 'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.shippednotification': {
            'Meta': {'object_name': 'ShippedNotification', '_ormbases': [u'deviceapp.Notification']},
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'}),
            'purchaseditem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PurchasedItem']"})
        },
        u'deviceapp.shoppingcart': {
            'Meta': {'object_name': 'ShoppingCart'},
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.BasicUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.soldnotification': {
            'Meta': {'object_name': 'SoldNotification', '_ormbases': [u'deviceapp.Notification']},
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'}),
            'purchaseditem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PurchasedItem']"})
        },
        u'deviceapp.soldpaymentnotification': {
            'Meta': {'object_name': 'SoldPaymentNotification', '_ormbases': [u'deviceapp.Notification']},
            u'notification_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Notification']", 'unique': 'True', 'primary_key': 'True'}),
            'purchaseditem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PurchasedItem']"})
        },
        u'deviceapp.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['deviceapp.Category']", 'symmetrical': 'False'}),
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maincategory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maincategory'", 'to': u"orm['deviceapp.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'totalunits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['deviceapp']
    symmetrical = True
