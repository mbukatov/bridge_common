import datetime
from dateutil import parser
from inspect import getframeinfo
from inspect import stack
import json
import sys
from tendrl.commons.utils.time_utils import now

# TODO(anmol, collectd) This is a workaround required due to
# https://github.com/collectd/collectd/issues/2179
# An appropriate solution needs to be carved out
is_collectd_imported = False
if '/usr/lib64/collectd' in sys.path:
    is_collectd_imported = True
    sys.path.remove('/usr/lib64/collectd')
import uuid  # noqa: E402
if is_collectd_imported:
    sys.path.append('/usr/lib64/collectd')


class Message(object):
    """At the time of message object intialization

    message_id, timestamp and caller are always None
    because it assinged by Message class but request_id,
    flwo_id, parent_id, cluster_id may come, when from_json
    function call message old message_id, time_stamp and
    caller is populated
    """
    def __init__(self, priority, publisher, payload, request_id=None,
                 flow_id=None, parent_id=None, cluster_id=None,
                 message_id=None, timestamp=None, node_id=None,
                 caller=None, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        if message_id is None:
            self.message_id = str(uuid.uuid4())
            self.timestamp = now()
            # From which function, line and file error raised
            caller = getframeinfo(stack()[1][0])
            self.caller = {"filename": (caller.filename.rsplit('/', 1))[1],
                           "line_no": caller.lineno,
                           "function": caller.function}
        else:
            self.message_id = message_id
            self.timestamp = timestamp
            self.caller = caller
        self.priority = priority
        self.publisher = publisher
        self.node_id = node_id
        if self.node_id is None:
            self.node_id = tendrl_ns.node_context.node_id
        self.request_id = request_id
        self.flow_id = flow_id
        self.parent_id = parent_id
        self.cluster_id = cluster_id
        self.payload = payload

    @staticmethod
    def from_json(json_str):
        message_json = json.loads(json_str)
        timestamp = parser.parse(message_json["timestamp"])
        message_json["timestamp"] = timestamp
        message = Message(**message_json)
        if not message.validate():
            # Invalid message logged as debug
            message_new = Message("debug",
                                  "node-agent",
                                  {"message": message})
            return message_new
        else:
            return message

    @staticmethod
    def to_json(message):
        return json.dumps(message.__dict__, default=serialize_message)

    def validate(self):
        priorities = ["debug", "info", "notice",
                      "warning", "error", "critical"]
        """Validation for the object

        check all the mandatory fields are present,
        check payload is in dict format,
        if payload contains job id then it is considered
        as job_updates, job updates should have flow id,
        Check priorities and publishers are correct
        """

        # Check payload type is dict
        if type(self.payload) != dict:
            return False
        # Check mandatory fields
        if (self.priority not in priorities or
            self.node_id is None or
                "message" not in self.payload):
            return False
        if self.request_id is not None:
            if self.flow_id is None:
                return False

        return True


# To serialize when json contains old message object
def serialize_message(obj):
    if isinstance(obj, Message):
        serial = obj.__dict__
        return serial
    elif isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
    else:
        raise TypeError(
            "Message object is not serializable")
