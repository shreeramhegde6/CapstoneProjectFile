from cloudguard.azure_client import Resource
from cloudguard.models import PolicyRule
from cloudguard.rules import RequiredTagsRule,OpenNSGPortRule
def test_missing_tag():
 p=PolicyRule(config={"required_tags":["owner"]}); r=Resource("1","vm","vm",{},{}); assert RequiredTagsRule().evaluate(r,p)=={"missing_tags":["owner"]}
def test_open_port():
 p=PolicyRule(config={"ports":[22]}); r=Resource("1","nsg","Microsoft.Network/networkSecurityGroups",{}, {"security_rules":[{"access":"Allow","source":"*","port":22}]}); assert OpenNSGPortRule().evaluate(r,p)
