# -*- coding=utf-8 -*-

from flask.ext.principal import RoleNeed, Permission

auth = Permission(RoleNeed('authenticated'))

# this is assigned when you want to block a permission to all
# never assign this role to anyone !
null = Permission(RoleNeed('null'))
admin = Permission(RoleNeed('superuser'))
