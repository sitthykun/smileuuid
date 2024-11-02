"""
Author: masakokh
Version: 1.0.0
Note: library
"""
# built-in
import hashlib
import os
from datetime import datetime
# external
import redis


class SmileUuid:
	"""

	"""
	CACHE_NAME:str  = 'cache'
	START_NUMBER:int= 100000000000000

	def __init__(self, key: str, isForceOverrideNewId: bool= False, enableRedis: bool= False, startId: int= None, increment: int= None, cachePath: str= ''):
		"""

		"""
		# private
		## number
		self.__numberInc: int   = increment if increment else 1
		self.__numberOrigin: int= startId if startId else 0
		self.__numberStart: int = self.__numberOrigin
		## file
		self.__cachePath: str   = cachePath
		self.__filename: str    = ''
		self.__keyUuid: str     = key
		## setting
		self.__enableRedis: bool= enableRedis
		self.__isForceNew: bool = isForceOverrideNewId
		## other
		self.__redis: redis     = redis.Redis()
		self.__redisExpire: int = 0
		## default
		self.__resultFail: int      = -1
		self.__resultSuccess: int   = 1
		self.__resultNerd: int      = 0
		# load
		self.__load()

	def __createFilename(self) -> int:
		try:
			#
			with open(self.__getFilename(), 'w') as fo:
				fo.write('')
				#
				return self.__resultSuccess

		except Exception as e:
			return self.__resultFail

	def __encryptFilename(self) -> str:
		"""

		:return:
		"""
		# Encode the string to bytes, then hash it
		hashObject:hashlib  = hashlib.md5(self.__keyUuid.encode())
		# Convert the hash to a hexadecimal string
		hashHex:str         = hashObject.hexdigest()
		#
		return hashHex

	def __getFilename(self) -> str:
		"""

		:return:
		"""
		try:
			#
			if self.__filename:
				return self.__filename

			#
			else:
				# Ensure the cache directory exists
				if self.__cachePath:
					os.makedirs(os.path.join(self.__cachePath, SmileUuid.CACHE_NAME), exist_ok= True)
					self.__filename = os.path.join(self.__cachePath, SmileUuid.CACHE_NAME, self.__encryptFilename())

				else:
					os.makedirs(os.path.join(SmileUuid.CACHE_NAME), exist_ok= True)
					self.__filename = os.path.join(SmileUuid.CACHE_NAME, self.__encryptFilename())
				#
				return self.__filename

		except Exception as e:
			return ''

	def __load(self) -> None:
		"""

		:return:
		"""
		# override with the new value at the instance object
		if self.__isForceNew and self.__numberStart > 0:
			# write the read file
			self.saveCache()
		else:
			#
			if self.__enableRedis:
				# nothing add first time
				pass
			#
			elif self.__validFilename():
				# load from exist file
				self.__numberStart  = self.__readFilename()
			else:
				# will use the default
				self.__numberStart  = SmileUuid.START_NUMBER

	def __readFilename(self) -> int:
		"""

		:return:
		"""
		try:
			#
			with open(self.__getFilename(), 'r') as fo:
				#
				firstLine: str = fo.readline().strip()
				#
				return int(firstLine)

		except Exception as e:
			# return 1 or 0
			# create
			return self.__saveFilename()

	def __readRedis(self) -> int:
		"""

		:return:
		"""
		try:
			# Retrieves the data stored with this key
			value: str  = self.__redis.get(self.__keyUuid)

			#
			if value:
				# Decode the byte string to a regular string
				return int(value.decode('utf-8'))
			#
			return self.__resultNerd

		except Exception as e:
			return self.__resultFail

	def __saveFilename(self) -> int:
		"""

		:return:
		"""
		try:
			#
			with open(self.__getFilename(), 'w') as fo:
				#
				fo.write(
					str(self.__numberStart)
				)
			#
			return self.__resultSuccess

		except Exception as e:
			return self.__resultNerd

	def __saveRedis(self) -> int:
		"""

		:return:
		"""
		try:
			# scalar value
			self.__redis.set(
				name    = self.__keyUuid
				, value = self.__numberStart
				, ex    = self.__redisExpire
			)
			#
			return self.__resultNerd

		except Exception as e:
			return self.__resultFail

	def __validFilename(self) -> bool:
		"""

		:return:
		"""
		return bool(self.__getFilename() and os.path.exists(self.__getFilename()))

	def configRedis(self, host: str, port: int, index: int, password: str, expire: int = 300000, showMessage: bool= False) -> int:
		"""

		:param host:
		:param port:
		:param index:
		:param password:
		:param expire:
		:param showMessage:
		:return:
		"""
		try:
			#
			self.__redis        = redis.Redis(host= host, port= port, db= index, password= password)
			self.__redisExpire  = expire
			# Test the connection
			try:
				if self.__redis.ping():
					temp                = self.__readRedis()
					#
					if temp == -1 or temp == 0:
						self.__numberStart  = SmileUuid.START_NUMBER
						# update
						self.__saveRedis()
					else:
						self.__numberStart  = temp

					#
					if showMessage:
						print('Connected to Redis successfully!')

			except redis.ConnectionError:
				print('Could not connect to Redis')
			#
			return self.__resultSuccess

		except Exception as e:
			return self.__resultFail

	def currentId(self) -> int:
		"""

		:return:
		"""
		#
		return self.__numberStart

	def getLastModification(self) -> str:
		"""

		:return:
		"""
		filename    = self.__getFilename()
		#
		if filename != '':
			# Get the last modified time
			timestamp = os.path.getmtime(filename)
			# Convert it to a datetime object
			#lastModifiedDate    = datetime.fromtimestamp(timestamp)
			#return lastModifiedDate
			return str(datetime.fromtimestamp(timestamp))
		#
		return ''

	def nextId(self) -> int:
		"""

		:return:
		"""
		#
		self.__numberStart  = self.__numberStart + self.__numberInc
		#
		return self.__numberStart

	def saveCache(self) -> int:
		"""

		:return:
		"""
		try:
			#
			if self.__enableRedis:
				return self.__saveRedis()
			#
			else:
					# if self.__validFilename():
					# 	return 0
					if not self.__createFilename():
						return self.__resultNerd
					#
					return self.__saveFilename()

		except Exception as e:
			return self.__resultFail

	def removeCache(self) -> int:
		"""

		:return:
		"""
		try:
			#
			if self.__enableRedis:
				return self.__saveRedis()
			#
			else:
				#
				os.remove(self.__getFilename())
				#
				return self.__resultSuccess

		except Exception as e:
			return self.__resultFail
