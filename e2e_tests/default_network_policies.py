import re
import logging

import e2e_tests.test_base as tb
import e2e_tests.network_policy_test_base as npt

from utils.defer import defer

QONTRACT_E2E_TEST = 'default-network-policies'


@defer
def run(defer=None):
    oc_map = tb.get_oc_map(QONTRACT_E2E_TEST)
    defer(lambda: oc_map.cleanup())
    pattern = tb.get_namespaces_pattern()
    for cluster in oc_map.clusters():
        oc = oc_map.get(cluster)
        logging.info("[{}] validating default NetworkPolicies".format(cluster))

        projects = [p['metadata']['name']
                    for p in oc.get_all('Project')['items']
                    if p['status']['phase'] != 'Terminating' and
                    not re.search(pattern, p['metadata']['name']) and
                    'api.openshift.com/id'
                    not in p['metadata'].get('labels', {})]

        for project in projects:
            logging.info("[{}/{}] validating NetworkPolicies".format(
                cluster, project))
            npt.test_project_network_policies(oc, project)
