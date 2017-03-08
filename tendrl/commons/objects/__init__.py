import abc
import six

import etcd

from tendrl.commons.central_store import utils as cs_utils


@six.add_metaclass(abc.ABCMeta)
class BaseObject(object):
    def __init__(
            self,
            attrs=None,
            enabled=None,
            obj_list=None,
            obj_value=None,
            atoms=None,
            flows=None
    ):
        self.attrs = attrs
        self.enabled = enabled

        # path to LIST of all instance of the object
        self.obj_list = obj_list

        # path to GET an instance of the object
        self.obj_value = obj_value

        self.atoms = atoms

        # List of flows under this object
        self.flows = flows

    def __new__(cls, *args, **kwargs):

        super_new = super(BaseObject, cls).__new__
        if super_new is object.__new__:
            instance = super_new(cls)
        else:
            instance = super_new(cls, *args, **kwargs)

        return instance

    def save(self):
        try:
            current_obj = self.load()
            for attr, val in self.__dict__.iteritems():
                if attr in ["attrs", "enabled", "obj_list", "obj_value", "atoms",
                            "flows", "value", "list"]:
                    continue
                if val is None:
                    continue
                if attr.startswith("_"):
                    continue

                setattr(current_obj, attr, val)

            cls_etcd = cs_utils.to_etcdobj(self._etcd_cls, current_obj)
        except etcd.EtcdKeyNotFound as ex:
            cls_etcd = cs_utils.to_etcdobj(self._etcd_cls, self)

        getattr(tendrl_ns.central_store_thread, "save_%s" %
                self.__class__.__name__.lower())(cls_etcd())

    def load(self):
        cls_etcd = cs_utils.to_etcdobj(self._etcd_cls, self)
        result = tendrl_ns.etcd_orm.read(cls_etcd())
        return result.to_tendrl_obj()
