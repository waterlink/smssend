#coding=utf-8
import subprocess
from pyquery import PyQuery as PQ
import httplib2
from PIL import Image
import urllib
import re
import os
import time

http = httplib2.Http()

addr = 'http://www.mts.com.ua/ukr/sendsms.php'
response, text = http.request(addr)
headers = {}
headers['Cookie'] = response['set-cookie']
# text = open('sms_form').read().decode('cp1251')
d = PQ(text)

# print '<form name="Data" action="http://www.mts.com.ua/back/modules/sms/db_sms.php" method="post" class="send_sms">'
# print d('form[name="Data"]').find('[name]')
captcha = d('form[name="Data"]').find('img')
src = captcha.attr('src')
src = 'http://www.mts.com.ua' + src
captcha.attr('src', src)
# print captcha
response, image_data = http.request(src, headers=headers)
open('img.png', 'w').write(image_data)
# print '<input type="submit" value="Submit" />'
# print '<a href="javascript:document.Data.submit();">Send SMS</a>'
# print '</form>'

# print 

data = {}
data['lang'] = 'lat'

def out(x, y):
	# print d(y)
	print d(y)
	if not d(y).attr('type'):
		d(y).attr('type', 'none')
	if d(y).attr('type').lower() == 'hidden':
		data[d(y).attr('name')] = d(y).val()
	elif d(y).attr('type').lower() == 'text' or d(y).is_('textarea'):
		data[d(y).attr('name')] = raw_input(d(y).attr('name') + ' ---> ')
	elif d(y).is_('select'):
		vals = map(lambda x: d(x).val(), d(y).find('option'))
		print 'choose one of:', vals
		data[d(y).attr('name')] = raw_input(d(y).attr('name') + ' ---> ')
	elif d(y).attr('name') == 'captcha':
		im = Image.open('img.png')
		im.show()
		data[d(y).attr('name')] = raw_input(d(y).attr('name') + ' ---> ')

d('form[name="Data"]').find('[name]').filter('[type="hidden"]').each(out)
print '-' * 10
d('form[name="Data"]').find('[name]').filter('[type!="hidden"]').each(out)
print data


headers['Content-type'] = 'application/x-www-form-urlencoded'
response, content = http.request(
	'http://www.mts.com.ua/back/modules/sms/db_sms.php',
	'POST',
	headers=headers,
	body=urllib.urlencode(data)
)

print response, content
res = re.findall(r'sms_message=([^$]*)$', response['location'])
print res == ['2']
if res == ['2']:
	open(os.path.join(
		'success',
		data['captcha'] + '_' + str(time.time())
	), 'w').write(
		open('img.png').read()
	)
