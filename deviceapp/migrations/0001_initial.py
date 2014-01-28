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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'deviceapp', ['Manufacturer'])

        # Adding model 'Category'
        db.create_table(u'deviceapp_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Industry'])),
            ('totalunits', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'deviceapp', ['Category'])

        # Adding model 'SubCategory'
        db.create_table(u'deviceapp_subcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('maincategory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maincategory', to=orm['deviceapp.Category'])),
            ('totalunits', self.gf('django.db.models.fields.IntegerField')()),
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

        # Adding model 'Image'
        db.create_table(u'deviceapp_image', (
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('photo_small', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
            ('photo_medium', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'deviceapp', ['Image'])

        # Adding model 'BasicUser'
        db.create_table(u'deviceapp_basicuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('businesstype', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('address_one', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('address_two', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=60, null=True)),
            ('phonenumber', self.gf('django.db.models.fields.BigIntegerField')(max_length=14)),
            ('user_rank', self.gf('django.db.models.fields.CharField')(default='newb', max_length=20)),
            ('balanceduri', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('payout_method', self.gf('django.db.models.fields.CharField')(default='none', max_length=20)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(default='none', max_length=20)),
            ('default_payment_cc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BalancedCard'], null=True, blank=True)),
            ('default_payment_ba', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='default_payment_ba', null=True, to=orm['deviceapp.BalancedBankAccount'])),
            ('default_payout_ba', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='default_payout_ba', null=True, to=orm['deviceapp.BalancedBankAccount'])),
            ('check_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.UserAddress'], null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['BasicUser'])

        # Adding model 'Item'
        db.create_table(u'deviceapp_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.SubCategory'])),
            ('manufacturer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('serialno', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('modelyear', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('originalowner', self.gf('django.db.models.fields.BooleanField')()),
            ('mainimage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Image'], null=True, blank=True)),
            ('contract', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('contractdescription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('conditiontype', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('conditionquality', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('conditiondescription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('productdescription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('whatsincluded', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('shippingincluded', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('offlineviewing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tos', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('msrp_price', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('price', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('promo_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PromoCode'], null=True, blank=True)),
            ('commission_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sold_online', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('liststatus', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('listeddate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('savedcount', self.gf('django.db.models.fields.IntegerField')()),
            ('liststage', self.gf('django.db.models.fields.IntegerField')()),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'deviceapp', ['Item'])

        # Adding model 'SellerMessage'
        db.create_table(u'deviceapp_sellermessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['SellerMessage'])

        # Adding model 'SavedItem'
        db.create_table(u'deviceapp_saveditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
        ))
        db.send_create_signal(u'deviceapp', ['SavedItem'])

        # Adding model 'ItemImage'
        db.create_table(u'deviceapp_itemimage', (
            (u'image_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Image'], unique=True, primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'], null=True)),
        ))
        db.send_create_signal(u'deviceapp', ['ItemImage'])

        # Adding model 'LatLong'
        db.create_table(u'deviceapp_latlong', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(max_length=5, db_index=True)),
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
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Item'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seller', to=orm['deviceapp.BasicUser'])),
            ('dateasked', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dateanswered', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['Question'])

        # Adding model 'UserAddress'
        db.create_table(u'deviceapp_useraddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address_one', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address_two', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(max_length=100)),
            ('phonenumber', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'deviceapp', ['UserAddress'])

        # Adding model 'BalancedCard'
        db.create_table(u'deviceapp_balancedcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'], null=True, blank=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('brand', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cardhash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('expiration_month', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('expiration_year', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('last_four', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['BalancedCard'])

        # Adding model 'BalancedBankAccount'
        db.create_table(u'deviceapp_balancedbankaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'], null=True, blank=True)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fingerprint', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bank_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('verification_uri', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'deviceapp', ['BalancedBankAccount'])

        # Adding model 'Checkout'
        db.create_table(u'deviceapp_checkout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('shipping_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.UserAddress'], null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(default='none', max_length=20)),
            ('cc_payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BalancedCard'], null=True, blank=True)),
            ('ba_payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BalancedBankAccount'], null=True, blank=True)),
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
            ('shoppingcart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.ShoppingCart'], null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
        ))
        db.send_create_signal(u'deviceapp', ['CartItem'])

        # Adding model 'BankPayout'
        db.create_table(u'deviceapp_bankpayout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BalancedBankAccount'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['BankPayout'])

        # Adding model 'CheckPayout'
        db.create_table(u'deviceapp_checkpayout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BasicUser'])),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.UserAddress'])),
        ))
        db.send_create_signal(u'deviceapp', ['CheckPayout'])

        # Adding model 'Commission'
        db.create_table(u'deviceapp_commission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.Item'], unique=True)),
            ('amount', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(default='none', max_length=20)),
            ('cc_payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BalancedCard'], null=True, blank=True)),
            ('ba_payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BalancedBankAccount'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['Commission'])

        # Adding model 'PurchasedItem'
        db.create_table(u'deviceapp_purchaseditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchaseditemseller', to=orm['deviceapp.BasicUser'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchaseditembuyer', to=orm['deviceapp.BasicUser'])),
            ('total', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('unit_price', self.gf('django.db.models.fields.BigIntegerField')(max_length=20)),
            ('cartitem', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deviceapp.CartItem'], unique=True)),
            ('checkout', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.Checkout'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('item_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('purchase_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('item_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seller_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('buyer_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('paid_out', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('payout_method', self.gf('django.db.models.fields.CharField')(default='none', max_length=20)),
            ('online_payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.BankPayout'], null=True, blank=True)),
            ('check', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.CheckPayout'], null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['PurchasedItem'])

        # Adding model 'SellerReview'
        db.create_table(u'deviceapp_sellerreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sellerreviewseller', to=orm['deviceapp.BasicUser'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sellerreviewbuyer', to=orm['deviceapp.BasicUser'])),
            ('review_rating', self.gf('django.db.models.fields.IntegerField')(max_length=20)),
            ('review', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['SellerReview'])

        # Adding model 'ItemReview'
        db.create_table(u'deviceapp_itemreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itemreview_seller', to=orm['deviceapp.BasicUser'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itemreview_buyer', to=orm['deviceapp.BasicUser'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['deviceapp.PurchasedItem'])),
            ('review_rating', self.gf('django.db.models.fields.IntegerField')(max_length=20)),
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

        # Adding model 'PromoCode'
        db.create_table(u'deviceapp_promocode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('promo_text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('promo_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('factor', self.gf('django.db.models.fields.IntegerField')(max_length=100, null=True, blank=True)),
            ('discount', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'deviceapp', ['PromoCode'])


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

        # Deleting model 'Image'
        db.delete_table(u'deviceapp_image')

        # Deleting model 'BasicUser'
        db.delete_table(u'deviceapp_basicuser')

        # Deleting model 'Item'
        db.delete_table(u'deviceapp_item')

        # Deleting model 'SellerMessage'
        db.delete_table(u'deviceapp_sellermessage')

        # Deleting model 'SavedItem'
        db.delete_table(u'deviceapp_saveditem')

        # Deleting model 'ItemImage'
        db.delete_table(u'deviceapp_itemimage')

        # Deleting model 'LatLong'
        db.delete_table(u'deviceapp_latlong')

        # Deleting model 'Question'
        db.delete_table(u'deviceapp_question')

        # Deleting model 'UserAddress'
        db.delete_table(u'deviceapp_useraddress')

        # Deleting model 'BalancedCard'
        db.delete_table(u'deviceapp_balancedcard')

        # Deleting model 'BalancedBankAccount'
        db.delete_table(u'deviceapp_balancedbankaccount')

        # Deleting model 'Checkout'
        db.delete_table(u'deviceapp_checkout')

        # Deleting model 'ShoppingCart'
        db.delete_table(u'deviceapp_shoppingcart')

        # Deleting model 'CartItem'
        db.delete_table(u'deviceapp_cartitem')

        # Deleting model 'BankPayout'
        db.delete_table(u'deviceapp_bankpayout')

        # Deleting model 'CheckPayout'
        db.delete_table(u'deviceapp_checkpayout')

        # Deleting model 'Commission'
        db.delete_table(u'deviceapp_commission')

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

        # Deleting model 'PromoCode'
        db.delete_table(u'deviceapp_promocode')


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
        u'deviceapp.balancedbankaccount': {
            'Meta': {'object_name': 'BalancedBankAccount'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bank_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fingerprint': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']", 'null': 'True', 'blank': 'True'}),
            'verification_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.balancedcard': {
            'Meta': {'object_name': 'BalancedCard'},
            'brand': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cardhash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expiration_month': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'expiration_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_four': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']", 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.bankpayout': {
            'Meta': {'object_name': 'BankPayout'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BalancedBankAccount']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.basicuser': {
            'Meta': {'object_name': 'BasicUser'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'balanceduri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'businesstype': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'check_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.UserAddress']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'default_payment_ba': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_payment_ba'", 'null': 'True', 'to': u"orm['deviceapp.BalancedBankAccount']"}),
            'default_payment_cc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BalancedCard']", 'null': 'True', 'blank': 'True'}),
            'default_payout_ba': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_payout_ba'", 'null': 'True', 'to': u"orm['deviceapp.BalancedBankAccount']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '20'}),
            'payout_method': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '20'}),
            'phonenumber': ('django.db.models.fields.BigIntegerField', [], {'max_length': '14'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_rank': ('django.db.models.fields.CharField', [], {'default': "'newb'", 'max_length': '20'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
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
        u'deviceapp.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'checkout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Checkout']", 'null': 'True', 'blank': 'True'}),
            'dateadded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'shoppingcart': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.ShoppingCart']", 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.category': {
            'Meta': {'object_name': 'Category'},
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Industry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'totalunits': ('django.db.models.fields.IntegerField', [], {})
        },
        u'deviceapp.checkout': {
            'Meta': {'object_name': 'Checkout'},
            'ba_payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BalancedBankAccount']", 'null': 'True', 'blank': 'True'}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            'cc_payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BalancedCard']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '20'}),
            'purchased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'purchased_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.UserAddress']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'deviceapp.checkpayout': {
            'Meta': {'object_name': 'CheckPayout'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.UserAddress']"}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.commission': {
            'Meta': {'object_name': 'Commission'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'ba_payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BalancedBankAccount']", 'null': 'True', 'blank': 'True'}),
            'cc_payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BalancedCard']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Item']", 'unique': 'True'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '20'})
        },
        u'deviceapp.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
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
            'commission_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'conditiondescription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'conditionquality': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'conditiontype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'contract': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'contractdescription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listeddate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'liststage': ('django.db.models.fields.IntegerField', [], {}),
            'liststatus': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'mainimage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Image']", 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modelyear': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'msrp_price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'offlineviewing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'originalowner': ('django.db.models.fields.BooleanField', [], {}),
            'price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'productdescription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'promo_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PromoCode']", 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'savedcount': ('django.db.models.fields.IntegerField', [], {}),
            'serialno': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'shippingincluded': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sold_online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.SubCategory']"}),
            'tos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'whatsincluded': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'deviceapp.itemimage': {
            'Meta': {'object_name': 'ItemImage', '_ormbases': [u'deviceapp.Image']},
            u'image_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.Image']", 'unique': 'True', 'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']", 'null': 'True'})
        },
        u'deviceapp.itemreview': {
            'Meta': {'object_name': 'ItemReview'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'itemreview_buyer'", 'to': u"orm['deviceapp.BasicUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.PurchasedItem']"}),
            'review': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'review_rating': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
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
            'zipcode': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'db_index': 'True'})
        },
        u'deviceapp.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'cartitem': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.CartItem']", 'unique': 'True'}),
            'check': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.CheckPayout']", 'null': 'True', 'blank': 'True'}),
            'checkout': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Checkout']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'item_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'online_payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BankPayout']", 'null': 'True', 'blank': 'True'}),
            'paid_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paid_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payout_method': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '20'}),
            'purchase_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchaseditemseller'", 'to': u"orm['deviceapp.BasicUser']"}),
            'seller_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'total': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'}),
            'unit_price': ('django.db.models.fields.BigIntegerField', [], {'max_length': '20'})
        },
        u'deviceapp.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.Item']"}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.sellerreview': {
            'Meta': {'object_name': 'SellerReview'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sellerreviewbuyer'", 'to': u"orm['deviceapp.BasicUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'review_rating': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sellerreviewseller'", 'to': u"orm['deviceapp.BasicUser']"})
        },
        u'deviceapp.shoppingcart': {
            'Meta': {'object_name': 'ShoppingCart'},
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deviceapp.BasicUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'deviceapp.subcategory': {
            'Meta': {'object_name': 'SubCategory'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['deviceapp.Category']", 'symmetrical': 'False'}),
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maincategory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maincategory'", 'to': u"orm['deviceapp.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'totalunits': ('django.db.models.fields.IntegerField', [], {})
        },
        u'deviceapp.useraddress': {
            'Meta': {'object_name': 'UserAddress'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['deviceapp.BasicUser']", 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['deviceapp']