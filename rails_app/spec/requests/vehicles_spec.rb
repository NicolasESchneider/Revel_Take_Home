RSpec.describe 'Vehicle API', type: :request do
    # initialize test data 
    let!(:vehicles) { create_list(:vehicle, 10) }
    let(:vehicle_id) { vehicles.first.id }

    # if you want to use fixtures
    let(:vehicles_raw) { yaml_fixture_file("vehicles.yml") }
  
    # Test suite for GET /vehicles
    describe 'GET /vehicles' do
      # make HTTP get request before each example
      before { get '/vehicles' }
  
      it 'returns vehicles' do
        # Note `json` is a custom helper to parse JSON responses
        expect(json).not_to be_empty
        expect(json.size).to eq(10)
      end
  
      it 'returns status code 200' do
        expect(response).to have_http_status(200)
      end
    end
  
    # Test suite for GET /vehicles/:id
    describe 'GET /vehicles/:id' do
      before { get "/vehicles/#{vehicle_id}" }
  
      context 'when the record exists' do
        it 'returns the vehicle' do
          expect(json).not_to be_empty
          expect(json['id']).to eq(vehicle_id)
        end
  
        it 'returns status code 200' do
          expect(response).to have_http_status(200)
        end
      end
  
      context 'when the record does not exist' do
        let(:vehicle_id) { 100 }
  
        it 'returns status code 404' do
          expect(response).to have_http_status(404)
        end
  
        it 'returns a not found message' do
          expect(response.body).to match(/Couldn't find Vehicle/)
        end
      end
    end
  end