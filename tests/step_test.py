import json
from . import app, client, cache, create_token_non_internal, create_token_internal, reset_database


class TestStepCrud():

    reset_database()

# step get all
    def test_step_get_all_valid(self, client):
        # token = create_token_non_internal()
        data = {
            'recipeID' : 1
        }
        res = client.get('/steps', query_string=data, content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200  
    
    def test_step_get_all_invalid(self, client):
        # token = create_token_non_internal()
        data = {
           'recipeID' : -1
        }
        res = client.get('/steps', query_string=data, content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 404

# step options
    def test_step_options_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/steps',
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200