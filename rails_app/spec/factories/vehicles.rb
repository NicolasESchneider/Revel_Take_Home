FactoryBot.define do
  factory :vehicle do
    license_plate { "MyString" }
    battery_level { 1.5 }
    in_use { false }
    model { "MyString" }
    location_lat { 1.5 }
    location_long { 1.5 }
  end
end
