from django.db import models
import datetime
import ipaddress
from django.template.defaultfilters import truncatechars
import logging


logger = logging.getLogger('happynms')
logger.debug('IPAM.models')


class Block(models.Model):

    ADDRESS_CATEGORY_CHOICES = (
        ('priv', 'Private'),
        ('pub', 'Public'),
    )
    network_id = models.CharField(max_length=20)
    mask = models.IntegerField(null=True, blank=True)
    start_address = models.CharField(
        max_length=20, null=True, blank=True)
    end_address = models.CharField(max_length=20, null=True, blank=True)
    address_category = models.CharField(
        max_length=4,
        choices=ADDRESS_CATEGORY_CHOICES,
        default='priv',
    )
    total_addresses = models.IntegerField(null=True, blank=True)
    assigned_addresses = models.IntegerField(default=0, null=True)
    utilized_addresses = models.IntegerField(default=0, null=True)
    percentage_assigned = models.IntegerField(default=0, null=True)
    percentage_utilized = models.IntegerField(default=0, null=True)
    description = models.TextField(max_length=1024, null=True, blank=True)
    rir = models.CharField(max_length=7, null=True, blank=True)
    rir_handle = models.CharField(max_length=30, null=True, blank=True)
    rir_assigned = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def short_description(self):
        return truncatechars(self.description, 80)

    def __str__(self):
        return self.network_id

    def __unicode__(self):
        return self.network_id

    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_update_timestamp', False):
            self.updated_at = datetime.datetime.now()

        # If creating record vs updating
        if not self.pk:
            logger.debug('Adding/Calculating Block!')
            net = ipaddress.ip_network(self.network_id)

            if not self.start_address:
                self.start_address = net.network_address

            if not self.end_address:
                self.end_address = net.broadcast_address

            if not self.total_addresses:
                self.total_addresses = net.num_addresses

        super(Block, self).save(*args, **kwargs)


class Address(models.Model):

    ip_address = models.CharField(max_length=20)
    mac_address = models.CharField(max_length=20, null=True)
    hostname = models.CharField(max_length=255, null=True)
    note = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=20, null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.network_id

    def __unicode__(self):
        return self.ip_address

    def save(self, *args, **kwargs):

        if not kwargs.pop('skip_update_timestamp', False):
            self.updated_at = datetime.datetime.now()

        super(Address, self).save(*args, **kwargs)
