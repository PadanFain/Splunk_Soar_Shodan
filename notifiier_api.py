from shodan_consts import SHODAN_NOTIFIER_ID, SHODAN_NOTIFIER_PROVIDER, SHODAN_NOTIFIER
import phantom.app as phantom
from phantom.action_result import ActionResult


class Notifier:
    def __init__(self, parent) -> None:
        self._parent = parent
        
    def common_setup(self, params):
        self._parent.save_progress('In action handler for: {0}'.format(self._parent.get_action_identifier()))       
        return self._parent.add_action_result(ActionResult(dict(params)))

    def get_all_user_notications(self, params):
        action_result = self.common_setup(params)

        ret_val, response = self._make_rest_call(SHODAN_NOTIFIER, action_result, params=None, headers=None)

        summary = action_result.update_summary({})
        summary['total'] = response['total']
        action_result.update_data(response['matches'])

        if phantom.is_fail(ret_val):
            self.save_progress("Get all user notificstions action Failed.")
            return ret_val.get_status()

        self.save_progress("Get all user notificstions Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def get_all_notifiaction_providers(self, params):
        action_result = self.common_setup(params)

        ret_val, response = self._make_rest_call(SHODAN_NOTIFIER_PROVIDER, action_result, params=None, headers=None)
        # response is a dict of dicts, need to massage to make phantom friendly

        remap = []
        for k,v in response.items():
            temp = dict(provider=k, required=v['required']) 
            remap.append(temp)

        summary = action_result.update_summary({})
        summary['total'] = len(remap)
        action_result.update_data(remap)

        if phantom.is_fail(ret_val):
            self.save_progress("Get all user notificstion providers action Failed.")
            return ret_val.get_status()

        self.save_progress("Get all user notificstion providers Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def create_notification(self, params):
        """Create a new notification service for the user. """
        action_result = self.common_setup(params)

        provider = params.get('provider', None)
        if provider is None:
            return action_result.set_status(phantom.APP_ERROR, "Provider Paramater must be included")

        description = params.get('description', None)
        if description is None:
            return action_result.set_status(phantom.APP_ERROR, "Description Paramater must be included")

        args = params.get('args', None)
        if args is None or type(args) is not str:
            return action_result.set_status(phantom.APP_ERROR, "Args Paramater must be included")

        verifed_data = {
            'description': description,
            'provider': provider,
            'args' : args
        }

        ret_val, response = self._make_rest_call(SHODAN_NOTIFIER_PROVIDER, action_result, method="post", data=verifed_data, headers=None)

        summary = action_result.update_summary({})
        summary['success'] = response['success']
        summary['id'] = response['id']

        if phantom.is_fail(ret_val):
            self.save_progress("Get all user notificstion providers action Failed.")
            return ret_val.get_status()

        self.save_progress("Get all user notificstion providers Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def edit_notification(self, params):
        """Edit a notifier. """
        action_result = self.common_setup(params)

        id = params.get('id', None)
        if id is None:
            return action_result.set_status(phantom.APP_ERROR, "Must supply notifier ID")

        args = params.get('args', None)
        if args is None or type(args) is not str:
            return action_result.set_status(phantom.APP_ERROR, "Args Paramater must be included")

        verifed_data = {
            'args' : args
        }

        ret_val, response = self._make_rest_call(SHODAN_NOTIFIER_PROVIDER, action_result, method="post", data=verifed_data, headers=None)

        summary = action_result.update_summary({})
        summary['success'] = response['success']
        summary['id'] = response['id']

        if phantom.is_fail(ret_val):
            self.save_progress("Get all user notificstion providers action Failed.")
            return ret_val.get_status()

        self.save_progress("Get all user notificstion providers Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def retrieve_notification(self, params):
        """Get information about a notifier. """
        action_result = self.common_setup(params)

        id = params.get('id', None)
        if id is None:
            return action_result.set_status(phantom.APP_ERROR, "Must supply notifier ID")

        endpoint = SHODAN_NOTIFIER_ID.format(id=id)
        ret_val, response = self._make_rest_call(endpoint, action_result, headers=None)

        if phantom.is_fail(ret_val):
            self.save_progress("Search Tag Queries action Failed.")
            return ret_val.get_status()

        summary = action_result.update_summary({})
        summary['success'] = True
        action_result.add_data(response)

        self.save_progress("Search tag queries Passed")
        return action_result.set_status(phantom.APP_SUCCESS)


    def delete_notification(self, params):
        """Delete a notification service. """
        self.save_progress('In action handler for: {0}'.format(self.get_action_identifier()))       
        action_result = self._parent.add_action_result(ActionResult(dict(params)))

        id = params.get('id', None)
        if id is None:
            return action_result.set_status(phantom.APP_ERROR, "Must supply notifier ID")

        endpoint = SHODAN_NOTIFIER_ID.format(id=id)
        ret_val, response = self._make_rest_call(endpoint, action_result, method='delete', params=None, headers=None)

        summary = action_result.update_summary({})
        summary['success'] = response['success']

        if phantom.is_fail(ret_val):
            self.save_progress("Search Tag Queries action Failed.")
            return ret_val.get_status()

        self.save_progress("Search tag queries Passed")
        return action_result.set_status(phantom.APP_SUCCESS)


