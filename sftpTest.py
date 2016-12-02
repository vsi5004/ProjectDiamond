import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu', 'username':'ftpuser', 'password':'test1234', 'port':109}
try:
	with pysftp.Connection(**cinfo) as sftp:
		try:
			with sftp.cd('/home/IvanIakimenko/ProjectDiamond/payload'):
				sftp.put('message.json')
		except:
			print( "file issue")
except (Exception, err):
	print (err)
