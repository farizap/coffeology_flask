import json
from . import app, client, cache, create_token_non_internal, create_token_internal, reset_database


class TestRecipeCrud():

    reset_database()

# recipe get by id
    def test_recipe_get_by_id_valid(self, client):
        # token = create_token_non_internal()
        res = client.get('/recipes/1',
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_by_id_invalid(self, client):
        # token = create_token_non_internal()
        res = client.get('/recipes/-1',
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 404

# recipe get all
    def test_recipe_get_all_valid_1(self, client):
        # token = create_token_non_internal()
        res = client.get('/recipes', content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_get_all_valid_2(self, client):
        # token = create_token_non_internal()
        data = {
            'userID' : 1,
            'methodID' : 1,
            'orderby' : 'favoriteCount',
            'sort' : 'asc'
        }
        res = client.get('/recipes', query_string=data, content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200  
    
    def test_recipe_get_all_valid_3(self, client):
        # token = create_token_non_internal()
        data = {
            'userID' : 1,
            'methodID' : 1,
            'orderby' : 'favoriteCount',
            'sort' : 'desc'
        }
        res = client.get('/recipes', query_string=data, content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200  

    def test_recipe_get_all_valid_4(self, client):
        # token = create_token_non_internal()
        data = {
            'orderby' : 'difficulty',
            'sort' : 'asc'
        }
        res = client.get('/recipes', query_string=data, content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200  

    def test_recipe_get_all_valid_5(self, client):
        # token = create_token_non_internal()
        data = {
            'orderby' : 'difficulty',
            'sort' : 'desc'
        }
        res = client.get('/recipes', query_string=data, content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200  

    def test_recipe_get_all_invalid(self, client):
        # token = create_token_non_internal()
        data = {
            'userID' : -1,
            'methodID' : -1
        }
        res = client.get('/recipes', query_string=data, content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 404  

    
# recipe options
    def test_recipe_options_by_id_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/recipes/1',
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200

    def test_recipe_options_valid(self, client):
        # token = create_token_non_internal()
        res = client.options('/recipes',
                        content_type='application/json')
        
        res_json=json.loads(res.data)
        assert res.status_code == 200