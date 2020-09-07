class CreateVehicles < ActiveRecord::Migration[6.0]
  def change
    create_table :vehicles do |t|
      t.string :license_plate
      t.float :battery_level
      t.boolean :in_use
      t.string :model
      t.float :location_lat
      t.float :location_long

      t.timestamps
    end
  end
end
