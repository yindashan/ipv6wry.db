#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack, unpack_from
import ipaddr

def inet_ntoa(number):
	addresslist=[]
	addresslist.append((number>>24)&0xff)
	addresslist.append((number>>16)&0xff)
	addresslist.append((number>>8)&0xff)
	addresslist.append(number&0xff)
	return ".".join("%d" % i for i in addresslist)

class IPDBv4(object):
	"""qqwry.db数据库查询功能集合
	"""
	def __init__(self, dbname = "qqwry.db"):
		""" 初始化类，读取数据库内容为一个字符串
		"""
	
		self.dbname = dbname
		f = file(dbname, "rb")
		self.img = f.read()
		f.close()

		if self.img[:4] != "IPDB":
			# 数据库格式错误
			return
		if self.getLong8(4, 2) > 1:
			# 数据库格式错误
			return
		self.firstIndex = self.getLong8(16)
		self.indexCount = self.getLong8(8)
		self.offlen = self.getLong8(6, 1)
	
	def getString(self, offset = 0):
		""" 读取字符串信息，包括"国家"信息和"地区"信息

		QQWry.Dat的记录区每条信息都是一个以"\0"结尾的字符串"""
		
		o2 = self.img.find("\0", offset)
		# 有可能只有国家信息没有地区信息，
		gb_str = self.img[offset:o2]
		try:
			utf8_str = unicode(gb_str,"utf-8")
		except:
			return u"未知数据"
		return utf8_str

	def getLong3(self, offset = 0):
		"""QQWry.Dat中的偏移记录都是3字节，本函数取得3字节的偏移量的常规表示
		QQWry.Dat使用“字符串“存储这些值"""
		s = self.img[offset: offset + 3]
		s += "\0"
		# unpack用一个"I"作为format，后面的字符串必须是4字节
		return unpack("I", s)[0]

	def getLong4(self, offset = 0):
		s = self.img[offset: offset + 4]
		return unpack("I", s)[0]

	def getLong8(self, offset = 0, size = 8):
		s = self.img[offset: offset + size]
		s += "\0\0\0\0\0\0\0\0"
		return unpack_from("Q", s)[0]

	def getAreaAddr(self, offset = 0):
		""" 通过给出偏移值，取得区域信息字符串，"""
		
		byte = ord(self.img[offset])
		if byte == 1 or byte == 2:
			# 第一个字节为1或者2时，取得2-4字节作为一个偏移量调用自己
			p = self.getLong8(offset + 1, self.offlen)
			return self.getAreaAddr(p)
		else:
			return self.getString(offset)

	def getAddr(self, offset, ip = 0):
		img = self.img
		o = offset
		byte = ord(img[o])

		if byte == 1:
			# 重定向模式1
			# [IP][0x01][国家和地区信息的绝对偏移地址]
			# 使用接下来的3字节作为偏移量调用字节取得信息
			return self.getAddr(self.getLong8(o + 1, self.offlen))

		else:
			# 重定向模式2 + 正常模式
			# [IP][0x02][信息的绝对偏移][...]
			cArea = self.getAreaAddr(o)
			if byte == 2:
				o += 1 + self.offlen
			else:
				o = self.img.find("\0",o) + 1
			aArea = self.getAreaAddr(o)
			return (cArea, aArea)

	def find(self, ip, l, r):
		""" 使用二分法查找网络字节编码的IP地址的索引记录"""
		if r - l <= 1:
			return l

		m = (l + r) / 2
		o = self.firstIndex + m * (4 + self.offlen)
		new_ip = self.getLong4(o)
		if ip < new_ip:
			return self.find(ip, l, m)
		else:
			return self.find(ip, m, r)
		
	def getIPAddr(self, ip):
		""" 调用其他函数，取得信息！"""
		try:
			# 把IP地址转成数字
			ip4 = ipaddr.IPAddress(ip)
			ip = int(ip4)
			# 使用 self.find 函数查找ip的索引偏移
			i = self.find(ip, 0, self.indexCount)
			# 得到索引记录
			o = self.firstIndex + i * (4 + self.offlen)
			o2 = self.getLong8(o + 4, self.offlen)
			(c, a) = self.getAddr(o2)
			(cc, aa) = (c, a)
			i1 = inet_ntoa(self.getLong4(o))
			try:
				i2 = inet_ntoa(self.getLong4(o + 4 + self.offlen) - 1)
			except:
				i2 = "255.255.255.255"
		except:
			i1 = ""
			i2 = ""
			c = cc = u"错误的IP地址"
			a = aa = ""
		return (i1, i2, c + u" " + a, cc, aa)
		
#	def output(self, first, last):
#		for i in range(first, last):
#			o = self.firstIndex +  i * 7
#			ip = inet_ntoa(pack("!I", unpack("I", self.img[o:o+4])[0]))
#			offset = self.getLong3(o + 4)
#			(c, a) = self.getAddr(offset + 4)
#			print "%s %d %s/%s" % (ip, offset, c, a)

