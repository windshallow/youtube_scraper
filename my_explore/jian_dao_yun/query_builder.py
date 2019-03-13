# -*- coding: utf-8 -*-


class JDYQueryBuilderMixin(object):
    """JDY 数据筛选器"""

    @property
    def data_id(self):
        """类似于游标的作用"""
        if hasattr(self, '_data_id'):
            return self._data_id
        return ""

    @property
    def limit(self):
        if hasattr(self, '_limit'):
            return self._limit
        return 100

    @property
    def fields(self):
        if hasattr(self, "_fields"):
            return self._fields
        return []

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

    def set_data_id(self, value):
        setattr(self, "_data_id", value)

    def set_limit(self, value):
        setattr(self, "_limit", value)

    def set_fields(self, value):
        setattr(self, "_fields", value)

    def set_rel(self, value):
        if value not in ['and', 'or']:
            raise Exception
        else:
            setattr(self, '_rel', value)

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

    @property
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
        return '<Query Body({self.data_query!r})>'.format(self=self)


if __name__ == '__main__':
    import json

    obj = JDYQueryBuilderMixin()
    obj.set_data_id(110)
    obj.set_limit(66)
    obj.set_fields(['aa', 'bb'])
    obj.set_rel('and')
    obj.add_cond_single('aa', 'eq', ['hello'])
    obj.add_cond_single('bb', 'not_empty')
    print obj
    print(json.dumps(obj.data_query, indent=2))  # indent 缩进格数
