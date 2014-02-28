# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Industry'
        db.create_table(u'deviceapp_industry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'deviceapp', ['Industry'])

        # Adding model 'Manufacturer'
        db.create_table(u'deviceapp_manufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'deviceapp', ['Manufacturer'])

        # Adding model 'Category'
        db.create_table(u'deviceapp_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Industry'])),
            ('totalunits', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'deviceapp', ['Category'])

        # Adding model 'SubCategory'
        db.create_table(u'deviceapp_subcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('maincategory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maincategory', to=orm['deviceapp.Category'])),
            ('totalunits', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'deviceapp', ['SubCategory'])

        # Adding M2M table for field category on 'SubCategory'
        m2m_table_name = db.shorten_name(u'deviceapp_subcategory_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subcategory', models.ForeignKey(orm[u'deviceapp.subcategory'], null=False)),
            ('category', models.ForeignKey(orm[u'deviceapp.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subcategory_id', 'category_id'])

        # Adding model 'Charity'
        db.create_table(u'deviceapp_charity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'deviceapp', ['Charity'])

        # Adding model 'PromoCode'
        db.create_table(u'deviceapp_promocode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('promo_text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            ('uses_left', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('promo_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('factor', self.gf('django.db.models.fields.IntegerField')(max_length=100, null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['PromoCode'])

        # Adding model 'BasicUser'
        db.create_table(u'deviceapp_basicuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=60)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('businesstype', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('phonenumber', self.gf('django.db.models.fields.BigIntegerField')(max_length=10, null=True, blank=True)),
            ('user_rank', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('balanceduri', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('payment_method', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='paymentmethod', null=True, to=orm['deviceapp.Payment'])),
            ('payout_method', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='payoutmethod', null=True, to=orm['deviceapp.Payment'])),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'deviceapp', ['BasicUser'])

        # Adding model 'Item'
        db.create_table(u'deviceapp_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.SubCategory'])),
            ('manufacturer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('serialno', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('modelyear', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('originalowner', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mainimage', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='mainitemimage', null=True, to=orm['deviceapp.Image'])),
            ('contract', self.gf('django.db.models.fields.CharField')(default='none', max_length=40)),
            ('contractdescription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('conditiontype', self.gf('django.db.models.fields.CharField')(default='preowned', max_length=20)),
            ('conditionquality', self.gf('django.db.models.fields.IntegerField')(default=3, max_length=10)),
            ('conditiondescription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('productdescription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('whatsincluded', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('shippingincluded', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('offlineviewing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tos', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('msrp_price', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('price', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('max_price', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('promo_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PromoCode'], null=True, blank=True)),
            ('commission_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sold_online', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('liststatus', self.gf('django.db.models.fields.CharField')(default='incomplete', max_length=30, db_index=True)),
            ('charity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('charity_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Charity'], null=True, blank=True)),
            ('liststage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('savedcount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'deviceapp', ['Item'])

        # Adding model 'Image'
        db.create_table(u'deviceapp_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('photo', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
            ('photo_small', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
            ('photo_medium', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
        ))
        db.send_create_signal(u'deviceapp', ['Image'])

        # Adding model 'Notification'
        db.create_table(u'deviceapp_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'deviceapp', ['Notification'])

        # Adding model 'SellerMessageNotification'
        db.create_table(u'deviceapp_sellermessagenotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('sellermessage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.SellerMessage'])),
        ))
        db.send_create_signal(u'deviceapp', ['SellerMessageNotification'])

        # Adding model 'SellerQuestionNotification'
        db.create_table(u'deviceapp_sellerquestionnotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Question'])),
        ))
        db.send_create_signal(u'deviceapp', ['SellerQuestionNotification'])

        # Adding model 'BuyerQuestionNotification'
        db.create_table(u'deviceapp_buyerquestionnotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Question'])),
        ))
        db.send_create_signal(u'deviceapp', ['BuyerQuestionNotification'])

        # Adding model 'AuthorizedBuyerNotification'
        db.create_table(u'deviceapp_authorizedbuyernotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
        ))
        db.send_create_signal(u'deviceapp', ['AuthorizedBuyerNotification'])

        # Adding model 'SoldNotification'
        db.create_table(u'deviceapp_soldnotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('purchaseditem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PurchasedItem'])),
        ))
        db.send_create_signal(u'deviceapp', ['SoldNotification'])

        # Adding model 'SoldPaymentNotification'
        db.create_table(u'deviceapp_soldpaymentnotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('purchaseditem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PurchasedItem'])),
        ))
        db.send_create_signal(u'deviceapp', ['SoldPaymentNotification'])

        # Adding model 'ShippedNotification'
        db.create_table(u'deviceapp_shippednotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('purchaseditem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PurchasedItem'])),
        ))
        db.send_create_signal(u'deviceapp', ['ShippedNotification'])

        # Adding model 'PayoutNotification'
        db.create_table(u'deviceapp_payoutnotification', (
            (u'notification_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Notification'], unique=True, primary_key=True)),
            ('payout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Payout'], null=True, blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'deviceapp', ['PayoutNotification'])

        # Adding model 'SellerMessage'
        db.create_table(u'deviceapp_sellermessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['SellerMessage'])

        # Adding model 'SavedItem'
        db.create_table(u'deviceapp_saveditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
        ))
        db.send_create_signal(u'deviceapp', ['SavedItem'])

        # Adding model 'LatLong'
        db.create_table(u'deviceapp_latlong', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=5, db_index=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('county', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'deviceapp', ['LatLong'])

        # Adding model 'Question'
        db.create_table(u'deviceapp_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seller', to=orm['deviceapp.BasicUser'])),
            ('dateasked', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dateanswered', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['Question'])

        # Adding model 'Address'
        db.create_table(u'deviceapp_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address_one', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address_two', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(max_length=100)),
            ('phonenumber', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'deviceapp', ['Address'])

        # Adding model 'Payment'
        db.create_table(u'deviceapp_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'], null=True, blank=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['Payment'])

        # Adding model 'CheckAddress'
        db.create_table(u'deviceapp_checkaddress', (
            (u'payment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Payment'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Address'])),
        ))
        db.send_create_signal(u'deviceapp', ['CheckAddress'])

        # Adding model 'BalancedCard'
        db.create_table(u'deviceapp_balancedcard', (
            (u'payment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Payment'], unique=True, primary_key=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cardhash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('expiration_month', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('expiration_year', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('last_four', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
        ))
        db.send_create_signal(u'deviceapp', ['BalancedCard'])

        # Adding model 'BalancedBankAccount'
        db.create_table(u'deviceapp_balancedbankaccount', (
            (u'payment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Payment'], unique=True, primary_key=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fingerprint', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bank_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'deviceapp', ['BalancedBankAccount'])

        # Adding model 'Payout'
        db.create_table(u'deviceapp_payout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('total_commission', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('total_charity', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('cc_fee', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
        ))
        db.send_create_signal(u'deviceapp', ['Payout'])

        # Adding model 'BankPayout'
        db.create_table(u'deviceapp_bankpayout', (
            (u'payout_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Payout'], unique=True, primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BalancedBankAccount'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=20)),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('events_uri', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'deviceapp', ['BankPayout'])

        # Adding model 'CheckPayout'
        db.create_table(u'deviceapp_checkpayout', (
            (u'payout_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Payout'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.CheckAddress'])),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'deviceapp', ['CheckPayout'])

        # Adding model 'Commission'
        db.create_table(u'deviceapp_commission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Item'], unique=True)),
            ('price', self.gf('django.db.models.fields.BigIntegerField')(max_length=12)),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Payment'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'deviceapp', ['Commission'])

        # Adding model 'Checkout'
        db.create_table(u'deviceapp_checkout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('shipping_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Address'], null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Payment'], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('purchased', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('purchased_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['Checkout'])

        # Adding model 'ShoppingCart'
        db.create_table(u'deviceapp_shoppingcart', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.BasicUser'], unique=True, null=True, blank=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['ShoppingCart'])

        # Adding model 'CartItem'
        db.create_table(u'deviceapp_cartitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checkout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Checkout'], null=True, blank=True)),
            ('dateadded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('price', self.gf('django.db.models.fields.BigIntegerField')()),
            ('shoppingcart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.ShoppingCart'], null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=4)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['CartItem'])

        # Adding model 'Order'
        db.create_table(u'deviceapp_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Payment'], null=True, blank=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('total', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('tax', self.gf('django.db.models.fields.BigIntegerField')(default=0, max_length=13)),
            ('shipping_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Address'], null=True, blank=True)),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'deviceapp', ['Order'])

        # Adding model 'PurchasedItem'
        db.create_table(u'deviceapp_purchaseditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchaseditemseller', to=orm['deviceapp.BasicUser'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchaseditembuyer', to=orm['deviceapp.BasicUser'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Order'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('unit_price', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('item_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('charity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('charity_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Charity'], null=True, blank=True)),
            ('promo_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PromoCode'], null=True, blank=True)),
            ('commission', self.gf('django.db.models.fields.BigIntegerField')(max_length=14)),
            ('shipping_included', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('item_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seller_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('buyer_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('paid_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('payout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Payout'], null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['PurchasedItem'])

        # Adding model 'SellerReview'
        db.create_table(u'deviceapp_sellerreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sellerreview_seller', to=orm['deviceapp.BasicUser'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sellerreview_buyer', to=orm['deviceapp.BasicUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('review_rating', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('review', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['SellerReview'])

        # Adding model 'ItemReview'
        db.create_table(u'deviceapp_itemreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itemreview_seller', to=orm['deviceapp.BasicUser'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itemreview_buyer', to=orm['deviceapp.BasicUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PurchasedItem'])),
            ('review_rating', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('review', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['ItemReview'])

        # Adding model 'Report'
        db.create_table(u'deviceapp_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purchased_item', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.PurchasedItem'], unique=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'deviceapp', ['Report'])

        # Adding model 'InactiveRequest'
        db.create_table(u'deviceapp_inactiverequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('reason', self.gf('django.db.models.fields.TextField')()),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['InactiveRequest'])

        # Adding model 'BuyAuthorization'
        db.create_table(u'deviceapp_buyauthorization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='authorizedseller', to=orm['deviceapp.BasicUser'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='authorizedbuyer', to=orm['deviceapp.BasicUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['BuyAuthorization'])

        # Adding model 'ReminderToken'
        db.create_table(u'deviceapp_remindertoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.SellerMessage'])),
            ('action', self.gf('django.db.models.fields.CharField')(default='none', max_length=50)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'deviceapp', ['ReminderToken'])

        # Adding model 'PriceChange'
        db.create_table(u'deviceapp_pricechange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('date_changed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('original_price', self.gf('django.db.models.fields.BigIntegerField')(max_length=14)),
            ('new_price', self.gf('django.db.models.fields.BigIntegerField')(max_length=14)),
        ))
        db.send_create_signal(u'deviceapp', ['PriceChange'])

        # Adding model 'Contact'
        db.create_table(u'deviceapp_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'deviceapp', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'Industry'
        db.delete_table(u'deviceapp_industry')

        # Deleting model 'Manufacturer'
        db.delete_table(u'deviceapp_manufacturer')

        # Deleting model 'Category'
        db.delete_table(u'deviceapp_category')

        # Deleting model 'SubCategory'
        db.delete_table(u'deviceapp_subcategory')

        # Removing M2M table for field category on 'SubCategory'
        db.delete_table(db.shorten_name(u'deviceapp_subcategory_category'))

        # Deleting model 'Charity'
        db.delete_table(u'deviceapp_charity')

        # Deleting model 'PromoCode'
        db.delete_table(u'deviceapp_promocode')

        # Deleting model 'BasicUser'
        db.delete_table(u'deviceapp_basicuser')

        # Deleting model 'Item'
        db.delete_table(u'deviceapp_item')

        # Deleting model 'Image'
        db.delete_table(u'deviceapp_image')

        # Deleting model 'Notification'
        db.delete_table(u'deviceapp_notification')

        # Deleting model 'SellerMessageNotification'
        db.delete_table(u'deviceapp_sellermessagenotification')

        # Deleting model 'SellerQuestionNotification'
        db.delete_table(u'deviceapp_sellerquestionnotification')

        # Deleting model 'BuyerQuestionNotification'
        db.delete_table(u'deviceapp_buyerquestionnotification')

        # Deleting model 'AuthorizedBuyerNotification'
        db.delete_table(u'deviceapp_authorizedbuyernotification')

        # Deleting model 'SoldNotification'
        db.delete_table(u'deviceapp_soldnotification')

        # Deleting model 'SoldPaymentNotification'
        db.delete_table(u'deviceapp_soldpaymentnotification')

        # Deleting model 'ShippedNotification'
        db.delete_table(u'deviceapp_shippednotification')

        # Deleting model 'PayoutNotification'
        db.delete_table(u'deviceapp_payoutnotification')

        # Deleting model 'SellerMessage'
        db.delete_table(u'deviceapp_sellermessage')

        # Deleting model 'SavedItem'
        db.delete_table(u'deviceapp_saveditem')

        # Deleting model 'LatLong'
        db.delete_table(u'deviceapp_latlong')

        # Deleting model 'Question'
        db.delete_table(u'deviceapp_question')

        # Deleting model 'Address'
        db.delete_table(u'deviceapp_address')

        # Deleting model 'Payment'
        db.delete_table(u'deviceapp_payment')

        # Deleting model 'CheckAddress'
        db.delete_table(u'deviceapp_checkaddress')

        # Deleting model 'BalancedCard'
        db.delete_table(u'deviceapp_balancedcard')

        # Deleting model 'BalancedBankAccount'
        db.delete_table(u'deviceapp_balancedbankaccount')

        # Deleting model 'Payout'
        db.delete_table(u'deviceapp_payout')

        # Deleting model 'BankPayout'
        db.delete_table(u'deviceapp_bankpayout')

        # Deleting model 'CheckPayout'
        db.delete_table(u'deviceapp_checkpayout')

        # Deleting model 'Commission'
        db.delete_table(u'deviceapp_commission')

        # Deleting model 'Checkout'
        db.delete_table(u'deviceapp_checkout')

        # Deleting model 'ShoppingCart'
        db.delete_table(u'deviceapp_shoppingcart')

        # Deleting model 'CartItem'
        db.delete_table(u'deviceapp_cartitem')

        # Deleting model 'Order'
        db.delete_table(u'deviceapp_order')

        # Deleting model 'PurchasedItem'
        db.delete_table(u'deviceapp_purchaseditem')

        # Deleting model 'SellerReview'
        db.delete_table(u'deviceapp_sellerreview')

        # Deleting model 'ItemReview'
        db.delete_table(u'deviceapp_itemreview')

        # Deleting model 'Report'
        db.delete_table(u'deviceapp_report')

        # Deleting model 'InactiveRequest'
        db.delete_table(u'deviceapp_inactiverequest')

        # Deleting model 'BuyAuthorization'
        db.delete_table(u'deviceapp_buyauthorization')

        # Deleting model 'ReminderToken'
        db.delete_table(u'deviceapp_remindertoken')

        # Deleting model 'PriceChange'
        db.delete_table(u'deviceapp_pricechange')

        # Deleting model 'Contact'
        db.delete_table(u'deviceapp_contact')


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
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
            'tax': ('django.db.models.fields.BigIntegerField', [], {'default': '0', 'max_length': '13'}),
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
            'promo_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'uses_left': ('django.db.models.fields.IntegerField', [], {'max_length': '5'})
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