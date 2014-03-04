from django.db import models

############################################
####### Questions Model  ###################
############################################
class Question(models.Model):
	item = models.ForeignKey('listing.Item')
	buyer = models.ForeignKey('account.BasicUser',related_name="questionbuyer")
	seller = models.ForeignKey('account.BasicUser',related_name="questionseller")
	dateasked = models.DateTimeField(auto_now_add = True)
	dateanswered = models.DateTimeField(blank=True,null=True)
	question = models.TextField()
	answer = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.question
