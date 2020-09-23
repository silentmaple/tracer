from django.test import TestCase
import re
import redis
from django_redis import get_redis_connection
# Create your tests here.

# a = "16630967001"
a = '13567891234'
# print(re.match(r'1[3][5][6][7][8][9]\d{9}$', a))
print(re.match(r'1[356789]\d{9}$', a))

