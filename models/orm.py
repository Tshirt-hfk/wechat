import logging; logging.basicConfig(level=logging.INFO)
import pymysql
from DBUtils.PooledDB import PooledDB

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

def create_pool(**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = PooledDB(
    	creator=pymysql,
        cursorclass=pymysql.cursors.DictCursor,
        use_unicode=True,
    	host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        mincached=5,
        maxcached=10,
    )

		
def select(sql, args, size=None):
	log(sql, args)
	global __pool
	try:
		conn = __pool.connection()
		cur = conn.cursor()
		cur.execute(sql.replace('?', '%s'), args or ())
		if size:
			rs = cur.fetchmany(size)
		else:
			rs = cur.fetchall()
	except BaseException as e:
		raise
	finally:
		cur.close()
		conn.close()
		logging.info('rows returned: %s' % len(rs))
	return rs

def execute(sql, args):
	log(sql)
	global __pool
	try:
		conn = __pool.connection()
		cur = conn.cursor()
		cur.execute(sql.replace('?', '%s'), args)
		conn.commit()
		affected = cur.rowcount
	except BaseException as e:
		raise
	finally:
		cur.close()
		conn.close()
	return affected

def create_args_string(num):
	L = []
	for n in range(num):
		L.append('?')
	return ', '.join(L)
	
class Field(object):
	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default
	def __str__(self):
		return ('<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name))

class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, column_type='varchar(50)'):
        super().__init__(name, column_type, primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'int', primary_key, default)

class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise StandardError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise StandardError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f:'`%s`' %f, fields))
        attrs['__table__'] = tableName
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' %(primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into  `%s` (%s, `%s`) values(%s)' %(tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s` = ?' %(tableName, ', '.join(map(lambda f:'`%s`=?' %(mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from  `%s` where `%s`=?' %(tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):

	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

	def getValue(self, key):
		return getattr(self, key, None)

	def getValueOrDefault(self, key):
		value = getattr(self, key, None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default value for %s: %s' % (key, str(value)))
				setattr(self, key, value)
		return value

	@classmethod
	def find(cls, pk):#通过主键查找
		rs = select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
		if len(rs) == 0:
			return None
		return cls(**rs[0])

	@classmethod
	def findAll(cls, **kw):#一般性查找
		rs = []
		if len(kw) == 0:
			rs = select(cls.__select__, None)
		else:
			args = []
			values = []
			for k,v in kw.items():
				args.append('`%s`=?' % k)
				values.append(v)
			rs = select('%s where %s ' % (cls.__select__, ' and '.join(args)), values)
		return [cls(**r) for r in rs]

	def save(self):
		args = list(map(self.getValueOrDefault, self.__fields__))
		args.append(self.getValueOrDefault(self.__primary_key__))
		rows = execute(self.__insert__, args)
		if rows != 1:
			logging.warn('failed to insert record: affected rows: %s' % rows)

	def update(self):
		args = list(map(self.getValue, self.__fields__))
		args.append(self.getValue(self.__primary_key__))
		rows = execute(self.__update__, args)
		if rows != 1:
			logging.warn('failed to update by primary key: affected rows: %s' % rows)

	def remove(self):
		args = [self.getValue(self.__primary_key__)]
		rows = execute(self.__delete__, args)
		if rows != 1:
			logging.warn('failed to remove by primary key: affected rows: %s' % rows)
