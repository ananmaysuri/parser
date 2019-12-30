import asvmq
import asvprotobuf

pub = asvmq.Publisher(topic_name="imu_raw", object_type=asvprotobuf.sensor_pb2.Imu)

string = '''
roll di. pitch di. yaw di. accelp di. gyrop di. temperature di.
roll = -1.812914e-01

pitch = 9.814460e-02

yaw = 306.542542

accelp = 00-- -1.648378
01-- -3.322935
02-- 1002.729431


gyrop = 00-- 0.000000e+00
01-- 0.000000e+00
02-- 0.000000e+00


temperature = 29.500000
'''


def callback(data):
	data = [i for i in serial_msg.data.split("\r\n") if len(i)!=0]
	msg = asvprotobuf.sensor_pb2.Imu()
	msg.header = serial_msg.header

	msg.linear_acceleration.x = float(data[5][14:])/100
	msg.linear_acceleration.y = float(data[6][5:])/100
	msg.linear_acceleration.z = float(data[7][5:])/100
	msg.angular_velocity.x = -float(data[8][13:])
	msg.angular_velocity.y = -float(data[9][5:])
	msg.angular_velocity.z = -float(data[10][5:])
	temp_msg = sensor_msgs.msg.Temperature()
	z_error = [yaw, pitch, roll]
	expected_z = 9.81*math.cos(z_error[1])*math.cos(z_error[2])
	expected_x = 9.81*math.sin(z_error[1])
	expected_y = 9.81*math.sin(z_error[2])
	if(np.sign(expected_z)!=np.sign(msg.linear_acceleration.z)):
		expected_z *= -1
	if(np.sign(expected_x)!=np.sign(msg.linear_acceleration.x)):
		expected_x *= -1
	if(np.sign(expected_y)!=np.sign(msg.linear_acceleration.y)):
		expected_y *= -1
	msg.linear_acceleration.z = float("%f" % (msg.linear_acceleration.z-expected_z))
	msg.linear_acceleration.x = float("%f" % (msg.linear_acceleration.x-expected_x))
	msg.linear_acceleration.y = float("%f" % (msg.linear_acceleration.y-expected_y))
	temp_msg.header = msg.header
	temp_msg.temperature = float(data[11][14:])
	pub.publish(data)
	pub_temp.publish(temp_msg)

asvmq.Subscriber(topic_name="imu_raw", object_type=asvprotobuf.sensor_pb2.Imu, callback=callback)
