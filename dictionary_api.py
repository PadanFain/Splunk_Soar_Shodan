from shodan_consts import SHODAN_QUERY, SHODAN_QUERY_SEARCH, SHODAN_QUERY_TAGS
import phantom.app as phantom
from phantom.action_result import ActionResult


class Dictionary:
    def __init__(self, parent) -> None:
        self._parent = parent
        

    def resquest_helper(self, endpoint, params, action_result):
        get_full_list = params['page'] == 0
        found_matches = []

        if get_full_list:
            page = 1
            more_pages = True
            while more_pages:
                params['page'] = page
                ret_val, response = self._parent._make_rest_call(endpoint, action_result, params=params, headers=None)
                found_matches.extend(response['matches'])
                # each page sends 10 entries
                more_pages = page * 10 > response['total']
                page += 1
        else:
            # make single rest call
            params['page'] = page
            ret_val, response = self._make_rest_call(endpoint, action_result, params=params, headers=None)
            found_matches.extend(response['matches'])

        if phantom.is_fail(ret_val):
            self.save_progress("Action Failed.")
            return action_result.get_status()

        summary = action_result.update_summary({})
        summary['total_matches'] = response['total']
        action_result.update_data(found_matches)

        return action_result.set_status(phantom.APP_SUCCESS)

    def queries(self, params):        
        """List the search queries that have been shared by other users. """
        self.save_progress('In action handler for: {0}'.format(self.get_action_identifier()))       
        action_result = self._parent.add_action_result(ActionResult(dict(params)))

        page = params.get('page', 1)
        get_full_list = False
        if page < 0:
            return action_result.set_status(phantom.APP_ERROR, "Page Paramater must be the number 0 or greater")

        order = params.get('order', 'desc')
        if order not in ['desc', 'asc']:
            return action_result.set_status(phantom.APP_ERROR, "Order Paramater must be desc or asc")

        sort = params.get('sort', 'timestamp')
        if sort not in ['timestamp', 'votes']:
            return action_result.set_status(phantom.APP_ERROR, "Sort Paramater must be votes or timestamp")

        verifed_params = {
            'sort': sort,
            'order': order,
            'page' : page
        }

        result =  self.resquest_helper(self, SHODAN_QUERY, verifed_params, action_result)

        if phantom.is_fail(result):
            self.save_progress("List Queries action Failed.")
            return result.get_status()

        self.save_progress("List queries Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def queries_search(self, params):
        """Search the directory of saved search queries in Shodan. """
        self.save_progress('In action handler for: {0}'.format(self.get_action_identifier()))       
        action_result = self._parent.add_action_result(ActionResult(dict(params)))

        page = params.get('page', 1)
        if page < 0 or type(page) is not int:
            return action_result.set_status(phantom.APP_ERROR, "Page Paramater must be the number 0 or greater")

        query = params.get('query', None)
        if query is None:
            return action_result.set_status(phantom.APP_ERROR, "Query Paramater must be provided")

        verifed_params = {
            'page': page,
            'query': query,
        }

        result =  self.resquest_helper(self, SHODAN_QUERY_SEARCH, verifed_params, action_result)

        if phantom.is_fail(result):
            self.save_progress("Search Queries action Failed.")
            return result.get_status()

        self.save_progress("Search queries Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def queries_tags(self, params):
    #  def queries_tags(self, size=10):
        """List the most popular tags. """
        self.save_progress('In action handler for: {0}'.format(self.get_action_identifier()))       
        action_result = self._parent.add_action_result(ActionResult(dict(params)))

        size = params.get('size', 1)
        if size < 1 or type(size) is not int:
            return action_result.set_status(phantom.APP_ERROR, "Page Paramater must be the number 0 or greater")

        verifed_params = {
            'size': size,
        }        
        ret_val, response = self._make_rest_call(SHODAN_QUERY_TAGS, action_result, params=verifed_params, headers=None)
        found_matches = response['matches']

        summary = action_result.update_summary({})
        summary['total_matches'] = response['total']
        action_result.update_data(found_matches)


        if phantom.is_fail(ret_val):
            self.save_progress("Search Tag Queries action Failed.")
            return ret_val.get_status()

        self.save_progress("Search tag queries Passed")
        return action_result.set_status(phantom.APP_SUCCESS)
