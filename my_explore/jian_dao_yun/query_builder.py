# -*- coding: utf-8 -*-


class JDYQueryBuilderMixin(object):
    """JDY 数据筛选器"""

    def __init__(self, fields, limit=100):
        self.fields = fields
        self.limit = limit

    @property
    def data_id(self):
        """类似于游标的作用"""
        if hasattr(self, '_data_id'):
            return self._data_id
        return ""

    @property
    def rel(self):
        """rel  必需  String  筛选组合关系；“and”(满足所有过滤条件), “or”(满足任一过滤条件)"""
        if hasattr(self, '_rel'):
            return self._rel
        return "and"

    @property
    def cond(self):
        if hasattr(self, '_cond'):
            return self._cond
        return []

    # @data_id.setter
    # def data_id(self, value):
    #     setattr(self, "_data_id", value)

    def set_data_id(self, data_id):
        setattr(self, "_data_id", data_id)

    def set_rel(self, rel):
        if rel not in ['and', 'or']:
            raise Exception
        else:
            setattr(self, '_rel', rel)

    @staticmethod
    def create_cond_single(field, method, value=None, type_=None):
        """单条筛选"""

        value = [] if not value else value
        assert field and method
        assert method in ["empty", "not_empty", "eq", "in", "range", "nin", "ne", "like"]
        assert type(value) == list
        # 过滤方法；“not_empty”(不为空)，“empty”(为空)，“eq”(等于)，“in”(等于任意一个)，“range”(在x与y之间，并且包含x和y本身)，
        # “nin”(不等于任意一个)，“ne”(不等于), “like”(文本包含)

        cond = {
            "field": field,
            "method": method,
        }

        if type_:
            cond["type"] = type_
        if value:
            cond["value"] = value

        return cond

    def add_cond_single(self, field, method, value=None, type_=None):
        value = [] if not value else value
        single = self.create_cond_single(field, method, value, type_)
        if hasattr(self, '_cond'):
            self._cond.append(single)
        else:
            setattr(self, '_cond', [single])

    def data_query(self):
        query = {
            "data_id": self.data_id,
            "limit": self.limit,
            "fields": self.fields,
            "filter": {
                "rel": self.rel,
                "cond": self.cond
            }
        }
        return query

    def __repr__(self):
        return '<Query Body(data_id={self.data_id!r})>'.format(self=self)
