from apigee_python_client import ApigeeClient

"""
Script used for testing

Usage: poetry run pytest
"""

client = ApigeeClient()
organisation = "my-organization"
proxy_name = "test-undeploy"
environment = "sandbox1"
kvm = "custom-test-kvm"
kvm_entry = "custom-test-kvm-entry"
developer = "the-developer@developer.com"


def test_proxies():
    proxies = client.proxy_client.list_proxies(organisation)

    assert len(proxies) > 0

    deployments = client.proxy_client.list_proxy_deployments(organisation, proxy_name)
    bundle = client.proxy_client.get_proxy_bundle_for_environment(organisation, proxy_name, environment)
    revisions = client.proxy_client.get_revisions_by_env(organisation, proxy_name)


def test_environments():
    environments = client.environment_client.list_environments(organisation)
    deployments = client.environment_client.list_environment_deployments(organisation, environment)

    targets = client.environment_client.list_environment_targets(organisation, environment)
    if len(targets) > 0:
        target = client.environment_client.get_environment_target(organisation, environment, targets[0])

    envgroups = client.environment_client.list_environment_groups(organisation)
    host_by_env = client.environment_client.get_hosts_by_env(organisation)


def test_kvm():
    environments = client.environment_client.list_environments(organisation)
    kvms = client.kvm_client.list_environment_kvms(organisation, environment[0])

    if len(kvms) > 0:
        entries = client.kvm_client.list_environment_kvm_entries(organisation, environment[0], kvms[0])

    kvms = client.kvm_client.list_proxy_kvms(organisation, proxy_name)
    if len(kvms) > 0:
        entries = client.kvm_client.list_proxy_kvm_entries(organisation, proxy_name, kvms[0])
