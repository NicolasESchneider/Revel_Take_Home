class VehiclesController < ApplicationController
  before_action :set_vehicle, only: [:show]

  rescue_from ActiveRecord::RecordNotFound do |e|
    json_response({ message: e.message }, :not_found)
  end

  rescue_from ActiveRecord::RecordInvalid do |e|
    json_response({ message: e.message }, :unprocessable_entity)
  end

  # GET /vehicles
  def index
    @vehicles = Vehicle.all
    json_response(@vehicles)
  end

  # POST /vehicles
  def create
    @vehicle = Vehicle.create!(vehicle_params)
    json_response(@vehicle, :created)
  end

  # GET /vehicles/:id
  def show
    json_response(@vehicle)
  end

  private

  def set_vehicle
    @vehicle = Vehicle.find(params[:id])
  end

  def json_response(object, status = :ok)
    render json: object, status: status
  end
end
