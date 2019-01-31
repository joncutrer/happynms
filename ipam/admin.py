from django.contrib import admin
from .models import Block, Address
import logging


logger = logging.getLogger('happynms')
logger.debug('IPAM.admin')


class BlockAdmin(admin.ModelAdmin):
    list_display = ('network_id', 'total_addresses',
                    'short_description', 'updated_at')

admin.site.register(Address)
admin.site.register(Block, BlockAdmin)
